import streamlit as st
from src.analysis.player_chances_for import get_chances_by_player
from src.analysis.player_chances_by_tactics import count_player_chances_by_tactics
from src.analysis.player_chances_by_high_mid import get_high_mid_chances_by_player
from src.analysis.player_shot_types import get_shot_types_by_player
from src.analysis.player_pass_data import get_player_pass_participation

def render_player_data_tab(df, team_for_name):
    st.subheader(f"🎯 Chancen pro Spieler - {team_for_name}")
    st.dataframe(get_chances_by_player(df), use_container_width=True)

    st.subheader(f"🧠 Taktische Situationen - {team_for_name}")
    st.dataframe(count_player_chances_by_tactics(df), use_container_width=True)

    st.subheader(f"📐 High/Mid Q Chancen - {team_for_name}")
    st.dataframe(get_high_mid_chances_by_player(df), use_container_width=True)

    st.subheader(f"🥍 Schusstypen pro Spieler - {team_for_name}")
    st.dataframe(get_shot_types_by_player(df), use_container_width=True)

    st.subheader(f"🤝 Spielerbeteiligung bei Chancen - {team_for_name}")
    st.dataframe(get_player_pass_participation(df), use_container_width=True)
