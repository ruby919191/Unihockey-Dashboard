import streamlit as st
import pandas as pd




from src.tabs.trends_events import (
    render_aggregated_event_summary,
    render_total_event_bar,
    render_median_events_per_game,
    render_event_win_correlation,
    add_goal_and_event_columns
)
from src.tabs.trends_chances import (
    filter_chance_rows,
    plot_chances_by_tactical_situation,
    plot_chances_by_shot_label,
    plot_chances_by_shot_metric,
    plot_chances_by_period,
    plot_chances_by_xg
)
from src.tabs.trends_goals import (
    filter_goal_rows,
    plot_goals_by_tactical_situation,
    plot_goals_by_numeric_situation,
    plot_goals_by_shot_label
)

from src.utils.team_utils import determine_team_names


def render_trends_page(all_df):
    st.header("📈 Trend-Analyse")

    ligas = [
        "SSL",
        "Fliiga",
        "L-UPL",
        "Superliga",
        "International Men",
        "International Women"
    ]
    selected_ligas = st.multiselect("Ligen auswählen:", ligas, default=["L-UPL"])

    # Filterlogik lokal in der Datei
    if "L-UPL" in selected_ligas:
        filtered_df = all_df[(all_df["season"] != "Divers") | (all_df["league"] == "L-UPL")]
        other_ligas = [liga for liga in selected_ligas if liga != "L-UPL"]
        if other_ligas:
            filtered_df = pd.concat([
                filtered_df,
                all_df[all_df["league"].isin(other_ligas)]
            ]).drop_duplicates()
    else:
        filtered_df = all_df[all_df["league"].isin(selected_ligas)]

    st.write(f"Gefilterte Daten: {len(filtered_df)} Zeilen")

    if filtered_df.empty:
        st.warning("Keine Daten für die gewählten Ligen verfügbar.")
        return

    filtered_df = add_goal_and_event_columns(filtered_df)
    team_for_name, _ = determine_team_names(filtered_df, selected_ligas[0])

    # Tabs
    tabs = st.tabs(["📊 Events", "🎯 Chancen", "🥅 Tore"])

    with tabs[0]:
        st.subheader("📊 Aggregierte Events Übersicht")
        render_aggregated_event_summary(filtered_df)

        st.subheader("📦 Total Events Balken")
        render_total_event_bar(filtered_df)

        st.subheader("📊 Median Events pro Spiel")
        render_median_events_per_game (filtered_df)


        st.subheader("📈 Einfluss der Eventanzahl auf Sieg/Niederlage")
        render_event_win_correlation(filtered_df)

        st.markdown(
        "Die Analyse prüft, ob eine hohe Anzahl an Events (Chancen, ZOE etc.) "
        "mit einem Sieg korreliert. Dafür wird der Median aller Event-Zahlen als Schwelle verwendet. "
        "Spiele mit mehr Events als der Median werden analysiert – und es wird berechnet, "
        "wie häufig in diesen Spielen gewonnen wurde."
)


    with tabs[1]:
        st.subheader("🎯 Chancenanalyse")
        chance_df = filter_chance_rows(filtered_df)

        plot_chances_by_tactical_situation(chance_df)
        plot_chances_by_shot_label(chance_df)
        plot_chances_by_shot_metric(chance_df)
        plot_chances_by_period(chance_df)
        plot_chances_by_xg(chance_df)

    with tabs[2]:
        st.subheader("🥅 Toreanalyse")
        goals_df = filter_goal_rows(filtered_df, team_name=team_for_name)

        plot_goals_by_tactical_situation(goals_df)
        plot_goals_by_numeric_situation(goals_df)
        plot_goals_by_shot_label(goals_df)
