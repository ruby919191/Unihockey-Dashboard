import pandas as pd

def get_high_mid_chances_by_player(df):
    """
    Gibt eine Übersicht über Mid Q und High Q Chancen pro Spieler
    sowie den Gesamtwert und den Anteil in Prozent.
    """
    # Nur Mid Q und High Q Chance For
    filtered = df[df["Action"].str.contains("Mid Q Chance For|High Q Chance For", na=False)]

    # Gruppieren
    grouped = filtered.groupby(["Spieler Tigers", "Action"]).size().unstack(fill_value=0)

    # Umbenennen für Klarheit
    grouped = grouped.rename(columns={
        "Mid Q Chance For: 1": "Mid Q",
        "High Q Chance For: 1": "High Q"
    })

    # Falls es mehrere Versionen gibt wie ": 2", ": 3", etc., fassen wir das generischer zusammen
    grouped["Mid Q"] = df[df["Action"].str.contains("Mid Q Chance For", na=False)] \
        .groupby("Spieler Tigers").size()
    grouped["High Q"] = df[df["Action"].str.contains("High Q Chance For", na=False)] \
        .groupby("Spieler Tigers").size()

    grouped = grouped.fillna(0).astype(int)

    # Total & Prozent
    grouped["Total"] = grouped["Mid Q"] + grouped["High Q"]
    grouped["HighMid %"] = round((grouped["High Q"] / grouped["Total"]) * 100, 1)
    grouped["HighMid %"] = grouped["HighMid %"].fillna(0.0)

    return grouped.reset_index().sort_values(by="Total", ascending=False).reset_index(drop=True)
