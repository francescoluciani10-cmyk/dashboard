# dashboard.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === CONFIGURAZIONE ===
SHEET_ID = "1FxfkmF_3x-YzNWsCYYr1GsgHM1pq2tuPB-CWAIk-aPw"  # ID del Google Sheet
WORKSHEET = "Europe Countries GDP"  # Nome del tab che vuoi leggere
JSON_FILE = "google.json"  # Chiave JSON del Service Account (locale e mai pubblica)

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

# === STREAMLIT ===
st.title("Dashboard Market Data")
st.write("Prime righe del dataset:")
st.dataframe(df.head())

# === ANALISI BASE ===
st.write("Statistiche descrittive:")
st.dataframe(df.describe())

# Esempio grafico: distribuzione di una colonna numerica (modifica "Price" con la tua colonna)
if "Price" in df.columns:
    st.write("Distribuzione dei prezzi:")
    fig, ax = plt.subplots()
    sns.histplot(df["Price"], kde=True, ax=ax)
    st.pyplot(fig)

# Esempio di calcolo rendimenti giornalieri (modifica "Price")
if "Price" in df.columns:
    df["Return"] = df["Price"].pct_change()
    st.write("Prime righe con rendimenti calcolati:")
    st.dataframe(df.head())

