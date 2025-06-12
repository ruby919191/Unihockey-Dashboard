def filter_data_for_trends(all_df):
    df = all_df.copy()
    
    # Setze Liga auf L-UPL für alle Saisons außer 'Divers'
    df["league_for_trends"] = df.apply(
        lambda row: "L-UPL" if row["season"] != "Divers" else row["league"],
        axis=1
    )

    # Filtern nur die gewünschten Ligen für Trends
    allowed_leagues = [
        "SSL",
        "Fliiga",
        "L-UPL",
        "Superliga",
        "International Men",
        "International Women"
    ]

    df_filtered = df[df["league_for_trends"].isin(allowed_leagues)]
    return df_filtered
