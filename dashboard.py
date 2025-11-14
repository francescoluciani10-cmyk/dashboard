import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === CONFIGURAZIONE PAGINA ===
st.set_page_config(
    page_title="GDP Europa Dashboard",
    page_icon="📊",
    layout="wide"
)

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
    st.error("❌ File google.json non trovato in nessuno dei percorsi definiti!")
    st.stop()

# === CONNESSIONE A GOOGLE SHEETS ===
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

@st.cache_data(ttl=300)
def load_data_from_sheets():
    try:
        creds = Credentials.from_service_account_file(JSON_FILE, scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET)
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if df.columns[0] != "Year":
            df.rename(columns={df.columns[0]: "Year"}, inplace=True)
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {str(e)}")
        return None

# === HEADER ===
st.title("📊 Dashboard GDP Paesi Europei")
st.markdown("---")

# === CARICAMENTO DATI ===
with st.spinner("⏳ Caricamento dati da Google Sheets..."):
    df = load_data_from_sheets()

if df is None or df.empty:
    st.error("❌ Impossibile caricare i dati!")
    st.stop()

st.success(f"✅ Dati caricati con successo: {len(df)} anni e {len(df.columns)-1} paesi")

# === SIDEBAR ===
st.sidebar.header("🎛️ Filtri")
available_countries = [col for col in df.columns if col != "Year"]

selected_countries = st.sidebar.multiselect(
    "Seleziona i paesi:",
    options=available_countries,
    default=["Euro area", "Italy", "Germany", "France"] if all(c in available_countries for c in ["Euro area", "Italy", "Germany", "France"]) else available_countries[:4]
)

year_range = st.sidebar.slider(
    "Seleziona range di anni:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(int(df["Year"].min()), int(df["Year"].max()))
)

df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# === SEZIONE DATI ===
st.header("📋 Visualizzazione Dati")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Prime 10 righe")
    st.dataframe(df_filtered.head(10), height=400)

with col2:
    st.subheader("Statistiche descrittive")
    if selected_countries:
        st.dataframe(df_filtered[selected_countries].describe(), height=400)
    else:
        st.warning("⚠️ Seleziona almeno un paese")

# === GRAFICO A BARRE ===
st.markdown("---")
st.header("📊 Grafico a Barre - Crescita PIL")
if selected_countries:
    fig1, ax1 = plt.subplots(figsize=(14, 7))
    x = range(len(df_filtered))
    width = 0.8 / len(selected_countries)
    colors = plt.cm.Set3(range(len(selected_countries)))
    for idx, country in enumerate(selected_countries):
        offset = (idx - len(selected_countries)/2) * width + width/2
        ax1.bar([i + offset for i in x], df_filtered[country], width, label=country, alpha=0.85, color=colors[idx])
    ax1.set_xlabel("Anno")
    ax1.set_ylabel("PIL (%)")
    ax1.set_title(f"Crescita del PIL ({year_range[0]}-{year_range[1]})")
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_filtered["Year"].astype(int), rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.axhline(0, color='black', linewidth=0.8)
    st.pyplot(fig1)
else:
    st.warning("⚠️ Seleziona almeno un paese")

# === GRAFICO A LINEE ===
st.markdown("---")
st.header("📈 Grafico a Linee - Andamento Temporale")
if selected_countries:
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    for country in selected_countries:
        ax2.plot(df_filtered["Year"], df_filtered[country], marker='o', linewidth=2.5, markersize=5, label=country)
    ax2.set_xlabel("Anno")
    ax2.set_ylabel("PIL (%)")
    ax2.set_title(f"Andamento PIL ({year_range[0]}-{year_range[1]})")
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.axhline(0, color='black', linewidth=0.8)
    st.pyplot(fig2)
else:
    st.warning("⚠️ Seleziona almeno un paese")

# === HEATMAP ===
st.markdown("---")
st.header("🔥 Heatmap - Confronto Completo")
if selected_countries:
    fig3, ax3 = plt.subplots(figsize=(14, max(6, len(selected_countries)*0.5)))
    heatmap_data = df_filtered.set_index("Year")[selected_countries].T
    sns.heatmap(
        heatmap_data,
        annot=True if len(df_filtered) <= 15 else False,
        fmt=".1f",
        cmap="RdYlGn",
        center=0,
        cbar_kws={'label': 'PIL (%)'},
        ax=ax3,
        linewidths=0.5
    )
    ax3.set_title(f"Heatmap PIL ({year_range[0]}-{year_range[1]})")
    ax3.set_xlabel("Anno")
    ax3.set_ylabel("Paese")
    st.pyplot(fig3)
else:
    st.warning("⚠️ Seleziona almeno un paese")

# === STATISTICHE PER PAESE ===
st.markdown("---")
st.header("📊 Statistiche Dettagliate per Paese")
if selected_countries:
    stats_data = []
    for country in selected_countries:
        country_data = df_filtered[country].dropna()
        if len(country_data) > 0:
            max_idx = country_data.idxmax()
            min_idx = country_data.idxmin()
            max_year = df_filtered.loc[max_idx, "Year"] if max_idx in df_filtered.index else "N/A"
            min_year = df_filtered.loc[min_idx, "Year"] if min_idx in df_filtered.index else "N/A"
            stats_data.append({
                "Paese": country,
                "Media (%)": f"{country_data.mean():.2f}",
                "Max (%)": f"{country_data.max():.2f} ({int(max_year) if max_year != 'N/A' else 'N/A'})",
                "Min (%)": f"{country_data.min():.2f} ({int(min_year) if min_year != 'N/A' else 'N/A'})",
                "Dev. Std.": f"{country_data.std():.2f}"
            })
    if stats_data:
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, height=300)

# === DOWNLOAD DATI ===
st.markdown("---")
st.header("💾 Download Dati")
if selected_countries:
    csv = df_filtered[["Year"] + selected_countries].to_csv(index=False)
    st.download_button(
        label="📥 Scarica dati filtrati (CSV)",
        data=csv,
        file_name=f"gdp_data_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv"
    )

# === FOOTER ===
st.markdown("---")
st.caption(f"📅 Ultimo aggiornamento: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
st.caption("💡 Usa i filtri nella sidebar per personalizzare la visualizzazione")
