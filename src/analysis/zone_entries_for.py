import pandas as pd

def get_zone_entries_for(df):
    """
    Gibt alle Zone Entries For zurück (Action enthält 'ZOE For:').
    """
    return df[df["Action"].str.contains("ZOE For:", na=False)].reset_index(drop=True)

def count_zone_entries_by_quality(df):
    """
    Zählt alle ZOE For nach Qualität (Good/Bad) + Prozentsatz.
    """
    entries = get_zone_entries_for(df)
    total = entries.shape[0]
    good = entries[entries["ZOE_For"] == "Good"].shape[0]
    bad = entries[entries["ZOE_For"] == "Bad"].shape[0]

    return pd.DataFrame([
        ["Good", good, round((good / total) * 100, 1) if total else 0.0],
        ["Bad", bad, round((bad / total) * 100, 1) if total else 0.0],
        ["Total", total, ""]
    ], columns=["Qualität", "Anzahl", "%"])

def count_zone_entries_by_period(df):
    """
    Zählt Anzahl ZOE For pro Drittel.
    """
    entries = get_zone_entries_for(df)
    return (
        entries.groupby("Drittel")
        .size()
        .reset_index(name="ZOE For")
        .sort_values(by="Drittel")
        .reset_index(drop=True)
    )

def count_zone_entries_by_line(df):
    """
    Zählt Anzahl ZOE For pro Linie.
    """
    entries = get_zone_entries_for(df)
    entries = entries.dropna(subset=["Linien For"])
    return (
        entries.groupby("Linien For")
        .size()
        .reset_index(name="ZOE For")
        .sort_values(by="ZOE For", ascending=False)
        .reset_index(drop=True)
    )
