import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, "..", "data")

columns_to_clean = [
    "Spieler Tigers", "Spieler Tigers 2" "Schusslabel", "Schussmetrik", "Taktische Spielsituation",
    "Nummerische Spielsituation", "XG", "ZOE For", "ZOE Against",
    "Drittel", "Linien For", "Linien Against"
]

def clean_first_value(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.split(",")
                .str[0]
                .str.strip()
                .replace("nan", pd.NA)
            )
    return df

def standardize_columns(df):
    df.columns = df.columns.str.strip()
    return df

def safe_read_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"⚠️ Fehler beim Einlesen von {path}: {e}")
        return pd.DataFrame()

def list_seasons():
    return sorted([
        folder for folder in os.listdir(data_folder)
        if os.path.isdir(os.path.join(data_folder, folder))
    ])

def get_all_games():
    all_data = []
    for season in list_seasons():
        season_path = os.path.join(data_folder, season)
        for root, _, files in os.walk(season_path):
            for file in files:
                if file.endswith(".csv"):
                    path = os.path.join(root, file)
                    df = safe_read_csv(path)
                    if df.empty:
                        continue

                    df = standardize_columns(df)

                    # 🟢 Action-Spalte NaN-safe machen
                    if "Action" in df.columns:
                        df["Action"] = df["Action"].fillna("NA").astype(str)

                    df["game"] = os.path.splitext(file)[0]
                    df["season"] = season.strip()

                    rel_path = os.path.relpath(root, season_path)
                    subfolder_name = rel_path if rel_path != "." else "Root"
                    df["subfolder"] = subfolder_name

                    # Nur für Season "Divers": Teams aus Dateiname extrahieren
                    if df["season"].iloc[0] == "Divers":
                        pattern = r'^(\d{4}-\d{2}-\d{2})_vs_([^_]+)_([^_]+)$'
                        match = re.match(pattern, df["game"].iloc[0])
                        if match:
                            df["team_for"] = match.group(2)
                            df["team_against"] = match.group(3)
                        else:
                            df["team_for"] = "Team For"
                            df["team_against"] = "Team Against"

                    df = clean_first_value(df, columns_to_clean)
                    all_data.append(df)

    if not all_data:
        raise ValueError("Keine gültigen CSV-Dateien gefunden in den Datenordnern.")

    return pd.concat(all_data, ignore_index=True)
