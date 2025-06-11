import streamlit as st
import pandas as pd
import os
import re

def format_saison_label(saison: str) -> str:
    if saison == "Divers":
        return "📂 Archiv / Divers"
    if "-" in saison:
        parts = saison.split("-")
        return f"Saison {parts[0]}/{parts[1]}"
    return saison

def format_game_display_name(game_id: str, saison: str) -> str:
    if saison == "Divers":
        match = re.match(r"(\d{4}-\d{2}-\d{2})_([A-Za-zÄÖÜäöüß]+)_vs_([A-Za-zÄÖÜäöüß]+)", game_id)
        if match:
            datum, team1, team2 = match.groups()
            return f"{datum} {team1} vs {team2}"
    else:
        match = re.match(r"(\d{4}-\d{2}-\d{2})_vs_([A-Za-zÄÖÜäöüß]+)", game_id)
        if match:
            datum, gegner = match.groups()
            return f"{datum} Tigers vs {gegner}"
    return game_id

def apply_filters(all_df: pd.DataFrame):
    preselected_season = st.query_params.get("season", None)
    preselected_game = st.query_params.get("game", None)
    direct_link_mode = preselected_season is not None and preselected_game is not None

    verfügbare_saisons = sorted(all_df["season"].unique())
    saison_ohne_divers = [s for s in verfügbare_saisons if s != "Divers"]
    fallback_saison = [saison_ohne_divers[-1]] if saison_ohne_divers else verfügbare_saisons[-1:]
    default_saison = [preselected_season] if preselected_season in verfügbare_saisons else fallback_saison

    saison_label_map = {s: format_saison_label(s) for s in verfügbare_saisons}
    label_to_saison = {v: k for k, v in saison_label_map.items()}

    if direct_link_mode:
        ausgewählte_saisons = [preselected_season]
        unterordner = (
            sorted(all_df.loc[all_df["season"] == "Divers", "subfolder"].unique())
            if preselected_season == "Divers"
            else []
        )
    else:
        ausgewählte_labels = st.sidebar.multiselect(
            "📁 Saisons filtern:",
            list(label_to_saison.keys()),
            default=[saison_label_map[s] for s in default_saison if s in saison_label_map]
        )
        ausgewählte_saisons = [label_to_saison[l] for l in ausgewählte_labels]

        unterordner = []
        if "Divers" in ausgewählte_saisons:
            alle_unterordner = sorted(all_df.loc[all_df["season"] == "Divers", "subfolder"].unique())
            unterordner = st.sidebar.multiselect(
                "📂 Unterordner in 'Divers' wählen:",
                alle_unterordner,
                default=alle_unterordner
            )

    filter_saisons = [s for s in ausgewählte_saisons if s != "Divers"]
    if unterordner:
        gefiltert = all_df[
            (all_df["season"].isin(filter_saisons)) |
            ((all_df["season"] == "Divers") & (all_df["subfolder"].isin(unterordner)))
        ]
    else:
        gefiltert = all_df[all_df["season"].isin(ausgewählte_saisons)]

    spiel_ids = sorted(gefiltert["game"].unique())
    saison = ausgewählte_saisons[0] if len(ausgewählte_saisons) == 1 else (gefiltert["season"].mode().iloc[0] if not gefiltert.empty else None)
    spiel_label_map = {g: format_game_display_name(g, saison) for g in spiel_ids}
    label_to_game = {v: k for k, v in spiel_label_map.items()}
    spiel_labels = list(label_to_game.keys())

    if direct_link_mode:
        auswahl = [preselected_game] if preselected_game in spiel_ids else []
    else:
        default_label = (
            [spiel_label_map[preselected_game]] if preselected_game in spiel_label_map else spiel_labels[:1]
        )
        ausgewählte_labels = st.sidebar.multiselect(
            "🎯 Spiele auswählen:",
            spiel_labels,
            default=default_label
        )
        auswahl = [label_to_game[l] for l in ausgewählte_labels]

    df = gefiltert[gefiltert["game"].isin(auswahl)] if auswahl else gefiltert

    if len(auswahl) == 1:
        selected_game = auswahl[0]
        selected_season = df.loc[df["game"] == selected_game, "season"].iloc[0]
    else:
        selected_game, selected_season = None, None

    if direct_link_mode:
        st.sidebar.empty()  # 🔒 Verstecke Sidebar bei Direktlink

    return df, ausgewählte_saisons, selected_game, selected_season