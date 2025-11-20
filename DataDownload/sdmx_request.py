"""
SDMX_request.py
Modulo per scaricare e trasformare i dati Eurostat
Utilizza indicators_config.py per configurazioni.
Include caching opzionale per evitare richieste ripetute.
"""

import os
import json
import hashlib
import requests
import pandas as pd
from indicators_config import INDICATORS, GEOS

# ==============================
# Configurazioni generali
# ==============================
BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ==============================
# Funzioni interne
# ==============================

def _params_hash(params):
    """Crea un hash stabile dai params (ordinando le chiavi)."""
    try:
        serialized = json.dumps(params, sort_keys=True, ensure_ascii=False)
    except Exception:
        serialized = str(params)
    return hashlib.sha1(serialized.encode("utf-8")).hexdigest()

def _cache_file_name(dataset, geo, params):
    """Nome del file di cache che include dataset, geo e hash dei params."""
    ph = _params_hash(params or {})
    filename = f"{dataset}_{geo}_{ph}.json"
    # rimuovi caratteri non sicuri
    filename = "".join(ch for ch in filename if ch.isalnum() or ch in ("_", "-")) + ".json"
    return os.path.join(CACHE_DIR, filename)

def download_single_indicator(dataset, params, freq, nome, geo, use_cache=True):
    """
    Scarica un indicatore Eurostat per una singola nazione.
    Salva in cache se use_cache=True.
    """
    cache_path = _cache_file_name(dataset, geo, params)
    data = None

    # Prova a leggere dalla cache
    if use_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Impossibile leggere cache {cache_path}: {e}. Scarico da remoto.")
            data = None

    if data is None:
        try:
            r = requests.get(
                f"{BASE_URL}/{dataset}",
                params={**params, "geo": geo, "format": "JSON"},
                timeout=30
            )
            r.raise_for_status()
            data = r.json()
            if use_cache:
                try:
                    with open(cache_path, "w", encoding="utf-8") as f:
                        json.dump(data, f)
                except Exception as e:
                    print(f"[WARN] Impossibile scrivere cache {cache_path}: {e}")
        except Exception as e:
            print(f"[ERRORE] Download {nome} per {geo}: {e}")
            return pd.DataFrame()

    # Parsing minimo e robusto
    if not isinstance(data, dict) or "dimension" not in data or "time" not in data["dimension"] or "value" not in data:
        return pd.DataFrame()

    # time index mapping
    try:
        time_idx = {v: k for k, v in data["dimension"]["time"]["category"]["index"].items()}
    except Exception:
        return pd.DataFrame()

    rows = []
    for k, v in data["value"].items():
        try:
            ik = int(k)
        except Exception:
            continue
        if ik in time_idx:
            rows.append({"date": time_idx[ik], "value": v, "geo": geo, "group": nome})

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # Converti date
    if freq == "M":
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m", errors="coerce")
    elif freq == "Q":
        # PeriodIndex -> timestamp (start of period)
        try:
            df["date"] = pd.PeriodIndex(df["date"], freq="Q").to_timestamp()
        except Exception:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
    elif freq == "A":
        df["date"] = pd.to_datetime(df["date"], format="%Y", errors="coerce")
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])

    # Aggiungi variazioni base (opzionali)
    if freq == "M":
        df["mom_pct"] = df.groupby("geo")["value"].pct_change(1) * 100
        df["yoy_pct"] = df.groupby("geo")["value"].pct_change(12) * 100
    elif freq == "Q":
        df["qoq_pct"] = df.groupby("geo")["value"].pct_change(1) * 100
        df["yoy_pct"] = df.groupby("geo")["value"].pct_change(4) * 100
    elif freq == "A":
        df["yoy_pct"] = df.groupby("geo")["value"].pct_change(1) * 100

    return df

# ==============================
# Funzione principale pubblica
# ==============================
def download_SDMX_data(use_cache=True):
    """
    Scarica tutti gli indicatori definiti in indicators_config.py
    Restituisce dict di DataFrame: { nome_indicatore: df }
    """
    results = {}
    for nome, (dataset, params, freq) in INDICATORS.items():
        dfs = []
        for geo in GEOS:
            df = download_single_indicator(dataset, params, freq, nome, geo, use_cache)
            if not df.empty:
                dfs.append(df)
        if dfs:
            results[nome] = pd.concat(dfs, ignore_index=True)
    return results

# ==============================
# Funzione di salvataggio Excel
# ==============================
# def save_to_excel(results, filename="macro_indicators.xlsx"):
#    if not results:
#        return None
#    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
#        for nome, df in results.items():
#            df.to_excel(writer, sheet_name=nome[:31], index=False)
#    return os.path.abspath(filename)

# ==============================
# Esecuzione diretta
# ==============================
if __name__ == "__main__":
    print("[INFO] Scaricando tutti gli indicatori...")
    data = download_SDMX_data()
#    path = save_to_excel(data)
#   print("[INFO] Dati salvati in:", path)
