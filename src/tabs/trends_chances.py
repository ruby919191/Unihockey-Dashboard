import pandas as pd
import streamlit as st
import plotly.express as px
import re

# --- 1. Filterfunktion ---
def filter_chance_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    pattern = r"(Low Q Chance|Mid Q Chance|High Q Chance|Pot \+ Chance) (For|Against):"
    df = df[df["Action"].astype(str).str.contains(pattern, na=False)]

    def extract_richtung(action):
        if "For" in action:
            return "For"
        elif "Against" in action:
            return "Against"
        return "Unknown"

    df["Richtung"] = df["Action"].apply(extract_richtung)
    return df

# --- 2. Plotfunktionen ---
def plot_chances_by_tactical_situation(df):
    if "Taktische Spielsituation" not in df.columns:
        st.warning("Spalte 'Taktische Spielsituation' fehlt.")
        return
    grouped = df.groupby(["Taktische Spielsituation", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Taktische Spielsituation", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)

def plot_chances_by_shot_label(df):
    if "Schusslabels" not in df.columns:
        st.warning("Spalte 'Schusslabels' fehlt.")
        return
    grouped = df.groupby(["Schusslabels", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Schusslabels", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)

def plot_chances_by_shot_metric(df):
    if "Schussmetrik" not in df.columns:
        st.warning("Spalte 'Schussmetrik' fehlt.")
        return
    grouped = df.groupby(["Schussmetrik", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Schussmetrik", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)

def plot_chances_by_period(df):
    if "Drittel" not in df.columns:
        st.warning("Spalte 'Drittel' fehlt.")
        return
    grouped = df.groupby(["Drittel", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Drittel", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)

def plot_chances_by_xg(df):
    if "XG" not in df.columns:
        st.warning("Spalte 'XG' fehlt.")
        return
    df_clean = df.dropna(subset=["XG"])
    df_clean["XG"] = pd.to_numeric(df_clean["XG"], errors="coerce")
    fig = px.histogram(df_clean, x="XG", color="Richtung", nbins=20, barmode="overlay")
    fig.update_layout(title="Verteilung der XG-Werte nach Richtung")
    st.plotly_chart(fig, use_container_width=True)