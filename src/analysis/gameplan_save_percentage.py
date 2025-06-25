import pandas as pd
import re

def calculate_dynamic_save_percentages(df, team_for, team_against):
    results = []

    for game_id, group in df.groupby("game"):
        # Gegentore zählen
        goals_against = group[group["Action"].str.startswith(f"Tor {team_for}")]
        goals_for = group[group["Action"].str.startswith(f"Tor {team_against}")]

        # Korrekte Regex-Muster
        chance_for_pattern = r"^(Low Q Chance|Mid Q Chance|High Q Chance|Pot \+ Chance) For"
        chance_against_pattern = r"^(Low Q Chance|Mid Q Chance|High Q Chance|Pot \+ Chance) Against"

        # Schüsse aufs Tor
        shots_against = group[
            group["Action"].str.contains(chance_for_pattern, na=False, regex=True) &
            (group["Schussmetrik"] == "Auf Tor")
        ]
        shots_for = group[
            group["Action"].str.contains(chance_against_pattern, na=False, regex=True) &
            (group["Schussmetrik"] == "Auf Tor")
        ]

        # Zählungen
        n_goals_against = len(goals_against)
        n_goals_for = len(goals_for)
        n_shots_against = len(shots_against)
        n_shots_for = len(shots_for)

        # Berechnung mit Fehlerabfang
        if n_shots_against > 0:
            val = ((n_shots_against - n_goals_against) / n_shots_against) * 100
            save_perc_against = round(val, 1) if val >= 0 else 0.0
        else:
            save_perc_against = None

        if n_shots_for > 0:
            val = ((n_shots_for - n_goals_for) / n_shots_for) * 100
            save_perc_for = round(val, 1) if val >= 0 else 0.0
        else:
            save_perc_for = None

        # Ergebnis speichern
        results.append({
            "game": game_id,
            f"Save % {team_for}": save_perc_for,
            f"Save % {team_against}": save_perc_against
        })

    return pd.DataFrame(results)
