import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SHEET_URL = "https://docs.google.com/spreadsheets/d/1P6SV2hYDgfA0Nkv2FI9NA-siYOdB8YLsQnCv5QsFEhI/edit"

TABS = [
    "EuropeGDPForecast",
    "EuropeGDPAnnual",
    "EuropeHICPForecast",
    "EuropeHICPAnnual",
    "Rates-Imported",
    "EUHICPData-Imported",
    "EUGDP-Imported",
    "USGDPData-Imported",
    "USPCEData-Imported",
]

POSSIBLE_PATHS = [
    r"C:/Users/utente/Desktop/Personal/google.json",
    r"C:/Users/franc/Documenti/google.json",
    os.path.expanduser("~/google.json"),   # fallback generico
]


def find_credentials_file():
    for path in POSSIBLE_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "Nessun file google.json trovato nei percorsi specificati. "
        "Aggiungi il path corretto alla lista POSSIBLE_PATHS."
    )


def connect_to_google_sheet():
    path = find_credentials_file()

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    creds = Credentials.from_service_account_file(path, scopes=scopes)
    return gspread.authorize(creds)


def load_single_tab(client, tab_name):
    try:
        spreadsheet = client.open_by_url(SHEET_URL)
        ws = spreadsheet.worksheet(tab_name)
        data = ws.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])
    except Exception:
        return None


def load_all_data():
    client = connect_to_google_sheet()
    dfs = {}

    for tab in TABS:
        df = load_single_tab(client, tab)
        if df is not None:
            dfs[tab] = df

    return dfs
