import streamlit as st
from src.analysis.season_summary import calculate_season_summary

def render_season_summary_tab(all_df, ausgewählte_saisons):
    st.subheader("📅 Saisonübersicht")
    
    if not ausgewählte_saisons:
        st.info("Bitte mindestens eine Saison auswählen.")
        return

    season_summary_df = calculate_season_summary(all_df[all_df["season"].isin(ausgewählte_saisons)])
    st.dataframe(season_summary_df, use_container_width=True)
