# dashboard/app.py

import streamlit as st
import os
import sys
from PIL import Image

# 📦 Projektpfad ergänzen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📥 Tabs importieren
from src.tabs.game_overview import render_game_overview_tab
from src.tabs.kpi import render_kpi_tab
from src.tabs.gameplan import render_gameplan_tab
from src.tabs.chancen import render_chancen_tab
from src.tabs.tore import render_tore_tab
from src.tabs.zone_entries import render_zone_entries_tab
from src.tabs.player_data import render_player_data_tab
from src.tabs.shotmaps import render_shotmaps_tab
from src.tabs.season_summary import render_season_summary_tab

# 🔧 Utils
from src.utils.data_handling import load_and_filter_data
from src.utils.team_utils import determine_team_names
from src.utils.render_tabs import render_all_tabs
from src.utils.layout import configure_layout

# 📄 Weitere Seiten
from src.pages.trend_page import render_trend_page


# 🧱 Layout konfigurieren
configure_layout()

# 🚀 Navigation in der Sidebar
seitenwahl = st.sidebar.radio("Navigation", [
    "📊 Dashboard",
    "📈 Trend-Analyse",
    
])

# 📥 Daten laden und filtern
all_df, df, ausgewählte_saisons, selected_game, selected_season = load_and_filter_data()

# 🧠 Teamnamen ermitteln
team_for_name, team_against_name = determine_team_names(df, selected_season)

# 🔁 Seitenauswahl ausführen
if seitenwahl == "📊 Dashboard":
    render_all_tabs(
        df=df,
        all_df=all_df,
        selected_game=selected_game,
        selected_season=selected_season,
        ausgewählte_saisons=ausgewählte_saisons,
        team_for_name=team_for_name,
        team_against_name=team_against_name
    )
elif seitenwahl == "📈 Trend-Analyse":
    render_trend_page(all_df)

