import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# === CONFIGURAZIONE ===
SHEET_ID = "1FxfkmF_3x-YzNWsCYYr1GsgHM1pq2tuPB-CWAIk-aPw"
WORKSHEET = "Europe Countries GDP"  # cambia con il tab che vuoi
JSON_FILE = "google.json"

# === CONNESSIONE ===
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

print("✅ Connessione riuscita! Prime righe:")
display(df.head())
