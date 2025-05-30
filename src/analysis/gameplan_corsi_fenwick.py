import pandas as pd

def calculate_corsi_fenwick(df):
    """
    Berechnet Corsi und Fenwick basierend auf Chancen-Events (nicht echten Schüssen).
    """
    corsi_for = df["Action"].str.contains("Chance For", na=False).sum()
    corsi_against = df["Action"].str.contains("Chance Against", na=False).sum()
    
    fenwick_for = df[
        df["Action"].str.contains("Chance For", na=False) &
        (df["Schussmetrik"] != "Geblockt")
    ].shape[0]
    
    fenwick_against = df[
        df["Action"].str.contains("Chance Against", na=False) &
        (df["Schussmetrik"] != "Geblockt")
    ].shape[0]
    
    total_corsi = corsi_for + corsi_against
    total_fenwick = fenwick_for + fenwick_against
    
    corsi_pct = round((corsi_for / total_corsi) * 100, 1) if total_corsi else 0.0
    fenwick_pct = round((fenwick_for / total_fenwick) * 100, 1) if total_fenwick else 0.0

    data = {
        "Corsi For": [corsi_for],
        "Corsi Against": [corsi_against],
        "Corsi %": [f"{corsi_pct} %"],
        "Fenwick For": [fenwick_for],
        "Fenwick Against": [fenwick_against],
        "Fenwick %": [f"{fenwick_pct} %"]
    }

    return pd.DataFrame(data)
