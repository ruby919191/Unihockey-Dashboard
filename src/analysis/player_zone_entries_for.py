import pandas as pd

def get_player_zone_entries(df):
    """
    Gibt ZOE For pro Spieler mit Qualität (Good/Bad) zurück.
    Berechnet Anzahl Good, Bad, Total und Good-% pro Spieler.
    """
    entries = df[df["Action"].str.contains("ZOE For", na=False)]
    entries = entries.dropna(subset=["Spieler Tigers"])

    data = []
    for player, group in entries.groupby("Spieler Tigers"):
        good = group[group["ZOE_For"] == "Good"].shape[0]
        bad = group[group["ZOE_For"] == "Bad"].shape[0]
        total = good + bad
        pct_good = round((good / total) * 100, 1) if total > 0 else 0.0

        data.append({
            "Spieler": player,
            "Good": good,
            "Bad": bad,
            "Total": total,
            "ZOE Good %": pct_good
        })

    return pd.DataFrame(data).sort_values(by="Total", ascending=False).reset_index(drop=True)
