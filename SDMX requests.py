"""
Scarica indicatori macroeconomici da Eurostat e salva in Excel
"""
import os
import requests
import pandas as pd

# ===== CONFIGURAZIONE =====
BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
GEOS = ["EA20","AT","BE","HR","CY","EE","FI","FR","DE","GR","IE","IT","LV","LT","LU","MT","NL","PT","SK","SI","ES"]

# Indicatori da scaricare: (dataset, parametri, frequenza)
INDICATORS = {
    "HICP": ("prc_hicp_midx", {"unit": "I15", "coicop": "CP00", "freq": "M"}, "M"),
    "GDP": ("namq_10_gdp", {"freq": "Q", "na_item": "B1GQ", "unit": "CLV20_MNAC", "s_adj": "NSA"}, "Q"),
    "Unemployment": ("une_rt_m", {"sex": "T", "age": "TOTAL", "unit": "PC_ACT", "freq": "M"}, "M"),
    "IndustrialProduction": ("sts_inpr_m", {"indic_bt": "PRD", "s_adj": "CA", "nace_r2": "B-D", "freq": "M", "unit": "I15"}, "M"),
    "RetailSales": ("sts_trtu_m", {"indic_bt": "VOL_SLS", "s_adj": "SCA", "nace_r2": "G", "freq": "M", "unit": "PCH_PRE"}, "M")
}


def scarica_indicatore(dataset, params, freq, nome, geo):
    """Scarica un indicatore da Eurostat e calcola le variazioni percentuali"""
    
    # Chiamata API
    try:
        r = requests.get(f"{BASE_URL}/{dataset}", 
                        params={**params, "geo": geo, "format": "JSON"}, 
                        timeout=30)
        if r.status_code != 200:
            print(f"✗ Errore {r.status_code} per {nome} {geo}")
            return pd.DataFrame()
        data = r.json()
    except Exception as e:
        print(f"✗ Errore connessione {nome} {geo}: {e}")
        return pd.DataFrame()
    
    # Verifica che ci siano dati
    if "dimension" not in data or "time" not in data["dimension"] or "value" not in data:
        print(f"✗ Nessun dato per {nome} {geo}")
        return pd.DataFrame()
    
    # Estrai le date e i valori
    time_idx = data["dimension"]["time"]["category"]["index"]
    idx_to_date = {v: k for k, v in time_idx.items()}  # Mappa indice → data
    
    # Crea lista di osservazioni
    obs = [{"date": idx_to_date[int(k)], "value": v, "geo": geo, "group": nome}
           for k, v in data["value"].items() if int(k) in idx_to_date]
    
    df = pd.DataFrame(obs)
    if df.empty:
        return df
    
    # Converti le date
    if freq == "M":
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m", errors="coerce")
    else:  # freq == "Q"
        df["date"] = pd.PeriodIndex(df["date"], freq="Q").to_timestamp()
    
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    
    # Calcola variazioni percentuali
    if freq == "M":
        df["mom_pct"] = df.groupby("geo")["value"].pct_change(1) * 100   # Mensile
        df["yoy_pct"] = df.groupby("geo")["value"].pct_change(12) * 100  # Annuale
    else:  # freq == "Q"
        df["qoq_pct"] = df.groupby("geo")["value"].pct_change(1) * 100   # Trimestrale
        df["yoy_pct"] = df.groupby("geo")["value"].pct_change(4) * 100   # Annuale
    
    print(f"✓ {nome} {geo}")
    return df


def main():
    """Scarica tutti gli indicatori e salva in Excel"""
    
    print("Scaricamento da Eurostat...\n")
    risultati = {}
    
    # Per ogni indicatore
    for nome, (dataset, params, freq) in INDICATORS.items():
        print(f"{nome}:")
        dati = []
        
        # Scarica per ogni paese
        for geo in GEOS:
            df = scarica_indicatore(dataset, params, freq, nome, geo)
            if not df.empty:
                dati.append(df)
        
        # Unisci tutti i paesi
        if dati:
            risultati[nome] = pd.concat(dati, ignore_index=True)
        print()
    
    # Salva in Excel
    if risultati:
        file = "macro_indicators_output.xlsx"
        with pd.ExcelWriter(file, engine="openpyxl") as writer:
            for nome, df in risultati.items():
                df.to_excel(writer, sheet_name=nome, index=False)
        
        print(f"\n✓ File creato: {file}")
        print(f"  Fogli: {', '.join(risultati.keys())}")
        print(f"  Percorso: {os.path.abspath(file)}")
    else:
        print("\n✗ Nessun dato scaricato")


if __name__ == "__main__":
    main()