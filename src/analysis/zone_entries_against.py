import pandas as pd

def get_zone_entries_against(df):
    """
    Gibt alle Zone Entries Against zurück (Action enthält 'ZOE Gegner:').
    """
    return df[df["Action"].str.contains("ZOE Gegner:", na=False)].reset_index(drop=True)

def count_zone_entries_against_by_quality(df):
    """
    Zählt alle ZOE Against nach Qualität (Good/Bad) + Prozentsatz.
    """
    entries = get_zone_entries_against(df)
    total = entries.shape[0]
    good = entries[entries["ZOE_Against"] == "Good"].shape[0]
    bad = entries[entries["ZOE_Against"] == "Bad"].shape[0]

    return pd.DataFrame([
        ["Good", good, round((good / total) * 100, 1) if total else 0.0],
        ["Bad", bad, round((bad / total) * 100, 1) if total else 0.0],
        ["Total", total, ""]
    ], columns=["Qualität", "Anzahl", "%"])

def count_zone_entries_against_by_period(df):
    """
    Zählt Anzahl ZOE Against pro Drittel.
    """
    entries = get_zone_entries_against(df)
    return (
        entries.groupby("Drittel")
        .size()
        .reset_index(name="ZOE Against")
        .sort_values(by="Drittel")
        .reset_index(drop=True)
    )

def count_zone_entries_against_by_line(df):
    """
    Zählt Anzahl ZOE Against pro Linie.
    """
    entries = get_zone_entries_against(df)
    entries = entries.dropna(subset=["Linien For"])
    return (
        entries.groupby("Linien For")
        .size()
        .reset_index(name="ZOE Against")
        .sort_values(by="ZOE Against", ascending=False)
        .reset_index(drop=True)
    )
