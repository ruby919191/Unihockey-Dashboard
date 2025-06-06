import pandas as pd

def calculate_season_summary(df):
    # Nur Saisons außer 'Divers'
    df_filtered = df[df["season"] != "Divers"]

    # Gewünschte Metriken definieren
    metrics = {
        "Chancen For": lambda d: d["Action"].str.contains("Chance For", na=False).sum(),
        "Chancen Against": lambda d: d["Action"].str.contains("Chance Against", na=False).sum(),
        "Corsi": lambda d: d["Action"].str.contains("Chance For", na=False).sum() / (
            d["Action"].str.contains("Chance For", na=False).sum() + d["Action"].str.contains("Chance Against", na=False).sum()
        ) if (d["Action"].str.contains("Chance For", na=False).sum() + d["Action"].str.contains("Chance Against", na=False).sum()) > 0 else 0,
        "Fenwick": lambda d: d[(d["Action"].str.contains("Chance For", na=False)) & (d["Schussmetrik"] != "Geblockt")].shape[0] / (
            d[(d["Action"].str.contains("Chance For", na=False)) & (d["Schussmetrik"] != "Geblockt")].shape[0] +
            d[(d["Action"].str.contains("Chance Against", na=False)) & (d["Schussmetrik"] != "Geblockt")].shape[0]
        ) if (d[(d["Action"].str.contains("Chance For", na=False)) & (d["Schussmetrik"] != "Geblockt")].shape[0] +
            d[(d["Action"].str.contains("Chance Against", na=False)) & (d["Schussmetrik"] != "Geblockt")].shape[0]) > 0 else 0,
        "Tore aus Auslösung": lambda d: d[(d["Action"].str.contains("Tor Tigers", na=False)) & (d["Taktische Spielsituation"] == "Auslösung")].shape[0],
        "Tore aus Konter": lambda d: d[(d["Action"].str.contains("Tor Tigers", na=False)) & (d["Taktische Spielsituation"] == "Konter")].shape[0],
        "Tore aus Festsetzen": lambda d: d[(d["Action"].str.contains("Tor Tigers", na=False)) & (d["Taktische Spielsituation"] == "Festsetzen")].shape[0],
        "Chancen aus Konter": lambda d: d[(d["Action"].str.contains("Chance For", na=False)) & (d["Taktische Spielsituation"] == "Konter")].shape[0],
        "Chancen aus Auslösung": lambda d: d[(d["Action"].str.contains("Chance For", na=False)) & (d["Taktische Spielsituation"] == "Auslösung")].shape[0],
    }

    play_metrics = []
    for (season, game), group in df_filtered.groupby(["season", "game"]):
        metric_values = {"season": season, "game": game}
        for name, func in metrics.items():
            metric_values[name] = func(group)
        play_metrics.append(metric_values)

    plays_df = pd.DataFrame(play_metrics)

    # Nur numerische Spalten auswählen (ohne season, game)
    numeric_cols = plays_df.select_dtypes(include="number").columns

    # Median und Mean je Saison berechnen nur für numerische Spalten
    median_df = plays_df.groupby("season")[numeric_cols].median().add_suffix(" Median")
    mean_df = plays_df.groupby("season")[numeric_cols].mean().add_suffix(" Mittelwert")

    summary_df = pd.concat([median_df, mean_df], axis=1).reset_index()

    return summary_df
