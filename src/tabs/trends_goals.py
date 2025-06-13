import pandas as pd
import streamlit as st
import plotly.express as px
import re

# --- 1. Filterfunktion ---
def filter_goal_rows(df: pd.DataFrame, team_name: str = "Tigers") -> pd.DataFrame:
    df = df.copy()
    pattern = r"Tor (Tigers|Gegner):"
    df = df[df["Action"].astype(str).str.contains("Tor", na=False)]

    def clean_first_value(val):
        if isinstance(val, str):
            return val.split(",")[0].strip()
        return val

    for col in ["Taktische Spielsituation", "Nummerische Spielsituation", "Schusslabels"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_first_value)

    def extract_richtung(row):
        action = row["Action"]
        if "team_for" in df.columns and "team_against" in df.columns:
            team_for = row.get("team_for", "")
            team_against = row.get("team_against", "")
            if f"Tor {team_for}" in action:
                return "For"
            elif f"Tor {team_against}" in action:
                return "Against"
        else:
            if f"Tor {team_name}" in action:
                return "For"
            elif "Tor Gegner" in action:
                return "Against"
        return "Unknown"

    df["Richtung"] = df.apply(extract_richtung, axis=1)
    return df

# --- 2. Plotfunktionen ---
def plot_goals_by_tactical_situation(df):
    if "Taktische Spielsituation" not in df.columns:
        st.warning("Spalte 'Taktische Spielsituation' fehlt.")
        return
    grouped = df.groupby(["Taktische Spielsituation", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Taktische Spielsituation", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)

def plot_goals_by_numeric_situation(df):
    if "Nummerische Spielsituation" not in df.columns:
        st.warning("Spalte 'Nummerische Spielsituation' fehlt.")
        return
    grouped = df.groupby(["Nummerische Spielsituation", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Nummerische Spielsituation", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)

def plot_goals_by_shot_label(df):
    if "Schusslabels" not in df.columns:
        st.warning("Spalte 'Schusslabels' fehlt.")
        return
    grouped = df.groupby(["Schusslabels", "Richtung"]).size().reset_index(name="Anzahl")
    fig = px.bar(grouped, x="Schusslabels", y="Anzahl", color="Richtung", barmode="group", text="Anzahl")
    st.plotly_chart(fig, use_container_width=True)
