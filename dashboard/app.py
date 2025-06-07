import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image

# 📦 Projektpfad ergänzen, damit 'src' gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📥 Daten
from src.data_loader import get_all_games

# 📊 Gameplan & KPIs
from src.analysis.gameplan_kpi_summary import generate_kpi_summary
from src.analysis.gameplan_corsi_fenwick import calculate_corsi_fenwick
from src.analysis.gameplan_momentum import calculate_momentum_by_game
from src.analysis.gameplan_save_percentage import calculate_save_percentages

# 🎯 Chancen
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

# 🧍‍♂️ Spieler
from src.analysis.player_chances_for import get_chances_by_player
from src.analysis.player_chances_by_tactics import count_player_chances_by_tactics
from src.analysis.player_chances_by_high_mid import get_high_mid_chances_by_player
from src.analysis.player_shot_types import get_shot_types_by_player
from src.analysis.player_zone_entries_for import get_player_zone_entries
from src.analysis.player_pass_data import get_player_pass_participation

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

# 📅 Saisonübersicht (Season Summary)
from src.analysis.season_summary import calculate_season_summary

# 🗺️ Shotmaps Helper
def show_shotmaps(game_id: str, saison: str):
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.abspath(os.path.join(base_path, ".."))
    shotmap_dir = os.path.join(base_path, "assets", "shotmaps", saison)

    st.subheader("📊 Shotmaps")

    if not os.path.exists(shotmap_dir):
        st.error(f"❌ Verzeichnis existiert nicht: {shotmap_dir}")
        return

    try:
        all_files = os.listdir(shotmap_dir)
    except Exception as e:
        st.error(f"Fehler beim Lesen des Ordners: {e}")
        return

    labels = ["Chances_For", "Chances_Against", "Tore_For", "Tore_Against"]
    cols = st.columns(2)
    images_found = False

    for i, label in enumerate(labels):
        pattern_prefix = f"{game_id}_"
        pattern_suffix = f"_{label}.jpg"

        matched_files = [
            file for file in all_files
            if file.startswith(pattern_prefix) and file.endswith(pattern_suffix)
        ]

        if matched_files:
            image_path = os.path.join(shotmap_dir, matched_files[0])
            try:
                image = Image.open(image_path)
                cols[i % 2].image(image, caption=label.replace("_", " "), use_container_width=True)
                images_found = True
            except Exception as e:
                cols[i % 2].error(f"Fehler beim Laden von {matched_files[0]}: {e}")

    if not images_found:
        st.info("Keine Shotmap-Bilder gefunden. Bitte Game-ID und Dateinamen prüfen.")

# =============================
# Streamlit Setup
# =============================
st.set_page_config(page_title="🏑 Unihockey Dashboard", layout="wide")
st.title("🏑 Unihockey Tigers Dashboard")

# Alle Daten laden
all_df = get_all_games()

# Saison-Filter
verfügbare_saisons = sorted(all_df["season"].unique())

# Default-Auswahl: die aktuellste Saison (letztes Element im sortierten List)
default_saison = [verfügbare_saisons[-1]] if verfügbare_saisons else []

ausgewählte_saisons = st.sidebar.multiselect("📁 Saisons filtern:", verfügbare_saisons, default=default_saison)

# Unterordner-Filter nur anzeigen, wenn 'Divers' ausgewählt ist
unterordner = []
if "Divers" in ausgewählte_saisons:
    alle_unterordner = sorted(all_df.loc[all_df["season"] == "Divers", "subfolder"].unique())
    unterordner = st.sidebar.multiselect("📂 Unterordner in 'Divers' wählen:", alle_unterordner, default=alle_unterordner)

# Daten filtern nach Saison und ggf. Unterordner
filter_saisons = [s for s in ausgewählte_saisons if s != "Divers"]
if unterordner:
    gefiltert = all_df[
        (all_df["season"].isin(filter_saisons)) |
        ((all_df["season"] == "Divers") & (all_df["subfolder"].isin(unterordner)))
    ]
else:
    gefiltert = all_df[all_df["season"].isin(ausgewählte_saisons)]

# Spielauswahl
spiel_ids = sorted(gefiltert["game"].unique())
auswahl = st.sidebar.multiselect("🎯 Spiele auswählen:", spiel_ids, default=spiel_ids[:1])

# Wenn keine Spiele ausgewählt sind, alle Spiele der ausgewählten Saison(n) anzeigen
if len(auswahl) == 0:
    df = gefiltert.copy()
else:
    df = gefiltert[gefiltert["game"].isin(auswahl)]

# Für Shotmaps: genau ein Spiel erforderlich
if len(auswahl) == 1:
    selected_game = auswahl[0]
    selected_season = df.loc[df["game"] == selected_game, "season"].iloc[0]
else:
    selected_game, selected_season = None, None

# === Dynamische Teamnamen je nach Season ===
if selected_season == "Divers" and "team_for" in df.columns and "team_against" in df.columns:
    team_for_name = df["team_for"].iloc[0]
    team_against_name = df["team_against"].iloc[0]
else:
    team_for_name = "Tigers"
    team_against_name = "Gegner"

# =============================
# Tabs definieren
# =============================
tab_names = ["📊 KPIs", "📘 Gameplan", "🎯 Chancen", "🥅 Tore", "📥 Zone-Entries"]

# Player Data Tab nur anzeigen, wenn nicht Divers
if selected_season != "Divers":
    tab_names.append("🧍‍♂️ Player Data")

# Shotmaps Tab immer anzeigen
tab_names.append("🗺️ Shotmaps")

# Saisonübersicht Tab nur anzeigen, wenn nicht Divers
if not ("Divers" in ausgewählte_saisons):
    tab_names.append("📅 Saisonübersicht")

tabs = st.tabs(tab_names)

# KPIs
with tabs[tab_names.index("📊 KPIs")]:
    st.subheader("📌 KPI Übersicht")
    st.dataframe(generate_kpi_summary(df, team_for_name, team_against_name), use_container_width=True)

# Gameplan
with tabs[tab_names.index("📘 Gameplan")]:
    st.subheader("📈 Momentum pro Spiel")
    st.dataframe(calculate_momentum_by_game(df), use_container_width=True)

    st.subheader("🔁 Corsi & Fenwick")
    st.dataframe(calculate_corsi_fenwick(df), use_container_width=True)

# Chancen
with tabs[tab_names.index("🎯 Chancen")]:
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

# Tore
with tabs[tab_names.index("🥅 Tore")]:
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

# Zone Entries
with tabs[tab_names.index("📥 Zone-Entries")]:
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

# Player Data (nur anzeigen, wenn nicht Divers)
if selected_season != "Divers":
    with tabs[tab_names.index("🧍‍♂️ Player Data")]:
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

# Shotmaps Tab (immer anzeigen)
with tabs[tab_names.index("🗺️ Shotmaps")]:
    st.subheader("🗺️ Shotmaps")
    if selected_game and selected_season:
        show_shotmaps(selected_game, selected_season)
    else:
        st.warning("Bitte genau ein Spiel auswählen, um Shotmaps zu sehen.")

# Saisonübersicht Tab (nur wenn Divers nicht ausgewählt)
if "📅 Saisonübersicht" in tab_names:
    with tabs[tab_names.index("📅 Saisonübersicht")]:
        st.subheader("📅 Saisonübersicht")
        season_summary_df = calculate_season_summary(all_df[all_df["season"].isin(ausgewählte_saisons)])
        st.dataframe(season_summary_df, use_container_width=True)
