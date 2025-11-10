import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === CONFIGURAZIONE ===
SHEET_ID = "1P6SV2hYDgfA0Nkv2FI9NA-siYOdB8YLsQnCv5QsFEhI"
WORKSHEET = "Europe Countries GDP"

# Lista dei possibili percorsi del file JSON su diversi PC
json_paths = [
    r"C:\Users\utente\Desktop\Personal\google.json",
    r"C:\Users\franc\Documents\google.json"
]

# Trova il percorso valido
JSON_FILE = None
for path in json_paths:
    if os.path.exists(path):
        JSON_FILE = path
        break

if JSON_FILE is None:
    raise FileNotFoundError("File google.json non trovato in nessuno dei percorsi definiti!")

print(f"✅ File JSON trovato: {JSON_FILE}")

# === CONNESSIONE A GOOGLE SHEETS ===
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def load_data_from_sheets():
    """Carica i dati da Google Sheets"""
    try:
        print("📊 Connessione a Google Sheets in corso...")
        creds = Credentials.from_service_account_file(JSON_FILE, scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET)
        
        # Ottieni tutti i dati
        data = worksheet.get_all_values()
        
        # Crea DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])  # Prima riga = header
        
        # Converti la colonna Date/Year in intero
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        
        # Converti tutte le altre colonne in float
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Rinomina la prima colonna in "Year" se necessario
        if df.columns[0] != "Year":
            df.rename(columns={df.columns[0]: "Year"}, inplace=True)
        
        print(f"✅ Dati caricati: {len(df)} anni, {len(df.columns)-1} paesi")
        return df
    
    except Exception as e:
        print(f"❌ Errore nel caricamento dei dati: {str(e)}")
        return None

# === CARICAMENTO DATI ===
df = load_data_from_sheets()

if df is None or df.empty:
    raise Exception("Impossibile caricare i dati!")

# === CONFIGURAZIONE VISUALIZZAZIONE ===
# Modifica questi parametri per personalizzare i grafici

# Paesi da visualizzare
SELECTED_COUNTRIES = ["Euro area", "Italy", "Germany", "France", "Poland"]

# Range di anni (None = tutti gli anni disponibili)
YEAR_START = None  # es. 2000 per iniziare dal 2000, None per tutti
YEAR_END = None    # es. 2023 per finire al 2023, None per tutti

# Verifica che i paesi esistano nel dataset
available_countries = [col for col in df.columns if col != "Year"]
SELECTED_COUNTRIES = [c for c in SELECTED_COUNTRIES if c in available_countries]

if not SELECTED_COUNTRIES:
    print("⚠️ Nessun paese valido selezionato, uso i primi 5 paesi disponibili")
    SELECTED_COUNTRIES = available_countries[:5]

print(f"\n📍 Paesi selezionati: {', '.join(SELECTED_COUNTRIES)}")

# Filtra per anni se specificato
if YEAR_START is not None or YEAR_END is not None:
    year_start = YEAR_START if YEAR_START is not None else df["Year"].min()
    year_end = YEAR_END if YEAR_END is not None else df["Year"].max()
    df_filtered = df[(df["Year"] >= year_start) & (df["Year"] <= year_end)].copy()
    print(f"📅 Range anni: {int(year_start)} - {int(year_end)}")
else:
    df_filtered = df.copy()
    print(f"📅 Range anni: {int(df['Year'].min())} - {int(df['Year'].max())} (tutti)")

# === VISUALIZZAZIONE DATI ===
print("\n" + "="*70)
print("📋 PRIME 10 RIGHE DEL DATASET")
print("="*70)
print(df_filtered.head(10).to_string())

print("\n" + "="*70)
print("📊 STATISTICHE DESCRITTIVE")
print("="*70)
print(df_filtered[SELECTED_COUNTRIES].describe().to_string())

# === GRAFICO A BARRE ===
print("\n📈 Generazione grafico a barre...")

fig, ax = plt.subplots(figsize=(16, 8))

x = range(len(df_filtered))
width = 0.8 / len(SELECTED_COUNTRIES)

# Colori
colors = plt.cm.Set3(range(len(SELECTED_COUNTRIES)))

# Crea le barre per ogni paese
for idx, country in enumerate(SELECTED_COUNTRIES):
    offset = (idx - len(SELECTED_COUNTRIES)/2) * width + width/2
    ax.bar(
        [i + offset for i in x],
        df_filtered[country],
        width,
        label=country,
        alpha=0.85,
        color=colors[idx]
    )

# Personalizzazione
ax.set_xlabel("Anno", fontsize=13, fontweight='bold')
ax.set_ylabel("PIL (%)", fontsize=13, fontweight='bold')
ax.set_title(
    f"Crescita del PIL ({int(df_filtered['Year'].min())}-{int(df_filtered['Year'].max())})",
    fontsize=15,
    fontweight='bold',
    pad=20
)
ax.set_xticks(x)
ax.set_xticklabels(df_filtered["Year"].astype(int), rotation=45, ha='right')
ax.legend(loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.axhline(y=0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig('gdp_barchart.png', dpi=300, bbox_inches='tight')
print("✅ Grafico a barre salvato come: gdp_barchart.png")

# === GRAFICO A LINEE ===
print("\n📉 Generazione grafico a linee...")

fig2, ax2 = plt.subplots(figsize=(16, 8))

for country in SELECTED_COUNTRIES:
    ax2.plot(
        df_filtered["Year"],
        df_filtered[country],
        marker='o',
        label=country,
        linewidth=2.5,
        markersize=5
    )

ax2.set_xlabel("Anno", fontsize=13, fontweight='bold')
ax2.set_ylabel("PIL (%)", fontsize=13, fontweight='bold')
ax2.set_title(
    f"Andamento PIL nel tempo ({int(df_filtered['Year'].min())}-{int(df_filtered['Year'].max())})",
    fontsize=15,
    fontweight='bold',
    pad=20
)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.axhline(y=0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig('gdp_linechart.png', dpi=300, bbox_inches='tight')
print("✅ Grafico a linee salvato come: gdp_linechart.png")

# === STATISTICHE PER PAESE ===
print("\n" + "="*70)
print("📊 STATISTICHE PER PAESE SELEZIONATO")
print("="*70)

stats_data = []
for country in SELECTED_COUNTRIES:
    country_data = df_filtered[country].dropna()
    max_year = df_filtered.loc[country_data.idxmax(), "Year"]
    min_year = df_filtered.loc[country_data.idxmin(), "Year"]
    
    stats_data.append({
        "Paese": country,
        "Media (%)": f"{country_data.mean():.2f}",
        "Max (%)": f"{country_data.max():.2f} ({int(max_year)})",
        "Min (%)": f"{country_data.min():.2f} ({int(min_year)})",
        "Dev. Std.": f"{country_data.std():.2f}"
    })

stats_df = pd.DataFrame(stats_data)
print(stats_df.to_string(index=False))

# === HEATMAP (BONUS) ===
print("\n🔥 Generazione heatmap...")

fig3, ax3 = plt.subplots(figsize=(16, 10))

# Prepara dati per heatmap
heatmap_data = df_filtered.set_index("Year")[SELECTED_COUNTRIES].T

sns.heatmap(
    heatmap_data,
    annot=False,
    fmt=".1f",
    cmap="RdYlGn",
    center=0,
    cbar_kws={'label': 'PIL (%)'},
    ax=ax3
)

ax3.set_title(
    f"Heatmap PIL ({int(df_filtered['Year'].min())}-{int(df_filtered['Year'].max())})",
    fontsize=15,
    fontweight='bold',
    pad=20
)
ax3.set_xlabel("Anno", fontsize=12, fontweight='bold')
ax3.set_ylabel("Paese", fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('gdp_heatmap.png', dpi=300, bbox_inches='tight')
print("✅ Heatmap salvata come: gdp_heatmap.png")

# === ESPORTA DATI FILTRATI ===
output_file = "gdp_data_filtered.csv"
df_filtered.to_csv(output_file, index=False)
print(f"\n💾 Dati filtrati esportati in: {output_file}")

# === MOSTRA GRAFICI ===
print("\n" + "="*70)
print("🎨 Visualizzazione grafici in corso...")
print("="*70)
print("ℹ️ Chiudi le finestre dei grafici per terminare il programma")

plt.show()

print("\n✅ Analisi completata!")