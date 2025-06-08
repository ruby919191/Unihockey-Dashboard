import streamlit as st
from src.analysis.gameplan_kpi_summary import generate_kpi_summary

def render_kpi_tab(df, team_for_name, team_against_name):
    st.subheader("📌 KPI Übersicht")
    st.dataframe(generate_kpi_summary(df, team_for_name, team_against_name), use_container_width=True)
