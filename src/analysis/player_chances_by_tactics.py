import pandas as pd

def count_player_chances_by_tactics(df):
    """
    Zählt Chancen pro Spieler pro taktischer Spielsituation.
    Gibt eine Tabelle mit Anzahl Chancen zurück, gruppiert nach Spieler Tigers und Taktische Spielsituation.
    """
    chances = df[df["Action"].str.contains("Chance For", na=False)]
    chances = chances.dropna(subset=["Spieler Tigers", "Taktische Spielsituation"])

    grouped = (
        chances.groupby(["Spieler Tigers", "Taktische Spielsituation"])
        .size()
        .reset_index(name="Anzahl Chancen")
    )

    # Pivot, damit jeder Spieler nur einmal auftritt
    pivoted = grouped.pivot_table(
        index="Spieler Tigers",
        columns="Taktische Spielsituation",
        values="Anzahl Chancen",
        fill_value=0
    ).reset_index()

    # Totalspalte
    pivoted["Total"] = pivoted.drop(columns="Spieler Tigers").sum(axis=1)

    # Nach Total sortieren
    pivoted = pivoted.sort_values(by="Total", ascending=False)

    return pivoted
