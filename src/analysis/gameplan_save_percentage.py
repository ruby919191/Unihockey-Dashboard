import pandas as pd

def calculate_save_percentages(df):
    """
    Berechnet Save % For und Save % Against basierend auf Chancen und Tore.
    """
    shots_for = df[df["Action"].str.contains("Chance For", na=False)]
    goals_for = df[df["Action"].str.contains("Tor Tigers", na=False)]

    shots_against = df[df["Action"].str.contains("Chance Against", na=False)]
    goals_against = df[df["Action"].str.contains("Tor Gegner", na=False)]

    def safe_pct(goals, shots):
        return round((1 - goals / shots) * 100, 1) if shots > 0 else 0.0

    return pd.DataFrame([
        ["Shots For", shots_for.shape[0]],
        ["Goals For", goals_for.shape[0]],
        ["Save % For", safe_pct(goals_for.shape[0], shots_for.shape[0])],
        ["Shots Against", shots_against.shape[0]],
        ["Goals Against", goals_against.shape[0]],
        ["Save % Against", safe_pct(goals_against.shape[0], shots_against.shape[0])]
    ], columns=["Metrik", "Wert"])
