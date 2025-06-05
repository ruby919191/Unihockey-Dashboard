import pandas as pd

def calculate_save_percentages(df):
    """
    Berechnet die Save Percentage für Tigers und Gegner pro Spiel.
    Annahme: 'Schussmetrik' gibt an, ob ein Schuss 'Auf Tor', 'Neben Tor' oder 'Geblockt' ist,
    'Action' enthält Treffer ('Tor Tigers', 'Tor Gegner').
    """
    results = []

    for game_id, group in df.groupby("game"):
        shots_on_tigers = group[(group["Schussmetrik"] == "Auf Tor") & (group["Action"].str.contains("Chance Against", na=False))]
        goals_on_tigers = group[group["Action"].str.contains("Tor Tigers", na=False)]

        shots_on_opponent = group[(group["Schussmetrik"] == "Auf Tor") & (group["Action"].str.contains("Chance For", na=False))]
        goals_on_opponent = group[group["Action"].str.contains("Tor Gegner", na=False)]

        # Anzahl Schüsse aufs Tor
        shots_tigers = len(shots_on_tigers)
        shots_opponent = len(shots_on_opponent)

        # Anzahl Gegentore
        goals_tigers = len(goals_on_tigers)
        goals_opponent = len(goals_on_opponent)

        save_perc_tigers = round(((shots_tigers - goals_tigers) / shots_tigers) * 100, 1) if shots_tigers > 0 else None
        save_perc_opponent = round(((shots_opponent - goals_opponent) / shots_opponent) * 100, 1) if shots_opponent > 0 else None

        results.append({
            "game": game_id,
            "Save % For": save_perc_opponent,
            "Save % Against": save_perc_tigers
        })

    return pd.DataFrame(results)
