import streamlit as st
from src.analysis.goals import (
    get_goal_situation_counts,
    get_opponent_goal_situation_counts
)
from src.analysis.gameplan_save_percentage import calculate_save_percentages

def render_tore_tab(df, team_for_name, team_against_name):
    st.subheader(f"🟢 Tore {team_for_name} (5:5, taktisch)")
    st.dataframe(get_goal_situation_counts(df, team_for_name), use_container_width=True)

    st.subheader(f"🔴 Gegentore {team_against_name} (5:5, taktisch)")
    st.dataframe(get_opponent_goal_situation_counts(df), use_container_width=True)

    st.subheader("🧤 Save Percentage")
    save_df = calculate_save_percentages(df)
    st.dataframe(save_df, use_container_width=True)

    if not save_df.empty and "Save % For" in save_df.columns and "Save % Against" in save_df.columns:
        last_game = save_df.iloc[-1]
        tigers_sv = last_game.get("Save % For", None)
        opp_sv = last_game.get("Save % Against", None)

        if tigers_sv is not None and opp_sv is not None:
            if tigers_sv > opp_sv:
                st.success(f"🟢 {team_for_name} Goalie war stärker: {tigers_sv}% vs. {opp_sv}%")
            elif tigers_sv < opp_sv:
                st.error(f"🔴 Gegnerischer Goalie war stärker: {opp_sv}% vs. {tigers_sv}%")
            else:
                st.info(f"⚖️ Gleichstand: Beide Save % bei {tigers_sv}%")
        else:
            st.warning("Nicht genügend Daten zur Save %-Analyse.")
    else:
        st.warning("Keine Save %-Daten verfügbar.")
