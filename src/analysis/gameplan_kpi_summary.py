import pandas as pd

def generate_kpi_summary(df, team_name="Tigers", opponent_name="Gegner"):
    """
    Erstellt eine übersichtliche KPI-Tabelle mit zentralen Spielmetriken.
    """
    # Flags für Chancen
    df["is_chance_for"] = df["Action"].str.contains("Chance For", na=False)
    df["is_chance_against"] = df["Action"].str.contains("Chance Against", na=False)

    # Chancen zählen
    chances_for = df["is_chance_for"].sum()
    chances_against = df["is_chance_against"].sum()
    chance_diff = chances_for - chances_against

    # Corsi und Fenwick
    corsi_for = chances_for
    corsi_against = chances_against
    corsi_pct = round((corsi_for / (corsi_for + corsi_against)) * 100, 1) if corsi_for + corsi_against > 0 else 0

    fenwick_for = df[df["is_chance_for"] & (df["Schussmetrik"] != "Geblockt")].shape[0]
    fenwick_against = df[df["is_chance_against"] & (df["Schussmetrik"] != "Geblockt")].shape[0]
    fenwick_pct = round((fenwick_for / (fenwick_for + fenwick_against)) * 100, 1) if fenwick_for + fenwick_against > 0 else 0

    # 5:5 Tore
    df_goals_for = df[df["Action"].str.startswith(f"Tor {team_name}") & (df["Nummerische Spielsituation"] == "5:5")]
    df_goals_against = df[df["Action"].str.startswith(f"Tor {opponent_name}") & (df["Nummerische Spielsituation"] == "5:5")]
    goals_for = df_goals_for.shape[0]
    goals_against = df_goals_against.shape[0]
    goal_diff = goals_for - goals_against

    # Effizienz
    efficiency = round((goals_for / chances_for) * 100, 1) if chances_for > 0 else 0

    # Mid-High %
    high_mid_for = df[df["Action"].str.contains("High Q Chance For|Mid Q Chance For", na=False)].shape[0]
    mid_high_pct = round((high_mid_for / chances_for) * 100, 1) if chances_for > 0 else 0

    # ZOE
    zoe_for = df[df["Action"].str.contains("ZOE For", na=False)]
    zoe_against = df[df["Action"].str.contains("ZOE Gegner", na=False)]

    good_zoe_for = zoe_for[zoe_for["ZOE_For"] == "Good"].shape[0]
    good_zoe_against = zoe_against[zoe_against["ZOE_Against"] == "Good"].shape[0]

    zoe_for_total = zoe_for.shape[0]
    zoe_against_total = zoe_against.shape[0]

    good_zoe_for_pct = round((good_zoe_for / zoe_for_total) * 100, 1) if zoe_for_total > 0 else 0
    good_zoe_against_pct = round((good_zoe_against / zoe_against_total) * 100, 1) if zoe_against_total > 0 else 0

    # Konter
    counter_for = df[df["Action"].str.contains("Chance For", na=False) & (df["Taktische Spielsituation"] == "Konter")].shape[0]
    counter_against = df[df["Action"].str.contains("Chance Against", na=False) & (df["Taktische Spielsituation"] == "Konter")].shape[0]
    counter_diff = counter_for - counter_against

    # Auslösung
    build_for = df[df["Action"].str.contains("Chance For", na=False) & (df["Taktische Spielsituation"] == "Auslösung")].shape[0]
    build_against = df[df["Action"].str.contains("Chance Against", na=False) & (df["Taktische Spielsituation"] == "Auslösung")].shape[0]
    build_diff = build_for - build_against

    # KPI-Tabelle
    kpis = [
        ("Chancen For", chances_for),
        ("Chancen Against", chances_against),
        ("Chancen-Differenz", f"{'+' if chance_diff >=0 else ''}{chance_diff}"),
        ("Corsi %", f"{corsi_pct} %"),
        ("Fenwick %", f"{fenwick_pct} %"),
        ("5:5 Tore For", goals_for),
        ("5:5 Tore Against", goals_against),
        ("Tordifferenz (5:5)", f"{'+' if goal_diff >=0 else ''}{goal_diff}"),
        ("Effizienz (Tore/Chancen)", f"{efficiency} %"),
        ("Mid-High %", f"{mid_high_pct} %"),
        ("ZOE For - Good %", f"{good_zoe_for_pct} %"),
        ("ZOE For - Total", zoe_for_total),
        ("ZOE Against - Good %", f"{good_zoe_against_pct} %"),
        ("ZOE Against - Total", zoe_against_total),
        ("Chancen For (Konter)", counter_for),
        ("Chancen Against (Konter)", counter_against),
        ("Konter-Differenz", f"{'+' if counter_diff >=0 else ''}{counter_diff}"),
        ("Chancen For (Auslösung)", build_for),
        ("Chancen Against (Auslösung)", build_against),
        ("Auslösungs-Differenz", f"{'+' if build_diff >=0 else ''}{build_diff}")
    ]

    return pd.DataFrame(kpis, columns=["Metrik", "Wert"])
