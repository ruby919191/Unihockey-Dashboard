import pandas as pd

def get_high_mid_chances_by_player(df):
    """
    Gibt eine Übersicht über Mid Q und High Q Chancen pro Spieler,
    basierend auf der Spalte 'Spieler Tigers' und Action-Werten,
    unabhängig vom Suffix (:1, :2, ...).
    """

    # Nur relevante Chancen (dein Team)
    filtered = df[df["Action"].str.contains("Mid Q Chance For|High Q Chance For", na=False)].copy()

    # Kategorie extrahieren: "Mid Q" oder "High Q"
    def extract_chance_type(action):
        if "Mid Q Chance For" in action:
            return "Mid Q"
        elif "High Q Chance For" in action:
            return "High Q"
        else:
            return None

    filtered["Chance Type"] = filtered["Action"].apply(extract_chance_type)

    # Gruppieren nach Spieler
    grouped = filtered.groupby(["Spieler Tigers", "Chance Type"]).size().unstack(fill_value=0)

    # Sicherstellen, dass beide Spalten existieren
    for col in ["Mid Q", "High Q"]:
        if col not in grouped.columns:
            grouped[col] = 0

    # Total & Prozentanteil
    grouped["Total"] = grouped["Mid Q"] + grouped["High Q"]
    grouped["HighMid %"] = round((grouped["High Q"] / grouped["Total"]) * 100, 1)
    grouped["HighMid %"] = grouped["HighMid %"].fillna(0.0)

    return grouped.reset_index().sort_values(by="Total", ascending=False).reset_index(drop=True)
