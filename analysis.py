# analysis.py

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === CONFIGURAZIONE ===
SHEET_ID = "1FxfkmF_3x-YzNWsCYYr1GsgHM1pq2tuPB-CWAIk-aPw"  # ID del Google Sheet
WORKSHEET = "Europe Countries GDP"  # Nome del tab
JSON_FILE = r"C:\Users\utente\Desktop\PythoncodeDashboard\google.json"  # File chiave JSON del Service Account

# === CONNESSIONE A GOOGLE SHEETS ===
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(JSON_FILE, scopes=SCOPE)
client = gspread.authorize(creds)

# === LETTURA DATI ===
sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# === OUTPUT SU TERMINALE VS ===
print("Prime righe del dataset:")
print(df.head(), "\n")

print("Statistiche descrittive:")
print(df.describe(), "\n")

import pandas as pd
import matplotlib.pyplot as plt

# === DATI E COLONNE ===
data = [
    ["1999", 2.907058688, 3.658582858, 3.542740902, -0.8486944934, 4.997954695, -0.5105465522, 4.38993302, 3.260717433, 1.990435317, 2.65880935, 10.53026966, 1.62880629, 2.550927434, -1.087485435, 8.176141678],
    ["2000", 4.034347457, 3.411957504, 3.716681052, 2.94525311, 5.965304455, 9.863549754, 5.75254079, 4.363914558, 3.106803498, 4.137806946, 9.403093201, 4.205536067, 5.86866135, 3.361962747, 6.938181063],
    ["2001", 2.157626917, 1.28685791, 1.099612482, 3.111234952, 3.952562582, 5.852183707, 2.641424003, 1.846576836, 1.752346516, 4.650447273, 5.30557305, 1.854856928, 6.282007098, 6.634470954, 3.074352696],
]

columns = [
    "Year", "Euro area", "Austria", "Belgium", "Croatia", "Cyprus", "Estonia", "Finland",
    "France", "Germany", "Greece", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg"
]
df = pd.DataFrame(data, columns=columns)

# === CONVERSIONI ===
df["Year"] = df["Year"].astype(int)
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# === GRAFICO A COLONNE PER OGNI PAESE E ANNO ===
# Se vuoi limitare a pochi paesi per leggibilità:
countries = ["Italy", "Germany", "France", "Spain","Euro area","Austria","Belgium","Croatia","Cyprus","Estonia","Finland"]  # Modifica qui
available = [c for c in countries if c in df.columns]  # nel caso "Spain" non ci sia

# Grafico a colonne multiple (anni sull'asse X)
df.plot(
    x="Year",
    y=available,
    kind="bar",
    figsize=(12, 6)
)

plt.title("Confronto valori per paese (1999–2001)")
plt.xlabel("Anno")
plt.ylabel("Valore (%)")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.legend(title="Paese", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("✅ Grafico a colonne con tutti gli anni completato.")
