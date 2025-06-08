import streamlit as st

def create_tabs(selected_season, ausgewählte_saisons):
    tab_names = [
        "📈 Game-Overview",
        "📊 KPIs",
        "📘 Gameplan",
        "🎯 Chancen",
        "🥅 Tore",
        "📥 Zone-Entries",
    ]
    if selected_season != "Divers":
        tab_names.append("🧍‍♂️ Player Data")
    tab_names.append("🗺️ Shotmaps")
    if "Divers" not in ausgewählte_saisons:
        tab_names.append("📅 Saisonübersicht")

    tabs = st.tabs(tab_names)
    return tab_names, tabs
