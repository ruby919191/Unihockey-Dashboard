# src/utils/filters.py

import streamlit as st
import pandas as pd

def apply_filters(all_df: pd.DataFrame):
    verfügbare_saisons = sorted(all_df["season"].unique())
    default_saison = [verfügbare_saisons[-1]] if verfügbare_saisons else []

    ausgewählte_saisons = st.sidebar.multiselect("📁 Saisons filtern:", verfügbare_saisons, default=default_saison)

    unterordner = []
    if "Divers" in ausgewählte_saisons:
        alle_unterordner = sorted(all_df.loc[all_df["season"] == "Divers", "subfolder"].unique())
        unterordner = st.sidebar.multiselect("📂 Unterordner in 'Divers' wählen:", alle_unterordner, default=alle_unterordner)

    filter_saisons = [s for s in ausgewählte_saisons if s != "Divers"]
    if unterordner:
        gefiltert = all_df[
            (all_df["season"].isin(filter_saisons)) |
            ((all_df["season"] == "Divers") & (all_df["subfolder"].isin(unterordner)))
        ]
    else:
        gefiltert = all_df[all_df["season"].isin(ausgewählte_saisons)]

    spiel_ids = sorted(gefiltert["game"].unique())
    auswahl = st.sidebar.multiselect("🎯 Spiele auswählen:", spiel_ids, default=spiel_ids[:1])

    if len(auswahl) == 0:
        df = gefiltert.copy()
    else:
        df = gefiltert[gefiltert["game"].isin(auswahl)]

    if len(auswahl) == 1:
        selected_game = auswahl[0]
        selected_season = df.loc[df["game"] == selected_game, "season"].iloc[0]
    else:
        selected_game, selected_season = None, None

    return df, ausgewählte_saisons, selected_game, selected_season
