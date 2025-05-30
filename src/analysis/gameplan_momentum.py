import pandas as pd

def calculate_momentum_by_game(df):
    """
    Berechnet das Chancen-Momentum pro Spiel basierend auf:
    Chancen For vs. Chancen Against.
    Gibt DataFrame mit Spiel, Chancen For, Chancen Against, Momentum und Momentum-% zurück.
    """
    # Relevante Aktionen extrahieren
    df = df.copy()
    df = df[df["Action"].notna()]

    # Flags setzen
    df["is_chance_for"] = df["Action"].str.contains("Chance For", na=False)
    df["is_chance_against"] = df["Action"].str.contains("Chance Against", na=False)

    # Gruppieren pro Spiel
    grouped = df.groupby("Spiel").agg({
        "is_chance_for": "sum",
        "is_chance_against": "sum"
    }).reset_index()

    grouped = grouped.rename(columns={
        "is_chance_for": "Chancen For",
        "is_chance_against": "Chancen Against"
    })

    # Momentum berechnen
    grouped["Momentum"] = grouped["Chancen For"] - grouped["Chancen Against"]
    grouped["Momentum %"] = grouped.apply(
        lambda row: round((row["Chancen For"] / (row["Chancen For"] + row["Chancen Against"])) * 100, 1)
        if (row["Chancen For"] + row["Chancen Against"]) > 0 else 0.0,
        axis=1
    )

    return grouped.sort_values(by="Spiel").reset_index(drop=True)
