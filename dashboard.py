import streamlit as st
import pandas as pd
import plotly.express as px

# Titolo della dashboard
st.title("📈 Market Dashboard (demo)")

# Dati di esempio
data = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", periods=10),
    "Price": [100, 102, 105, 103, 107, 108, 110, 112, 115, 118]
})

# Grafico
fig = px.line(data, x="Date", y="Price", title="Andamento prezzi demo")
st.plotly_chart(fig)

st.metric("Rendimento", f"{(data['Price'].iloc[-1]/data['Price'].iloc[0]-1)*100:.2f}%")
