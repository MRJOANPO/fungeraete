import streamlit as st
import requests
import pandas as pd
import time

st.header("🎄 Holy Night Funkgeräte")

responseCount = requests.get("https://qr.rocksolidsiegen.de/api/dashboard.php", timeout=1)
df = pd.json_normalize(responseCount.json())
df["Ausgeliehen"] = df["count_away"].astype(int)/df["total_count"].astype(int)*100
df["Auf Lager"] = 100-df["Ausgeliehen"]

st.bar_chart(df, x="dienst", y=["Auf Lager", "Ausgeliehen"], color=["#0ac247", "#1900ff"])
ex_zuletzt_zahlen = st.expander("Zahlen")
df.drop(columns=["Ausgeliehen", "Auf Lager"], inplace=True)
df.rename(columns={
   "dienst": "Dienst",
   "total_count": "Gesamt",
   "total_count_normal":"Normal",
   "total_count_master":"Master",
   "count_away": "Ausgeliehen (Gesamt)",
   "count_away_normal":"Ausgeliehen (Normal)",
   "count_away_master":"Ausgeliehen (Master)"
   }, inplace=True)
ex_zuletzt_zahlen.dataframe(df)

responseAusgeliehen = requests.get("https://qr.rocksolidsiegen.de/api/db_recent_ausgeliehen.php", timeout=1)
df_zuletzt_ausgeliehen = pd.json_normalize(responseAusgeliehen.json())
ex_zuletzt_ausgeliehen = st.expander("Zuletzt Ausgeliehen")
ex_zuletzt_ausgeliehen.dataframe(df_zuletzt_ausgeliehen)

responseZurueck = requests.get("https://qr.rocksolidsiegen.de/api/db_recent_zurueck.php", timeout=1)
df_zuletzt_zurueck = pd.json_normalize(responseZurueck.json())
ex_zuletzt_zurueck = st.expander("Zuletzt Zurueckgebracht")
ex_zuletzt_zurueck.dataframe(df_zuletzt_zurueck)

time.sleep(2)
st.rerun()