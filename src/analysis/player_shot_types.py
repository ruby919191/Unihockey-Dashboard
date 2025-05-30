import pandas as pd

def get_shot_types_by_player(df):
    """
    Gibt eine Pivot-Tabelle zurück:
    Spieler x Schussart mit Anzahl pro Schussart als Spalte.
    """
    # Nur relevante Zeilen
    shots = df.dropna(subset=["Spieler Tigers", "Schusslabels"])

    # Gruppieren und zählen
    grouped = (
        shots.groupby(["Spieler Tigers", "Schusslabels"])
        .size()
        .reset_index(name="Anzahl")
    )

    # Pivot-Tabelle
    pivot = grouped.pivot_table(
        index="Spieler Tigers",
        columns="Schusslabels",
        values="Anzahl",
        fill_value=0
    ).reset_index()

    # Optional: Spalten sortieren (Schusslabels alphabetisch, Spieler bleibt vorne)
    cols = ["Spieler Tigers"] + sorted([col for col in pivot.columns if col != "Spieler Tigers"])
    return pivot[cols].rename(columns={"Spieler Tigers": "Spieler"})
