import pandas as pd

def get_player_pass_participation(df):
    """
    Analysiert die Spielerbeteiligung bei Chancen For aus der Spalte 'Spieler Tigers 2'
    und gliedert nach Chancearten (Low Q, Mid Q, High Q, Pot +).
    """
    df = df[df["Action"].str.contains("Chance For", na=False)]
    df = df.dropna(subset=["Spieler Tigers 2"])

    # Mögliche Chancenarten
    chance_types = ["Low Q", "Mid Q", "High Q", "Pot +"]
    rows = {}

    for _, row in df.iterrows():
        player_str = row["Spieler Tigers 2"]
        chance_type = next((ct for ct in chance_types if ct in row["Action"]), None)
        if not chance_type:
            continue

        players = [p.strip() for p in player_str.split(",")]
        for player in players:
            if player not in rows:
                rows[player] = {ct: 0 for ct in chance_types}
            rows[player][chance_type] += 1

    df_result = pd.DataFrame.from_dict(rows, orient="index").fillna(0).astype(int)
    df_result["Total"] = df_result.sum(axis=1)
    df_result = df_result.sort_values("Total", ascending=False).reset_index()
    df_result = df_result.rename(columns={"index": "Spieler"})

    return df_result
