import os
import re
import numpy as np
import pandas as pd
from src.data_loader import (
    safe_read_csv, standardize_columns,
    clean_first_value, columns_to_clean,list_seasons
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, "..", "data")

def clean_numeric_column(df, col_name):
    if col_name in df.columns:
        df[col_name] = df[col_name].replace('', np.nan)
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    return df

def load_single_game(spielname: str) -> pd.DataFrame:
    print(f"load_single_game called with spielname={spielname}")
    for season in list_seasons():
        season_path = os.path.join(data_folder, season)
        for root, _, files in os.walk(season_path):
            for file in files:
                if not file.endswith(".csv"):
                    continue
                if os.path.splitext(file)[0] == spielname:
                    path = os.path.join(root, file)
                    df = safe_read_csv(path)
                    if df.empty:
                        return pd.DataFrame()

                    df = standardize_columns(df)
                    df["game"] = spielname
                    df["season"] = "Einzelansicht"

                    if season == "Divers":
                        pattern = r'^\d{4}-\d{2}-\d{2}_([A-Za-zÄÖÜäöüß]+)_vs_([A-Za-zÄÖÜäöüß]+)$'
                        match = re.match(pattern, spielname)
                        if match:
                            df["team_for"] = match.group(1)
                            df["team_against"] = match.group(2)
                        else:
                            df["team_for"] = "Unbekannt"
                            df["team_against"] = "Unbekannt"
                    else:
                        pattern = r'^\d{4}-\d{2}-\d{2}_vs_([A-Za-zÄÖÜäöüß]+)$'
                        match = re.match(pattern, spielname)
                        df["team_for"] = "Tigers"
                        df["team_against"] = match.group(1) if match else "Unbekannt"

                    df = clean_first_value(df, columns_to_clean)

                    # Hier die problematischen Spalten bereinigen
                    for col in ['Wert', '% Auf Tor', '%']:
                        df = clean_numeric_column(df, col)

                    return df
    return pd.DataFrame()
