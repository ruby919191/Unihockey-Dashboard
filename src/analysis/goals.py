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

def get_team_line_goals(df):
    df_even = df[df["Nummerische Spielsituation"] == "5:5"].copy()

    def get_team_for(row):
        return row["team_for"] if row.get("season") == "Divers" else "Tigers"

    df_even["team_name"] = df_even.apply(get_team_for, axis=1)
    df_even["is_team_goal"] = df_even.apply(
        lambda r: r["Action"].startswith(f"Tor {r['team_name']}"), axis=1
    )

    goals_for = (
        df_even[df_even["is_team_goal"]]
        .groupby("Linien For")
        .size()
        .reset_index(name="Tore")
        .sort_values(by="Tore", ascending=False)
    )

    total_row = pd.DataFrame([{
        "Linien For": "Total",
        "Tore": goals_for["Tore"].sum()
    }])

    return pd.concat([goals_for, total_row], ignore_index=True)

def get_opponent_line_goals(df):
    df_even = df[df["Nummerische Spielsituation"] == "5:5"].copy()

    def get_team_against(row):
        return row["team_against"] if row.get("season") == "Divers" else "Gegner"

    df_even["opponent_name"] = df_even.apply(get_team_against, axis=1)
    df_even["is_opponent_goal"] = df_even.apply(
        lambda r: r["Action"].startswith(f"Tor {r['opponent_name']}"), axis=1
    )

    goals_against = (
        df_even[df_even["is_opponent_goal"]]
        .groupby("Linien For")
        .size()
        .reset_index(name="Gegentore")
        .sort_values(by="Gegentore", ascending=False)
    )

    total_row = pd.DataFrame([{
        "Linien For": "Total",
        "Gegentore": goals_against["Gegentore"].sum()
    }])

    return pd.concat([goals_against, total_row], ignore_index=True)

def get_plus_minus_line_table(df):
    tore_df = get_team_line_goals(df)
    gegentore_df = get_opponent_line_goals(df)

    merged = pd.merge(tore_df, gegentore_df, on="Linien For", how="outer").fillna(0)
    merged["Tore"] = merged["Tore"].astype(int)
    merged["Gegentore"] = merged["Gegentore"].astype(int)
    merged["+/-"] = merged["Tore"] - merged["Gegentore"]

    # Nur L1, L2, L3 anzeigen
    filtered = merged[merged["Linien For"].isin(["L1", "L2", "L3"])]
    return filtered.sort_values(by="+/-", ascending=False).reset_index(drop=True)

def get_opponent_goal_situation_counts(df, opponent_name="Gegner"):
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
