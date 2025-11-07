import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.title("🔗 Test Connessione Google Sheets")

# --- 1️⃣ Definisci gli scope richiesti ---
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# --- 2️⃣ Autenticazione tramite secrets ---
try:
    creds = Credentials.from_service_account_info(
        st.secrets["google"], scopes=SCOPE
    )
    client = gspread.authorize(creds)

    # --- 3️⃣ Collega il foglio Google Sheets ---
    # Usa l'ID del file (dal link, la parte tra /d/ e /edit)
    SHEET_ID = "1FxfkmF_3x-YzNWsCYYr1GsgHM1pq2tuPB-CWAIk-aPw"
    WORKSHEET = "Europe Countries GDP Long Format"  # nome della linguetta in basso

    sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET)

    # --- 4️⃣ Legge i dati in un DataFrame ---
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    st.success("✅ Connessione avvenuta con successo!")
    st.dataframe(df.head())

except Exception as e:
    st.error("❌ Errore durante la connessione al foglio Google Sheets")
    st.exception(e)
