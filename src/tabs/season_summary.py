import streamlit as st
import pandas as pd
from src.analysis.season_summary import calculate_season_summary

def render_season_summary_tab(all_df, ausgewählte_saisons):
    st.subheader("📅 Saisonübersicht")
    
    if not ausgewählte_saisons:
        st.info("Bitte mindestens eine Saison auswählen.")
        return

    # Zusammenfassung berechnen
    season_summary_df = calculate_season_summary(all_df[all_df["season"].isin(ausgewählte_saisons)])

    # Saison-Vergleich auswählen
    seasons_to_compare = st.multiselect(
        "📌 Wähle Saisons für den Vergleich:",
        season_summary_df["season"].unique().tolist(),
        default=season_summary_df["season"].unique().tolist()[-2:]  # Standard letzte 2
    )

    # Prüfen ob Vergleich möglich ist
    if len(seasons_to_compare) == 0:
        st.info("Bitte mindestens eine Saison auswählen.")
        return
    elif len(seasons_to_compare) == 1:
        latest = season_summary_df[season_summary_df["season"] == seasons_to_compare[0]].iloc[0]
        prev = None
    elif len(seasons_to_compare) == 2:
        # immer chronologisch sortieren
        selected = season_summary_df[season_summary_df["season"].isin(seasons_to_compare)].sort_values(
            "season", key=lambda x: x.str[:4].astype(int)
        )
        prev, latest = selected.iloc[0], selected.iloc[1]
    else:
        st.warning("Bitte genau zwei Saisons für den Vergleich auswählen.")
        return

    st.markdown(f"### 📊 Saison {latest['season']}")

    # Nur Median-Spalten ohne Δ%-Spalten
    metric_cols = [
        col for col in season_summary_df.columns 
        if "Median" in col and "Δ%" not in col
    ]

    # In Reihen von max. 4 Spalten anzeigen
    for i in range(0, len(metric_cols), 4):
        cols = st.columns(4)
        for j, col in enumerate(metric_cols[i:i+4]):
            value = latest[col]
            delta = None
            if prev is not None:
                prev_val = prev[col]
                if prev_val != 0 and not pd.isna(prev_val):
                    delta_val = ((value - prev_val) / prev_val) * 100
                    delta = f"{delta_val:+.1f} %"
            with cols[j]:
                # Prozentwerte formatieren
                if "Corsi" in col or "Fenwick" in col or "%" in col:
                    st.metric(col, f"{value:.1%}", delta=delta)
                else:
                    st.metric(col, int(value), delta=delta)
