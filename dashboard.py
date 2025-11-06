import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("🔗 Test Connessione Google Sheets")

# 1️⃣ Autenticazione
creds = Credentials.from_service_account_info(st.secrets["google"])
client = gspread.authorize(creds)

# 2️⃣ Apri il file Google Sheet
SHEET_NAME = "Euro Area-ECB Forecast"   # cambia con il nome del tuo file
WORKSHEET = "ECB Excel Forecast"        # cambia con il nome del tab dentro il file

sheet = client.open(SHEET_NAME).worksheet(WORKSHEET)

# 3️⃣ Leggi i dati
data = pd.DataFrame(sheet.get_all_records())

# 4️⃣ Mostra i dati
st.success("Connessione avvenuta con successo ✅")
st.write("Ecco le prime righe del tuo foglio:")
st.dataframe(data.head())
