import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1P6SV2hYDgfA0Nkv2FI9NA-siYOdB8YLsQnCv5QsFEhI/edit"

TABS = [
    "Europe GDP Forecast",
    "Europe GDP Annual",
    "Europe HICP Forecast",
    "Europe HICP Annual",
    "Rates-Imported",
    "EU HICP Data-Imported",
    "EU GDP-Imported",
    "US GDP Data-Imported",
    "US PCE Data-Imported"
]

def connect_to_google_sheet(credentials_path):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def load_tabs(client, sheet_url, tabs):
    spreadsheet = client.open_by_url(sheet_url)
    out = {}

    for tab in tabs:
        ws = spreadsheet.worksheet(tab)
        data = ws.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        out[tab] = df

    return out

# QUI METTI IL PATH GIUSTO
client = connect_to_google_sheet(
    credentials_path="C:/Users/utente/Desktop/Personal/google.json"
)

dfs = load_tabs(client, SHEET_URL, TABS)

print("Caricati tab:", list(dfs.keys()))

# Visualizza le prime righe di "Europe GDP Forecast"
tab_name = "Europe GDP Forecast"
if tab_name in dfs:
    print(f"\nPrime righe di '{tab_name}':")
    # Stampa in modo leggibile anche con molte colonne
    print(dfs[tab_name].head().to_string(index=False))
else:
    print(f"\nTab non trovato: {tab_name}")
