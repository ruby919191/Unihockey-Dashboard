import streamlit as st
from src.analysis.gameplan_kpi_summary import generate_kpi_summary

def get_box_color(metrik: str, wert) -> str:
    """Bestimmt die Hintergrundfarbe für eine KPI-Box."""
    # Default grau
    color = "#f5f5f5"

    # For vs Against
    if "Tigers" in metrik:
        color = "#d4edda"  # hellgrün
    elif "Gegner" in metrik:
        color = "#f8d7da"  # hellrot

    # Differenzen -> grün oder rot
    if "Differenz" in metrik:
        try:
            val = int(str(wert).replace("+", "").replace("%", ""))
            color = "#d4edda" if val >= 0 else "#f8d7da"
        except:
            pass

    # Prozentwerte neutral
    if "%" in str(wert):
        color = "#e2e3e5"

    return color


def render_kpi_tab(df, team_for_name, team_against_name):
    st.subheader("📌 KPI Übersicht")

    # KPIs laden
    df_kpis, kategorien = generate_kpi_summary(df, team_for_name, team_against_name)

    # Dropdown
    auswahl = st.selectbox("🔎 Wähle eine KPI-Kategorie:", list(kategorien.keys()))

    # Boxen rendern
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
