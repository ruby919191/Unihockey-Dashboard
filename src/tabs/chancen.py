import streamlit as st
from src.analysis.chances_for import (
    count_chances_by_quality as chances_for_quality,
    count_chances_by_line as chances_for_line,
    count_chances_by_period as chances_for_period,
    count_chances_by_tactical_situation_detailed as chances_for_tactics
)
from src.analysis.chances_against import (
    count_chances_by_quality as chances_against_quality,
    count_chances_by_line as chances_against_line,
    count_chances_by_period as chances_against_period,
    count_chances_by_tactical_situation_detailed as chances_against_tactics
)

def render_chancen_tab(df, team_for_name, team_against_name):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🟢 Chancen {team_for_name}")
        st.dataframe(chances_for_quality(df), use_container_width=True)
    with col2:
        st.subheader(f"🔴 Chancen {team_against_name}")
        st.dataframe(chances_against_quality(df), use_container_width=True)

    st.subheader(f"📊 Chancen nach Linie (For - {team_for_name})")
    st.dataframe(chances_for_line(df), use_container_width=True)

    st.subheader(f"📊 Chancen nach Linie (Against - {team_against_name})")
    st.dataframe(chances_against_line(df), use_container_width=True)

    st.subheader(f"📊 Chancen pro Drittel (For - {team_for_name})")
    st.dataframe(chances_for_period(df), use_container_width=True)

    st.subheader(f"📊 Chancen pro Drittel (Against - {team_against_name})")
    st.dataframe(chances_against_period(df), use_container_width=True)

    st.subheader(f"📋 Chancen For nach Taktik (5:5 - {team_for_name})")
    st.dataframe(chances_for_tactics(df), use_container_width=True)

    st.subheader(f"📋 Chancen Against nach Taktik (5:5 - {team_against_name})")
    st.dataframe(chances_against_tactics(df), use_container_width=True)
