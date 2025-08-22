import pandas as pd
import re

def calculate_dynamic_save_percentages(df, team_for, team_against):
    results = []

    # Regex nur für echte Chancen (ohne Potentials)
    chance_for_pattern = r"^(Low Q Chance|Mid Q Chance|High Q Chance) For"
    chance_against_pattern = r"^(Low Q Chance|Mid Q Chance|High Q Chance) Against"

    for game_id, group in df.groupby("game"):
        action = group["Action"].fillna("")
        schuss = group["Schussmetrik"].fillna("")

        # Tore
        goals_for = action.str.startswith(f"Tor {team_for}", na=False)
        goals_against = action.str.startswith(f"Tor {team_against}", na=False)

        # Chancen aufs Tor (on target)
        shots_for = (action.str.contains(chance_for_pattern, na=False, regex=True) & (schuss == "Auf Tor")) | goals_for
        shots_against = (action.str.contains(chance_against_pattern, na=False, regex=True) & (schuss == "Auf Tor")) | goals_against

        n_goals_for = int(goals_for.sum())
        n_goals_against = int(goals_against.sum())
        n_shots_for = int(shots_for.sum())
        n_shots_against = int(shots_against.sum())

        # Helper
        def save_pct(goals: int, sog: int):
            if sog == 0 or goals > sog:
                return None
            return round((1 - goals / sog) * 100, 1)

        save_perc_for = save_pct(n_goals_for, n_shots_for)
        save_perc_against = save_pct(n_goals_against, n_shots_against)

        results.append({
            "game": game_id,
            f"Save % {team_for}": save_perc_for,
            f"Save % {team_against}": save_perc_against
        })

    return pd.DataFrame(results)
