import pandas as pd

def count_goals_by_situation(df, team_name, opponent_name, situation_for, situation_against):
    df_for = df[df["Nummerische Spielsituation"] == situation_for]
    df_against = df[df["Nummerische Spielsituation"] == situation_against]

    is_divers = (df["season"].iloc[0] == "Divers") if ("season" in df.columns and not df.empty) else False

    # Tore für team_name
    if is_divers and not df_for.empty:
        team_for = df_for["team_for"].iloc[0]
        team_against = df_for["team_against"].iloc[0]
        if team_name == team_for:
            goals_for = df_for[df_for["Action"].str.startswith(f"Tor {team_for}")].shape[0]
        elif team_name == team_against:
            goals_for = df_for[df_for["Action"].str.startswith(f"Tor {team_against}")].shape[0]
        else:
            goals_for = 0
    else:
        goals_for = df_for[df_for["Action"].str.startswith(f"Tor {team_name}")].shape[0]

    # Tore für opponent_name
    if is_divers and not df_against.empty:
        team_for = df_against["team_for"].iloc[0]
        team_against = df_against["team_against"].iloc[0]
        if opponent_name == team_for:
            goals_against = df_against[df_against["Action"].str.startswith(f"Tor {team_for}")].shape[0]
        elif opponent_name == team_against:
            goals_against = df_against[df_against["Action"].str.startswith(f"Tor {team_against}")].shape[0]
        else:
            goals_against = 0
    else:
        goals_against = df_against[df_against["Action"].str.startswith(f"Tor {opponent_name}")].shape[0]

    return goals_for, goals_against

def generate_kpi_summary(df, team_name="Tigers", opponent_name="Gegner"):
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
    corsi_pct = round((corsi_for / (corsi_for + corsi_against)) * 100, 1) if (corsi_for + corsi_against) > 0 else 0

    fenwick_for = df[df["is_chance_for"] & (df.get("Schussmetrik") != "Geblockt")].shape[0] if "Schussmetrik" in df.columns else 0
    fenwick_against = df[df["is_chance_against"] & (df.get("Schussmetrik") != "Geblockt")].shape[0] if "Schussmetrik" in df.columns else 0
    fenwick_pct = round((fenwick_for / (fenwick_for + fenwick_against)) * 100, 1) if (fenwick_for + fenwick_against) > 0 else 0

    # 5:5 Tore
    df_goals_for = df[df["Action"].str.startswith(f"Tor {team_name}") & (df["Nummerische Spielsituation"] == "5:5")] if "Nummerische Spielsituation" in df.columns else pd.DataFrame()
    df_goals_against = df[df["Action"].str.startswith(f"Tor {opponent_name}") & (df["Nummerische Spielsituation"] == "5:5")] if "Nummerische Spielsituation" in df.columns else pd.DataFrame()
    goals_for = df_goals_for.shape[0]
    goals_against = df_goals_against.shape[0]
    goal_diff = goals_for - goals_against

    # Powerplay Tore 5:4 / 4:5
    pp_goals_for, pp_goals_against = count_goals_by_situation(df, team_name, opponent_name, "5:4", "4:5")

    # Boxplay Tore 4:5 / 5:4
    bp_goals_for, bp_goals_against = count_goals_by_situation(df, team_name, opponent_name, "4:5", "5:4")

    # 6:5 Tore Tigers / Gegner
    six_five_goals_for, six_five_goals_against = count_goals_by_situation(df, team_name, opponent_name, "6:5", "6:5")

    # 5:6 Tore Tigers / Gegner
    five_six_goals_for, five_six_goals_against = count_goals_by_situation(df, team_name, opponent_name, "5:6", "5:6")

    # Effizienz
    efficiency = round((goals_for / chances_for) * 100, 1) if chances_for > 0 else 0

    # Mid-High %
    high_mid_for = df[df["Action"].str.contains("High Q Chance For|Mid Q Chance For", na=False)].shape[0]
    mid_high_pct = round((high_mid_for / chances_for) * 100, 1) if chances_for > 0 else 0

    # ZOE For
    if "ZOE_For" in df.columns:
        zoe_for = df[df["Action"].str.contains("ZOE For", na=False)]
        good_zoe_for = zoe_for[zoe_for["ZOE_For"] == "Good"].shape[0] if not zoe_for.empty else 0
        zoe_for_total = zoe_for.shape[0]
        good_zoe_for_pct = round((good_zoe_for / zoe_for_total) * 100, 1) if zoe_for_total > 0 else 0
    else:
        good_zoe_for_pct = 0
        zoe_for_total = 0

    # ZOE Against
    if "ZOE_Against" in df.columns:
        zoe_against = df[df["Action"].str.contains("ZOE Gegner", na=False)]
        good_zoe_against = zoe_against[zoe_against["ZOE_Against"] == "Good"].shape[0] if not zoe_against.empty else 0
        zoe_against_total = zoe_against.shape[0]
        good_zoe_against_pct = round((good_zoe_against / zoe_against_total) * 100, 1) if zoe_against_total > 0 else 0
    else:
        good_zoe_against_pct = 0
        zoe_against_total = 0

    # Konter
    counter_for = df[df["Action"].str.contains("Chance For", na=False) & (df.get("Taktische Spielsituation") == "Konter")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    counter_against = df[df["Action"].str.contains("Chance Against", na=False) & (df.get("Taktische Spielsituation") == "Konter")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    counter_diff = counter_for - counter_against

    # Auslösung
    build_for = df[df["Action"].str.contains("Chance For", na=False) & (df.get("Taktische Spielsituation") == "Auslösung")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    build_against = df[df["Action"].str.contains("Chance Against", na=False) & (df.get("Taktische Spielsituation") == "Auslösung")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    build_diff = build_for - build_against

    # Spezial-Situationen: Chancen Tigers (alles außer 5:5 inkl. 4:4)
    spezial_chancen_for = df[
        (df["is_chance_for"]) & (~df["Nummerische Spielsituation"].isin(["5:5"]))
    ].shape[0]

    # Spezial-Situationen: Chancen Gegner (alles außer 5:5 inkl. 4:4)
    spezial_chancen_against = df[
        (df["is_chance_against"]) & (~df["Nummerische Spielsituation"].isin(["5:5"]))
    ].shape[0]

    gesamt_chancen = chances_for + chances_against
    spezial_pct_for = round((spezial_chancen_for / chances_for) * 100, 1) if chances_for > 0 else 0
    spezial_pct_against = round((spezial_chancen_against / chances_against) * 100, 1) if chances_against > 0 else 0

    # KPI-Tabelle mit dynamischen Teamnamen
    kpis = [
        (f"Chancen {team_name}", chances_for),
        (f"Chancen {opponent_name}", chances_against),
        ("Chancen-Differenz", f"{'+' if chance_diff >= 0 else ''}{chance_diff}"),
        ("Corsi %", f"{corsi_pct} %"),
        ("Fenwick %", f"{fenwick_pct} %"),
        (f"5:5 Tore {team_name}", goals_for),
        (f"5:5 Tore {opponent_name}", goals_against),
        (f"Powerplay Tore {team_name} (5:4)", pp_goals_for),
        (f"Powerplay Tore {opponent_name} (4:5)", pp_goals_against),
        (f"Boxplay Tore {team_name} (4:5)", bp_goals_for),
        (f"Boxplay Tore {opponent_name} (5:4)", bp_goals_against),
        (f"6:5 Tore {team_name}", six_five_goals_for),
        (f"6:5 Tore {opponent_name}", six_five_goals_against),
        (f"5:6 Tore {team_name}", five_six_goals_for),
        (f"5:6 Tore {opponent_name}", five_six_goals_against),
        ("Tordifferenz (5:5)", f"{'+' if goal_diff >= 0 else ''}{goal_diff}"),
        (f"Spezial % {team_name}", f"{spezial_pct_for} %"),
        (f"Spezial % {opponent_name}", f"{spezial_pct_against} %"),
        ("Effizienz (Tore/Chancen)", f"{efficiency} %"),
        ("Mid-High %", f"{mid_high_pct} %"),
        (f"ZOE {team_name} - Good %", f"{good_zoe_for_pct} %"),
        (f"ZOE {team_name} - Total", zoe_for_total),
        (f"ZOE {opponent_name} - Good %", f"{good_zoe_against_pct} %"),
        (f"ZOE {opponent_name} - Total", zoe_against_total),
        (f"Chancen {team_name} (Konter)", counter_for),
        (f"Chancen {opponent_name} (Konter)", counter_against),
        ("Konter-Differenz", f"{'+' if counter_diff >= 0 else ''}{counter_diff}"),
        (f"Chancen {team_name} (Auslösung)", build_for),
        (f"Chancen {opponent_name} (Auslösung)", build_against),
        ("Auslösungs-Differenz", f"{'+' if build_diff >= 0 else ''}{build_diff}")
    ]

    return pd.DataFrame(kpis, columns=["Metrik", "Wert"])
