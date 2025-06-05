import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, "..", "data")

def clean_first_value(df, columns):
    """
    Für jede Spalte in `columns` wird nur der erste Wert vor einem Komma behalten.
    """
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.split(",")
                .str[0]
                .str.strip()
                .replace("nan", pd.NA)  # ersetzt nur string "nan"
            )
    return df

def standardize_columns(df):
    """
    Entfernt Leerzeichen & vereinheitlicht Spaltennamen.
    """
    df.columns = df.columns.str.strip()
    return df

def safe_read_csv(path):
    """
    Liest CSV-Datei ein, fängt Fehler ab, gibt leeres DF bei Problemen.
    """
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

def get_season_games(season):
    season_path = os.path.join(data_folder, season)
    if not os.path.exists(season_path):
        raise FileNotFoundError(f"Saisonordner nicht gefunden: {season_path}")

    dfs = []
    for file in os.listdir(season_path):
        if file.endswith(".csv"):
            path = os.path.join(season_path, file)
            df = safe_read_csv(path)
            if df.empty:
                continue

            df = standardize_columns(df)
            df["game"] = os.path.splitext(file)[0]

            # Spalten, bei denen nur der erste Wert vor einem Komma behalten werden soll
            columns_to_clean = [
                "Spieler Tigers", "Spieler Tigers 2", "Taktische Spielsituation",
                "Nummerische Spielsituation", "XG", "ZOE For", "ZOE Against", "Action",
                "Drittel", "Linien For", "Linien Against"  # ✅ NEU
            ]
            df = clean_first_value(df, columns_to_clean)

            dfs.append(df)

    if not dfs:
        raise ValueError(f"Keine gültigen CSV-Dateien gefunden in {season_path}")

    return pd.concat(dfs, ignore_index=True)
