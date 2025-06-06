import pandas as pd

def get_chances_by_player(df):
    qualities = ["Low Q", "Mid Q", "High Q", "Pot +"]

    players = df[df["Action"].str.contains("Chance For", na=False)]

    tor_df = df[df["Action"].str.startswith("Tor Tigers", na=False)]
    tor_counts = tor_df["Spieler Tigers"].value_counts()

    data = []

    for player, group in players.groupby("Spieler Tigers"):
        row = {"Spieler": player}

        for q in qualities:
            row[q] = group["Action"].str.contains(f"{q} Chance For", na=False).sum()

        row["Total"] = sum(row[q] for q in qualities)

        xg_series = pd.to_numeric(group.get("XG", pd.Series(dtype=float)), errors="coerce")
        row["xG"] = round(xg_series.sum(skipna=True), 2)

        if "Schussmetrik" in df.columns:
            for metric in ["Auf Tor", "Neben Tor", "Geblockt"]:
                shots = group[group["Schussmetrik"] == metric].shape[0]
                pct = round((shots / row["Total"]) * 100, 1) if row["Total"] > 0 else 0
                row[metric] = shots
                row[f"% {metric}"] = pct
        else:
            for metric in ["Auf Tor", "Neben Tor", "Geblockt"]:
                row[metric] = 0
                row[f"% {metric}"] = 0

        row["Tore"] = tor_counts.get(player, 0)
        row["Effizienz"] = f"{round((row['Tore'] / row['Total']) * 100, 1)} %" if row["Total"] > 0 else "0 %"

        data.append(row)

    df_out = pd.DataFrame(data)

    if df_out.empty or "Total" not in df_out.columns:
        # Leeres DataFrame mit passenden Spalten zurückgeben, falls keine Daten vorhanden
        return pd.DataFrame(columns=["Spieler", "Low Q", "Mid Q", "High Q", "Pot +", "Total", "xG", "Auf Tor", "Neben Tor", "Geblockt", "Tore", "Effizienz"])

    return df_out.sort_values(by="Total", ascending=False).reset_index(drop=True)
