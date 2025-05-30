import pandas as pd

def calculate_save_percentages(df):
    """
    Berechnet Save % For und Save % Opponent auf Basis von Chancen und Toren.
    Erwartet:
    - Action enthält 'Chance For' oder 'Chance Against'
    - Schussmetrik == 'Auf Tor'
    - Tore als 'Tor Tigers:' und 'Tor Gegner:' in 'Action'
    """
    games = df["game"].unique()
    rows = []

    for game in games:
        game_df = df[df["game"] == game]

        # Chancen Against mit Schuss auf Tor
        against = game_df[
            (game_df["Schussmetrik"] == "Auf Tor") &
            (game_df["Action"].str.contains("Chance Against", na=False))
        ]
        shots_against = against.shape[0]

        # Gegentore: "Tor Gegner:"
        goals_against = game_df["Action"].str.contains("Tor Gegner:", na=False).sum()

        # Chancen For mit Schuss auf Tor
        for_df = game_df[
            (game_df["Schussmetrik"] == "Auf Tor") &
            (game_df["Action"].str.contains("Chance For", na=False))
        ]
        shots_for = for_df.shape[0]

        # Eigene Tore: "Tor Tigers:"
        goals_for = game_df["Action"].str.contains("Tor Tigers:", na=False).sum()

        save_for = round((1 - (goals_against / shots_against)) * 100, 1) if shots_against > 0 else None
        save_against = round((1 - (goals_for / shots_for)) * 100, 1) if shots_for > 0 else None

        xg_for = game_df[game_df["Action"].str.contains("Chance For", na=False)]["XG"].sum()
        xg_against = game_df[game_df["Action"].str.contains("Chance Against", na=False)]["XG"].sum()

        rows.append({
            "game": game,
            "Shots Against": shots_against,
            "Goals Against": goals_against,
            "Shots For": shots_for,
            "Goals For": goals_for,
            "Save % For": save_for,
            "Save % Against": save_against,
            "xG For": round(xg_for, 2),
            "xG Against": round(xg_against, 2)
        })

    return pd.DataFrame(rows)
