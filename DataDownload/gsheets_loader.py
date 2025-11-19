import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

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
    "US PCE Data-Imported",
]


def connect_to_google_sheet(credentials_path):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    return gspread.authorize(creds)


def load_single_tab(client, tab_name):
    try:
        spreadsheet = client.open_by_url(SHEET_URL)
        ws = spreadsheet.worksheet(tab_name)
        data = ws.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])
    except Exception:
        return None


def load_all_data(credentials_path="C:/Users/utente/Desktop/Personal/google.json"):
    client = connect_to_google_sheet(credentials_path)
    dfs = {}
    for tab in TABS:
        df = load_single_tab(client, tab)
        if df is not None:
            dfs[tab] = df
    return dfs
