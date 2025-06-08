import streamlit as st
from src.analysis.gameplan_momentum import calculate_momentum_by_game
from src.analysis.gameplan_corsi_fenwick import calculate_corsi_fenwick

def render_gameplan_tab(df):
    st.subheader("📈 Momentum pro Spiel")
    st.dataframe(calculate_momentum_by_game(df), use_container_width=True)

    st.subheader("🔁 Corsi & Fenwick")
    st.dataframe(calculate_corsi_fenwick(df), use_container_width=True)
