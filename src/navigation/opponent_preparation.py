import streamlit as st
import pandas as pd

def render_opponent_preparation_page(all_df):
    st.title("🎯 Gegnervorbereitung")

    # Nur reguläre Saisons (ohne Divers)
    saison_df = all_df[all_df["season"] != "Divers"]

    # Gegnerliste extrahieren aus team_against (berechnet im dataloader)
    gegner_liste = sorted(saison_df["team_against"].dropna().unique())

    # Auswahlbox in der Sidebar
    ausgewählter_gegner = st.selectbox("Wähle einen Gegner aus:", gegner_liste)

    # Wenn ein Gegner ausgewählt wurde, filtere alle Spiele gegen diesen Gegner
    if ausgewählter_gegner:
        gegner_df = saison_df[saison_df["team_against"] == ausgewählter_gegner]

        # Absicherung: season-Spalte prüfen
        if "season" not in gegner_df.columns:
            st.warning("Die Daten enthalten keine 'season'-Spalte, die Analyse ist nicht möglich.")
            return

        st.markdown(f"### Statistiken gegen **{ausgewählter_gegner}**")

        anzahl_spiele = gegner_df["game"].nunique()
        tore_tigers = gegner_df["Action"].str.startswith("Tor Tigers").sum()
        tore_gegner = gegner_df["Action"].str.startswith("Tor Gegner").sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Anzahl Spiele", anzahl_spiele)
        col2.metric("Tore Tigers", tore_tigers)
        col3.metric("Tore Gegner", tore_gegner)

        st.markdown("---")
        st.info("Weitere Analysen wie xG, Chancenverteilung, Drittelstatistik folgen hier...")
