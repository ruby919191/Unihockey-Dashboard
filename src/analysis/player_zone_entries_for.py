import pandas as pd

def get_player_zone_entries(df):
    """
    Gibt ZOE For pro Spieler mit Qualität (Good/Bad) zurück.
    Zeigt alle Spieler, auch wenn sie keine Aktion hatten (NaN-Werte).
    """

    # Alle beteiligten Spieler aus allen relevanten Spalten extrahieren
    player_columns = ["Spieler Tigers", "Spieler Tigers 1", "Spieler Tigers 2"]
    players = pd.Series(dtype=str)
    for col in player_columns:
        if col in df.columns:
            players = pd.concat([players, df[col].dropna().astype(str).str.strip()])

    all_players = players.drop_duplicates().sort_values().tolist()

    # Nur ZOE For analysieren
    entries = df[df["Action"].str.contains("ZOE For", na=False)]

    # Daten für alle Spieler sammeln
    data = []

    for col in player_columns:
        if col not in entries.columns:
            continue

        grouped = entries.dropna(subset=[col]).groupby(col)

        for player, group in grouped:
            good = group[group["ZOE_For"] == "Good"].shape[0]
            bad = group[group["ZOE_For"] == "Bad"].shape[0]
            total = good + bad
            pct_good = round((good / total) * 100, 1) if total > 0 else 0.0

            data.append({
                "Spieler": player.strip(),
                "Good": good,
                "Bad": bad,
                "Total": total,
                "ZOE Good %": pct_good
            })

    # DataFrame erstellen und nach Spieler gruppieren, um Doppelzählungen zu addieren
    df_result = pd.DataFrame(data)
    if df_result.empty:
        # Falls keine Daten, trotzdem alle Spieler zeigen mit 0 Werten
        df_result = pd.DataFrame({
            "Spieler": all_players,
            "Good": 0,
            "Bad": 0,
            "Total": 0,
            "ZOE Good %": 0.0
        })
    else:
        df_result = (
            df_result.groupby("Spieler", as_index=False)
            .agg({
                "Good": "sum",
                "Bad": "sum",
                "Total": "sum",
                "ZOE Good %": "mean"  # gewichtete Werte könnten besser sein, aber hier Mittelwert
            })
        )

        # Falls es Spieler gibt, die keine Einträge haben, fülle sie mit 0
        missing_players = set(all_players) - set(df_result["Spieler"])
        if missing_players:
            missing_df = pd.DataFrame({
                "Spieler": list(missing_players),
                "Good": 0,
                "Bad": 0,
                "Total": 0,
                "ZOE Good %": 0.0
            })
            df_result = pd.concat([df_result, missing_df], ignore_index=True)

    # Sortieren
    df_result = df_result.sort_values(by="Total", ascending=False, na_position="last").reset_index(drop=True)

    return df_result
