import pandas as pd

def count_goals_by_situation(df, team_name, opponent_name, situation_for, situation_against):
    """Zählt Tore in einer nummerischen Spielsituation, getrennt für team_name und opponent_name."""
    df_for = df[df["Nummerische Spielsituation"] == situation_for]
    df_against = df[df["Nummerische Spielsituation"] == situation_against]

    goals_for = df_for[df_for["Action"].str.startswith(f"Tor {team_name}")].shape[0]
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

    # Corsi & Fenwick
    corsi_for = chances_for
    corsi_against = chances_against
    corsi_pct = round((corsi_for / (corsi_for + corsi_against)) * 100, 1) if (corsi_for + corsi_against) > 0 else 0

    fenwick_for = df[df["is_chance_for"] & (df.get("Schussmetrik") != "Geblockt")].shape[0] if "Schussmetrik" in df.columns else 0
    fenwick_against = df[df["is_chance_against"] & (df.get("Schussmetrik") != "Geblockt")].shape[0] if "Schussmetrik" in df.columns else 0
    fenwick_pct = round((fenwick_for / (fenwick_for + fenwick_against)) * 100, 1) if (fenwick_for + fenwick_against) > 0 else 0

    # 5:5 Tore
    df_goals_for = df[df["Action"].str.startswith(f"Tor {team_name}") & (df["Nummerische Spielsituation"] == "5:5")]
    df_goals_against = df[df["Action"].str.startswith(f"Tor {opponent_name}") & (df["Nummerische Spielsituation"] == "5:5")]
    goals_for = df_goals_for.shape[0]
    goals_against = df_goals_against.shape[0]
    goal_diff = goals_for - goals_against

    # Special Situation Tore
    pp_goals_for, pp_goals_against = count_goals_by_situation(df, team_name, opponent_name, "5:4", "4:5")
    bp_goals_for, bp_goals_against = count_goals_by_situation(df, team_name, opponent_name, "4:5", "5:4")
    six_five_goals_for, six_five_goals_against = count_goals_by_situation(df, team_name, opponent_name, "6:5", "6:5")
    five_six_goals_for, five_six_goals_against = count_goals_by_situation(df, team_name, opponent_name, "5:6", "5:6")

    # Spezialtore total (nicht 5:5)
    special_goals_for = df[df["Action"].str.startswith(f"Tor {team_name}") & (df["Nummerische Spielsituation"] != "5:5")].shape[0]
    total_goals_for = df[df["Action"].str.startswith(f"Tor {team_name}")].shape[0]
    special_pct_for = round((special_goals_for / total_goals_for) * 100, 1) if total_goals_for > 0 else 0

    special_goals_against = df[df["Action"].str.startswith(f"Tor {opponent_name}") & (df["Nummerische Spielsituation"] != "5:5")].shape[0]
    total_goals_against = df[df["Action"].str.startswith(f"Tor {opponent_name}")].shape[0]
    special_pct_against = round((special_goals_against / total_goals_against) * 100, 1) if total_goals_against > 0 else 0

    # Effizienz
    efficiency = round((goals_for / chances_for) * 100, 1) if chances_for > 0 else 0

    # Mid/High Q %
    high_mid_for = df[df["Action"].str.contains("High Q Chance For|Mid Q Chance For", na=False)].shape[0]
    mid_high_pct = round((high_mid_for / chances_for) * 100, 1) if chances_for > 0 else 0

    # Konter / Auslösung
    counter_for = df[df["is_chance_for"] & (df.get("Taktische Spielsituation") == "Konter")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    counter_against = df[df["is_chance_against"] & (df.get("Taktische Spielsituation") == "Konter")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    counter_diff = counter_for - counter_against

    build_for = df[df["is_chance_for"] & (df.get("Taktische Spielsituation") == "Auslösung")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    build_against = df[df["is_chance_against"] & (df.get("Taktische Spielsituation") == "Auslösung")].shape[0] if "Taktische Spielsituation" in df.columns else 0
    build_diff = build_for - build_against

    # --- KPIs nach Kategorien ---
    kategorien = {
        "Chancen & Effizienz": [
            (f"Chancen {team_name}", chances_for),
            (f"Chancen {opponent_name}", chances_against),
            ("Chancen-Differenz", f"{'+' if chance_diff >= 0 else ''}{chance_diff}"),
            ("Effizienz (Tore/Chancen)", f"{efficiency} %"),
            ("Mid-High %", f"{mid_high_pct} %")
        ],
        "Corsi & Fenwick": [
            ("Corsi %", f"{corsi_pct} %"),
            ("Fenwick %", f"{fenwick_pct} %")
        ],
        "Tore (5:5 + Spezial)": [
            (f"5:5 Tore {team_name}", goals_for),
            (f"5:5 Tore {opponent_name}", goals_against),
            ("Tordifferenz (5:5)", f"{'+' if goal_diff >= 0 else ''}{goal_diff}"),
            (f"Powerplay Tore {team_name} (5:4)", pp_goals_for),
            (f"Powerplay Tore {opponent_name} (4:5)", pp_goals_against),
            (f"Boxplay Tore {team_name} (4:5)", bp_goals_for),
            (f"Boxplay Tore {opponent_name} (5:4)", bp_goals_against),
            (f"6:5 Tore {team_name}", six_five_goals_for),
            (f"6:5 Tore {opponent_name}", six_five_goals_against),
            (f"5:6 Tore {team_name}", five_six_goals_for),
            (f"5:6 Tore {opponent_name}", five_six_goals_against),
            (f"Spezial % {team_name}", f"{special_pct_for} %"),
            (f"Spezial % {opponent_name}", f"{special_pct_against} %")
        ],
        "Taktische Spielsituationen": [
            (f"Chancen {team_name} (Konter)", counter_for),
            (f"Chancen {opponent_name} (Konter)", counter_against),
            ("Konter-Differenz", f"{'+' if counter_diff >= 0 else ''}{counter_diff}"),
            (f"Chancen {team_name} (Auslösung)", build_for),
            (f"Chancen {opponent_name} (Auslösung)", build_against),
            ("Auslösungs-Differenz", f"{'+' if build_diff >= 0 else ''}{build_diff}")
        ]
    }

    df_kpis = pd.DataFrame(
        [(cat, m, v) for cat, items in kategorien.items() for m, v in items],
        columns=["Kategorie", "Metrik", "Wert"]
    )

    return df_kpis, kategorien


def generate_spielphasen_summary(df, team_name="Tigers", opponent_name="Gegner"):
    def calc_totals(for_pattern, against_pattern):
        total_for = df["Action"].str.contains(for_pattern, na=False).sum()
        total_against = df["Action"].str.contains(against_pattern, na=False).sum()
        return total_for, total_against

    # --- Berechnungen ---
    nachsetzen = calc_totals("Nachsetzen For", "Nachsetzen Against")
    pressing = calc_totals("Pressing For", "Pressing Against")
    zoe_exits = calc_totals("Zone-Exits For", "Zone-Exits Against")
    zoe_pressing = calc_totals("ZOE For gg. Pressing", "ZOE Against gg. Pressing")
    zoe_gesamt = calc_totals("ZOE For", "ZOE Against")

    kategorien = {
        "Nachsetzen": [
            (f"Nachsetzen {team_name} - Total", nachsetzen[0]),
            (f"Nachsetzen {opponent_name} - Total", nachsetzen[1]),
        ],
        "Pressing": [
            (f"Pressing {team_name} - Total", pressing[0]),
            (f"Pressing {opponent_name} - Total", pressing[1]),
        ],
        "Zone-Exits": [
            (f"Zone-Exits {team_name} - Total", zoe_exits[0]),
            (f"Zone-Exits {opponent_name} - Total", zoe_exits[1]),
        ],
        "ZOE gg. Pressing": [
            (f"ZOE gg. Pressing {team_name} - Total", zoe_pressing[0]),
            (f"ZOE gg. Pressing {opponent_name} - Total", zoe_pressing[1]),
        ],
        "ZOE Gesamt": [
            (f"ZOE {team_name} - Total", zoe_gesamt[0]),
            (f"ZOE {opponent_name} - Total", zoe_gesamt[1]),
        ]
    }

    df_spielphasen = pd.DataFrame(
        [(cat, m, v) for cat, items in kategorien.items() for m, v in items],
        columns=["Kategorie", "Metrik", "Wert"]
    )

    return df_spielphasen, kategorien
