import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from src.analysis.spielsituationen import calculate_spielsituationen

def render_spielsituationen_tab(df: pd.DataFrame, selected_season: str):
    st.subheader("📘 Spielsituationen")

    # Analyse durchführen
    data = calculate_spielsituationen(df)

    if data.empty:
        st.info("Keine Spielsituationen im aktuellen Datensatz gefunden.")
        return

    # Teamnamen anpassen (bei 'Divers')
    if selected_season == "Divers":
        team_for_name = df["team_for"].iloc[0] if "team_for" in df.columns else "For"
        team_against_name = df["team_against"].iloc[0] if "team_against" in df.columns else "Against"
    else:
        team_for_name = "For"
        team_against_name = "Against"

    # Titel-Mapping für lesbare Abschnittsüberschriften
    AKTIONSTYP_TITEL = {
        "Zone-Exits": "Zone Exits",
        "Nachsetzen": "Nachsetzen",
        "Pressing": "Pressing",
        "ZOE gg. Pressing": "Zone Entry gegen Pressing"
    }

    # Pro Aktionstyp eigenen Abschnitt darstellen
    aktionstypen = data["Aktionstyp"].unique()

    for aktionstyp in aktionstypen:
        titel = AKTIONSTYP_TITEL.get(aktionstyp, aktionstyp)
        st.markdown(f"### {titel}")

        subset = data[data["Aktionstyp"] == aktionstyp].copy()

        # Tabelle
        table = pd.DataFrame({
            f"{team_for_name} Good": subset["For Good"].values,
            f"{team_for_name} Bad": subset["For Bad"].values,
            f"{team_against_name} Good": subset["Against Good"].values,
            f"{team_against_name} Bad": subset["Against Bad"].values,
        }, index=subset["Aktion"])

        st.dataframe(table, use_container_width=True)

        # Diagramm: horizontale Balken
        fig, ax = plt.subplots(figsize=(8, 2 + len(subset) * 0.6))

        y_labels = subset["Aktion"]
        y_pos = range(len(y_labels))

        # Bars For
        ax.barh(y_pos, subset["For Good"], label=f"{team_for_name} Good", color="#4CAF50")
        ax.barh(y_pos, subset["For Bad"], left=subset["For Good"], label=f"{team_for_name} Bad", color="#FFC107")

        # Bars Against (gespiegelt nach links)
        against_good_neg = -subset["Against Good"]
        against_bad_neg = -subset["Against Bad"]
        ax.barh(y_pos, against_good_neg, label=f"{team_against_name} Good", color="#2196F3")
        ax.barh(y_pos, against_bad_neg, left=against_good_neg, label=f"{team_against_name} Bad", color="#F44336")

        ax.set_yticks(y_pos)
        ax.set_yticklabels(y_labels)
        ax.set_xlabel("Anzahl")
        ax.axvline(0, color="black", linewidth=0.5)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)
        st.pyplot(fig)