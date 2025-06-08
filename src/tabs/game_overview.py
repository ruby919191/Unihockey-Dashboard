import streamlit as st
from src.analysis.gameoverview import (
    get_goals_by_team, get_goals_per_period, get_chances_and_xg,
    get_corsi_fenwick_percentage
)

def styled_score_box(team_name, score, is_winner):
    color = "#d4edda" if is_winner else "#f8d7da"
    return f"""
    <div style="
        background-color: {color};
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        font-size: 64px;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
        margin: 10px;
    ">
        <div style="font-size: 24px; margin-bottom: 10px;">{team_name}</div>
        {score}
    </div>
    """

def stat_card(title, value, color="#343a40"):
    return f"""
    <div style="
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        font-weight: 600;
        color: {color};
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
    ">
        <div style="font-size: 16px; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 28px;">{value}</div>
    </div>
    """

def render_game_overview_tab(df, selected_game, team_for_name, team_against_name):
    st.header("Game Overview")

    df_game = df[df["game"] == selected_game]

    goals_team1, goals_team2 = get_goals_by_team(df_game, team_for_name, team_against_name)

    col1, col2 = st.columns(2)
    with col1:
        is_winner = goals_team1 > goals_team2
        st.markdown(styled_score_box(team_for_name, goals_team1, is_winner), unsafe_allow_html=True)
    with col2:
        is_winner = goals_team2 > goals_team1
        st.markdown(styled_score_box(team_against_name, goals_team2, is_winner), unsafe_allow_html=True)

    goals_per_period_str = get_goals_per_period(df_game, team_for_name, team_against_name)
    st.markdown(f"""
    <div style='font-size: 20px; margin-top: 20px; font-weight: 600; text-align: center;'>
        Tore pro Drittel: <span style='color:#007bff;'>{goals_per_period_str}</span><br>
        <span style='font-size: 14px; font-weight: normal; color: gray;'>
            Die erste Zahl ist immer {team_for_name} (For).
        </span>
    </div>
    """, unsafe_allow_html=True)

    chances_team1, chances_team2, xg_team1, xg_team2 = get_chances_and_xg(df_game)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(stat_card(f"Gesamt-Chancen {team_for_name}", chances_team1), unsafe_allow_html=True)
    with col2:
        st.markdown(stat_card(f"Gesamt-Chancen {team_against_name}", chances_team2), unsafe_allow_html=True)
    with col3:
        st.markdown(stat_card(f"Gesamtes xG {team_for_name}", xg_team1), unsafe_allow_html=True)
    with col4:
        st.markdown(stat_card(f"Gesamtes xG {team_against_name}", xg_team2), unsafe_allow_html=True)

    corsi_pct, fenwick_pct = get_corsi_fenwick_percentage(df_game)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(stat_card("Corsi %", f"{corsi_pct if corsi_pct is not None else 'N/A'} %"), unsafe_allow_html=True)
    with col2:
        st.markdown(stat_card("Fenwick %", f"{fenwick_pct if fenwick_pct is not None else 'N/A'} %"), unsafe_allow_html=True)
