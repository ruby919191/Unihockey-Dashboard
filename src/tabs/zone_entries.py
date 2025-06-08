import streamlit as st
from src.analysis.zone_entries_for import (
    count_zone_entries_by_quality as zoe_for_quality,
    count_zone_entries_by_period as zoe_for_period,
    count_zone_entries_by_line as zoe_for_line
)
from src.analysis.zone_entries_against import (
    count_zone_entries_against_by_quality as zoe_against_quality,
    count_zone_entries_against_by_period as zoe_against_period,
    count_zone_entries_against_by_line as zoe_against_line
)
from src.analysis.player_zone_entries_for import get_player_zone_entries

def render_zone_entries_tab(df, team_for_name, team_against_name):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📥 ZOE For - {team_for_name}")
        st.dataframe(zoe_for_quality(df), use_container_width=True)
    with col2:
        st.subheader(f"📤 ZOE Against - {team_against_name}")
        st.dataframe(zoe_against_quality(df), use_container_width=True)

    st.subheader(f"📊 ZOE nach Drittel (For - {team_for_name})")
    st.dataframe(zoe_for_period(df), use_container_width=True)

    st.subheader(f"📊 ZOE nach Drittel (Against - {team_against_name})")
    st.dataframe(zoe_against_period(df), use_container_width=True)

    st.subheader(f"📋 ZOE nach Linie (For - {team_for_name})")
    st.dataframe(zoe_for_line(df), use_container_width=True)

    st.subheader(f"📋 ZOE nach Linie (Against - {team_against_name})")
    st.dataframe(zoe_against_line(df), use_container_width=True)

    st.subheader("🧍‍♂️ Zonen Entries Spieleraktivität")
    st.dataframe(get_player_zone_entries(df), use_container_width=True)
