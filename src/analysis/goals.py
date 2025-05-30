import pandas as pd

def get_game_goals(df, team_name, opponent_name):
    team_prefix = f"Tor {team_name}"
    opponent_prefix = f"Tor {opponent_name}"

    goals_team = df[df["Action"].str.startswith(team_prefix)].shape[0]
    goals_opponent = df[df["Action"].str.startswith(opponent_prefix)].shape[0]

    return {
        team_name: goals_team,
        opponent_name: goals_opponent
    }

def get_team_goals_with_situation(df, team_name):
    prefix = f"Tor {team_name}"
    filtered = df[
        df["Action"].str.startswith(prefix) &
        (df["Nummerische Spielsituation"] == "5:5")
    ]
    return filtered[["Action", "Taktische Spielsituation"]].reset_index(drop=True)

def get_opponent_goals_with_situation(df, opponent_name="Gegner"):
    prefix = f"Tor {opponent_name}"
    filtered = df[
        df["Action"].str.startswith(prefix) &
        (df["Nummerische Spielsituation"] == "5:5")
    ]
    return filtered[["Action", "Taktische Spielsituation"]].reset_index(drop=True)

def get_goal_situation_counts(df, team_name):
    prefix = f"Tor {team_name}"
    filtered = df[
        df["Action"].str.startswith(prefix) &
        (df["Nummerische Spielsituation"] == "5:5")
    ]

    grouped = (
        filtered.groupby("Taktische Spielsituation")
        .size()
        .reset_index(name="Tore")
        .sort_values(by="Tore", ascending=False)
    )

    total_row = pd.DataFrame([{
        "Taktische Spielsituation": "Total",
        "Tore": grouped["Tore"].sum()
    }])

    return pd.concat([grouped, total_row], ignore_index=True)

def get_opponent_goal_situation_counts(df, opponent_name="Gegner"):
    """
    Gibt ein DataFrame mit Anzahl 5:5-Gegentore pro taktischer Spielsituation zurück – inklusive Total-Zeile.
    """
    prefix = f"Tor {opponent_name}"
    filtered = df[
        df["Action"].str.startswith(prefix) &
        (df["Nummerische Spielsituation"] == "5:5")
    ]

    grouped = (
        filtered.groupby("Taktische Spielsituation")
        .size()
        .reset_index(name="Tore")
        .sort_values(by="Tore", ascending=False)
    )

    total = grouped["Tore"].sum()
    total_row = pd.DataFrame([{
        "Taktische Spielsituation": "Total",
        "Tore": total
    }])

    return pd.concat([grouped, total_row], ignore_index=True)
