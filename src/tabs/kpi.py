import pandas as pd
import streamlit as st
from src.analysis.gameplan_kpi_summary import generate_kpi_summary, generate_spielphasen_summary


def get_box_color(metrik: str, wert) -> str:
    """Bestimmt die Hintergrundfarbe für eine KPI-Box (ohne Median-Logik)."""
    color = "#f5f5f5"

    # Standard-Logik für For vs Against
    if "Tigers" in metrik and "Total" in metrik:
        color = "#d4edda"
    elif "Gegner" in metrik and "Total" in metrik:
        color = "#f8d7da"

    # Differenz → grün oder rot
    if "Differenz" in metrik:
        try:
            val = int(str(wert).replace("+", "").replace("%", ""))
            color = "#d4edda" if val >= 0 else "#f8d7da"
        except:
            pass

    # Good / Bad %
    if "Good %" in metrik:
        color = "#c3e6cb"
    if "Bad %" in metrik:
        color = "#f5c6cb"

    # Neutrale Prozentwerte
    if "%" in str(wert) and all(x not in metrik for x in ["Good %", "Bad %", "Differenz"]):
        color = "#e2e3e5"

    return color


def render_kpi_tab(df, team_for_name, team_against_name):
    st.subheader("📌 KPI Übersicht")

    # Daten laden
    df_kpis, kategorien = generate_kpi_summary(df, team_for_name, team_against_name)
    df_spielphasen, kategorien_spielphasen = generate_spielphasen_summary(df, team_for_name, team_against_name)

    # Auswahlblock
    auswahl_block = st.selectbox("🔎 Wähle KPI-Block:", ["KPI Übersicht", "Spielphasen"])

    if auswahl_block == "KPI Übersicht":
        auswahl = st.selectbox("📊 Kategorie wählen:", list(kategorien.keys()))
        for metr, wert in kategorien[auswahl]:
            color = get_box_color(metr, wert)
            st.markdown(
                f"""
                <div style="padding:12px; margin-bottom:10px; border-radius:10px;
                            background-color:{color}; box-shadow:1px 1px 5px rgba(0,0,0,0.1)">
                    <strong>{metr}</strong><br>
                    <span style="font-size:20px;">{wert}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif auswahl_block == "Spielphasen":
        unterkategorie = st.radio("⚙️ Spielphase wählen:", list(kategorien_spielphasen.keys()), horizontal=False)
        for metr, wert in kategorien_spielphasen[unterkategorie]:
            color = get_box_color(metr, wert)
            st.markdown(
                f"""
                <div style="padding:12px; margin-bottom:10px; border-radius:10px;
                            background-color:{color}; box-shadow:1px 1px 5px rgba(0,0,0,0.1)">
                    <strong>{metr}</strong><br>
                    <span style="font-size:20px;">{wert}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
