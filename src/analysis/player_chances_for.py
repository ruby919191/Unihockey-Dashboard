import pandas as pd

def get_chances_by_player(df):
    """
    Gibt eine Auswertung der Chancen For nach Spieler zurück.
    Zählt verschiedene Q-Klassen, XG, Trefferarten und berechnet Effizienz.
    """
    qualities = ["Low Q", "Mid Q", "High Q", "Pot +"]
    players = df[df["Action"].str.contains("Chance For", na=False)]

    data = []

    for player, group in players.groupby("Spieler Tigers"):
        row = {"Spieler": player}

        for q in qualities:
            row[q] = group["Action"].str.contains(f"{q} Chance For", na=False).sum()

        row["Total"] = sum(row[q] for q in qualities)

        # ✅ Robust gegen fehlende oder nicht-numerische XG
        xg_series = pd.to_numeric(group.get("XG", pd.Series(dtype=float)), errors="coerce")
        row["xG"] = round(xg_series.sum(skipna=True), 2)

        # Schussmetrik
        for metric in ["Auf Tor", "Neben Tor", "Geblockt"]:
            shots = group[group["Schussmetrik"] == metric].shape[0]
            pct = round((shots / row["Total"]) * 100, 1) if row["Total"] > 0 else 0
            row[metric] = shots
            row[f"% {metric}"] = pct

        # Tore zählen
        goals = df[df["Action"].str.startswith("Tor Tigers") & (df["Spieler Tigers"] == player)].shape[0]
        row["Tore"] = goals
        row["Effizienz"] = f"{round((goals / row['Total']) * 100, 1)} %" if row["Total"] > 0 else "0 %"

        data.append(row)

    return pd.DataFrame(data).sort_values(by="Total", ascending=False).reset_index(drop=True)
