# report_example.py
import pandas as pd
from sdmx_request import download_SDMX_data  # modulo SDMX
from transformations import pivot_long_to_wide  # pivot helper
import matplotlib.pyplot as plt

def main():
    # ==============================
    # 1) SCARICA DATI SDMX
    # ==============================
    print("[INFO] Scaricando dati SDMX da Eurostat...")
    sdmx_data = download_SDMX_data()

    # ==============================
    # 2) PREPARA I DATI PER LA PIVOT
    # ==============================
    all_data = []

    for key, df in sdmx_data.items():
        # Verifica che ci sia 'date', 'value', 'geo' o simili
        if 'date' not in df.columns or 'value' not in df.columns:
            print(f"[ERRORE] La serie '{key}' non contiene le colonne necessarie. Ignorata.")
            continue

        # Creiamo una colonna 'series' combinando indicatore e paese (geo)
        if 'geo' in df.columns:
            df['series'] = key + "_" + df['geo']
        else:
            df['series'] = key

        all_data.append(df[['date', 'series', 'value']])

    if not all_data:
        print("[ERRORE] Nessun dato valido da pivotare.")
        return

    all_data = pd.concat(all_data, ignore_index=True)

    # ==============================
    # 3) TRASFORMA IN FORMATO WIDE
    # ==============================
    wide_data = pivot_long_to_wide(all_data, index="date", columns="series", values="value")
   
    
    # ==== Grafico: colonne per GDP_ITA e GDP_FR dal 2010 ad oggi ====
  

    df_plot = wide_data.copy()
    # Assumiamo che 'date' sia una colonna; altrimenti adattare (es. index)
    df_plot['date'] = pd.to_datetime(df_plot['date'], errors='coerce')
    df_plot = df_plot.dropna(subset=['date']).set_index('date')

    cols = ['GDP_EA20', 'GDP_DE', 'GDP_FR', 'GDP_ES']
    missing = [c for c in cols if c not in df_plot.columns]
    if missing:
        print(f"[WARN] Colonne mancanti: {missing}. Controlla i nomi delle serie nel pivot.")
    else:
        # Aggrega su base annuale (ultima osservazione dell'anno) e filtra dal 2010
        df_year = df_plot[cols].resample('YE').last()
        df_year = df_year[df_year.index.year >= 2010]

        if df_year.empty:
            print("[WARN] Nessun dato disponibile dal 2010 in poi per le colonne richieste.")
        else:
            ax = df_year.plot(kind='bar', figsize=(12,6))
            ax.set_xlabel('Anno')
            ax.set_ylabel('GDP')
            ax.set_title('GDP BIG4 (2010 - oggi)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
    
    # ==============================
    # 4) SALVA RISULTATI
    # ==============================
    output_file = "report_data_ready.xlsx"
    try:
        wide_data.to_excel(output_file, index=False)
        print(f"[INFO] Report pronto: {output_file}")
    except PermissionError:
        print(f"[ERRORE] Non posso scrivere il file '{output_file}'. Chiudi eventuali copie aperte.")

if __name__ == "__main__":
    main()
 # Stampa le prime righe del DataFrame finale
