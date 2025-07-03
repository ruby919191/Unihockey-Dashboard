import streamlit as st
import matplotlib.pyplot as plt
from src.tabs.game_overview import render_game_overview_tab
from src.tabs.kpi import render_kpi_tab
from src.tabs.gameplan import render_gameplan_tab
from src.tabs.chancen import render_chancen_tab
from src.tabs.tore import render_tore_tab
from src.tabs.zone_entries import render_zone_entries_tab
from src.tabs.player_data import render_player_data_tab
from src.tabs.shotmaps import render_shotmaps_tab
from src.tabs.season_summary import render_season_summary_tab
from src.tabs.saisonverlauf import render_saisonverlauf_tab  # neu importieren

def render_all_tabs(df, all_df, selected_game, selected_season, ausgewählte_saisons, team_for_name, team_against_name):
    tab_names = [
        "📈 Game-Overview", 
        "📊 KPIs", 
        "📘 Gameplan", 
        "🎯 Chancen", 
        "🥅 Tore", 
        "📥 Zone-Entries"
    ]
    if selected_season != "Divers":
        tab_names.append("🧍‍♂️ Player Data")
    tab_names.append("🗺️ Shotmaps")
    if "Divers" not in ausgewählte_saisons:
        tab_names.append("📅 Saisonübersicht")
        tab_names.append("📅 Saisonverlauf")  # hier neu ergänzt

    tabs = st.tabs(tab_names)

    with tabs[tab_names.index("📈 Game-Overview")]:
        render_game_overview_tab(
            df,
            selected_game,
            team_for_name,
            team_against_name,
            selected_season
        )

    with tabs[tab_names.index("📊 KPIs")]:
        render_kpi_tab(df, team_for_name, team_against_name)

    with tabs[tab_names.index("📘 Gameplan")]:
        render_gameplan_tab(df)

    with tabs[tab_names.index("🎯 Chancen")]:
        render_chancen_tab(df, team_for_name, team_against_name)

    with tabs[tab_names.index("🥅 Tore")]:
        render_tore_tab(df, team_for_name, team_against_name)

    with tabs[tab_names.index("📥 Zone-Entries")]:
        render_zone_entries_tab(df, team_for_name, team_against_name)

    if selected_season != "Divers":
        with tabs[tab_names.index("🧍‍♂️ Player Data")]:
            render_player_data_tab(df, team_for_name)

    with tabs[tab_names.index("🗺️ Shotmaps")]:
        render_shotmaps_tab(selected_game, selected_season)

    if "📅 Saisonübersicht" in tab_names:
        with tabs[tab_names.index("📅 Saisonübersicht")]:
            render_season_summary_tab(all_df, ausgewählte_saisons)

    if "📅 Saisonverlauf" in tab_names:  # neu
        with tabs[tab_names.index("📅 Saisonverlauf")]:
            render_saisonverlauf_tab(all_df, ausgewählte_saisons)
