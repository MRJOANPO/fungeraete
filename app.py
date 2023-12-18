import streamlit as st
import requests
import pandas as pd
import time

responseCount = requests.get("https://qr.rocksolidsiegen.de/api/dashboard.php", timeout=2)
df = pd.json_normalize(responseCount.json())
df["Ausgeliehen"] = df["count_away"].astype(int)/df["total_count"].astype(int)*100
df["Auf Lager"] = 100-df["Ausgeliehen"]

st.bar_chart(df, x="dienst", y=["Auf Lager", "Ausgeliehen"], color=["#0ac247", "#1900ff"])

responseAusgeliehen = requests.get("https://qr.rocksolidsiegen.de/api/db_recent_ausgeliehen.php", timeout=2)
df_zuletzt_ausgeliehen = pd.json_normalize(responseAusgeliehen.json())
ex_zuletzt_ausgeliehen = st.expander("Zuletzt Ausgeliehen")
ex_zuletzt_ausgeliehen.dataframe(df_zuletzt_ausgeliehen)

responseZurueck = requests.get("https://qr.rocksolidsiegen.de/api/db_recent_zurueck.php", timeout=2)
df_zuletzt_zurueck = pd.json_normalize(responseZurueck.json())
ex_zuletzt_zurueck = st.expander("Zuletzt Zurueckgebracht")
ex_zuletzt_zurueck.dataframe(df_zuletzt_zurueck)

time.sleep(4)
st.rerun()