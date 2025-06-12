import streamlit as st
from src.analysis.saisonverlauf import calculate_saisonverlauf_stats

def render_saisonverlauf_tab(all_df, ausgewählte_saisons):
    stats = calculate_saisonverlauf_stats(all_df, ausgewählte_saisons)

    def farbe_resultat(val):
        if val == "Sieg":
            return "background-color: #d4edda"
        elif val == "Niederlage":
            return "background-color: #f8d7da"
        else:
            return ""

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🏆 Siege", stats["siege"])
    col2.metric("⚠️ Niederlagen", stats["niederlagen"])
    col3.metric("🤝 Unentschieden", stats["unentschieden"])
    col4.metric("🎲 Anzahl Spiele", stats["anzahl_spiele"])
    col5.metric("📊 Siege %", f"{stats['siege_prozent']} %")

    st.header("🏆 Saisonverlauf")
    styled_df = stats["df_ergebnisse"].style.applymap(farbe_resultat, subset=["Resultat"])
    st.dataframe(styled_df, use_container_width=True)
