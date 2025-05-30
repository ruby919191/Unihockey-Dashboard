import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image

# 📦 Projektpfad ergänzen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📥 Daten
from src.data_loader import list_seasons, get_season_games

# 📊 Gameplan & KPIs
from src.analysis.gameplan_kpi_summary import generate_kpi_summary
from src.analysis.gameplan_corsi_fenwick import calculate_corsi_fenwick
from src.analysis.gameplan_momentum import calculate_momentum_by_game
from src.analysis.gameplan_save_percentage import calculate_save_percentages

# 🎯 Chancen
from src.analysis.chances_for import (
    count_chances_by_quality as chances_for_quality,
    count_chances_by_line as chances_for_line,
    count_chances_by_period as chances_for_period
)
from src.analysis.chances_against import (
    count_chances_by_quality as chances_against_quality,
    count_chances_by_line as chances_against_line,
    count_chances_by_period as chances_against_period
)

# 🧍‍♂️ Spieler
from src.analysis.player_chances_for import get_chances_by_player
from src.analysis.player_chances_by_tactics import count_player_chances_by_tactics
from src.analysis.player_chances_by_high_mid import get_high_mid_chances_by_player
from src.analysis.player_shot_types import get_shot_types_by_player
from src.analysis.player_zone_entries_for import get_player_zone_entries

# 📥 Zone Entries
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

# 🥅 Tore
from src.analysis.goals import (
    get_goal_situation_counts,
    get_opponent_goal_situation_counts
)

# 🗺️ Shotmaps Helper
def show_shotmaps(game_id: str, saison: str):
    shotmap_dir = os.path.join("assets", "shotmaps", saison)
    labels = ["Chances_For", "Chances_Against", "Tore_For", "Tore_Against"]
    st.subheader("📊 Shotmaps")
    cols = st.columns(2)
    for i, label in enumerate(labels):
        pattern_prefix = f"{game_id}_vs_"
        pattern_suffix = f"_{label}.jpg"
        for file in os.listdir(shotmap_dir):
            if file.startswith(pattern_prefix) and file.endswith(pattern_suffix):
                image_path = os.path.join(shotmap_dir, file)
                image = Image.open(image_path)
                cols[i % 2].image(image, caption=label.replace("_", " "), use_column_width=True)

# =============================
# Streamlit Setup
# =============================

st.set_page_config(page_title="🏑 Unihockey Dashboard", layout="wide")
st.title("🏑 Unihockey Tigers Dashboard")

# Saison & Spielauswahl
available_seasons = list_seasons()
selected_season = st.sidebar.selectbox("Saison wählen", available_seasons)
df = get_season_games(selected_season)

available_games = df["game"].unique()
selected_game = st.sidebar.selectbox("Spiel wählen", ["Alle Spiele"] + list(available_games))
if selected_game != "Alle Spiele":
    df = df[df["game"] == selected_game]

# =============================
# Tabs
# =============================
tabs = st.tabs(["📊 KPIs", "📘 Gameplan", "🎯 Chancen", "🥅 Tore", "📥 Zone-Entries", "🧍‍♂️ Player Data", "🗺️ Shotmaps"])

# KPIs
with tabs[0]:
    st.subheader("📌 KPI Übersicht")
    st.dataframe(generate_kpi_summary(df), use_container_width=True)

# Gameplan
with tabs[1]:
    st.subheader("📈 Momentum pro Spiel")
    st.dataframe(calculate_momentum_by_game(df), use_container_width=True)

    st.subheader("🔁 Corsi & Fenwick")
    st.dataframe(calculate_corsi_fenwick(df), use_container_width=True)

# Chancen
with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 Chancen For")
        st.dataframe(chances_for_quality(df), use_container_width=True)
    with col2:
        st.subheader("🔴 Chancen Against")
        st.dataframe(chances_against_quality(df), use_container_width=True)

    st.subheader("📊 Chancen nach Linie (For)")
    st.dataframe(chances_for_line(df), use_container_width=True)

    st.subheader("📊 Chancen nach Linie (Against)")
    st.dataframe(chances_against_line(df), use_container_width=True)

    st.subheader("📊 Chancen pro Drittel (For)")
    st.dataframe(chances_for_period(df), use_container_width=True)

    st.subheader("📊 Chancen pro Drittel (Against)")
    st.dataframe(chances_against_period(df), use_container_width=True)

# Tore
with tabs[3]:
    st.subheader("🟢 Tore Tigers (5:5, taktisch)")
    st.dataframe(get_goal_situation_counts(df, "Tigers"), use_container_width=True)

    st.subheader("🔴 Gegentore (5:5, taktisch)")
    st.dataframe(get_opponent_goal_situation_counts(df), use_container_width=True)

    # 📊 Save % Analyse
    st.subheader("🧤 Save % Übersicht")
    save_df = calculate_save_percentages(df)
    st.dataframe(save_df, use_container_width=True)

    # 🔍 Dynamischer Goalie-Vergleich
    if "Save % For" in save_df.columns and "Save % Against" in save_df.columns:
        sp_for = save_df["Save % For"].mean()
        sp_against = save_df["Save % Against"].mean()

        if pd.notnull(sp_for) and pd.notnull(sp_against):
            if sp_for > sp_against:
                verdict = "✅ Tigers Goalie war besser."
            elif sp_for < sp_against:
                verdict = "❌ Gegnerischer Goalie war besser."
            else:
                verdict = "🤝 Beide Goalies gleich gut."

            st.success(f"Torhütervergleich: {verdict}")
        else:
            st.info("Nicht genügend Daten für Torhütervergleich.")

# Zone Entries
with tabs[4]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📥 ZOE For")
        st.dataframe(zoe_for_quality(df), use_container_width=True)
    with col2:
        st.subheader("📤 ZOE Against")
        st.dataframe(zoe_against_quality(df), use_container_width=True)

    st.subheader("📊 ZOE nach Drittel (For)")
    st.dataframe(zoe_for_period(df), use_container_width=True)

    st.subheader("📊 ZOE nach Drittel (Against)")
    st.dataframe(zoe_against_period(df), use_container_width=True)

    st.subheader("📋 ZOE nach Linie (For)")
    st.dataframe(zoe_for_line(df), use_container_width=True)

    st.subheader("📋 ZOE nach Linie (Against)")
    st.dataframe(zoe_against_line(df), use_container_width=True)

    st.subheader("🧍‍♂️ Zonen Entries Spieleraktivität")
    st.dataframe(get_player_zone_entries(df), use_container_width=True)

# Player Data
with tabs[5]:
    st.subheader("🎯 Chancen pro Spieler")
    st.dataframe(get_chances_by_player(df), use_container_width=True)

    st.subheader("🧠 Taktische Situationen")
    st.dataframe(count_player_chances_by_tactics(df), use_container_width=True)

    st.subheader("📐 High/Mid Q Chancen")
    st.dataframe(get_high_mid_chances_by_player(df), use_container_width=True)

    st.subheader("🥍 Schusstypen pro Spieler")
    st.dataframe(get_shot_types_by_player(df), use_container_width=True)

# Shotmaps
with tabs[6]:
    if selected_game != "Alle Spiele":
        show_shotmaps(selected_game, selected_season)
    else:
        st.warning("Bitte ein einzelnes Spiel auswählen, um Shotmaps zu sehen.")
