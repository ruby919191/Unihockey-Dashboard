import os
import pandas as pd

# Basisverzeichnis definieren (z. B. /Users/du/Desktop/Unihockey-Dashboard/src → eine Ebene rauf = Hauptordner)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, "..", "data")

def list_seasons():
    """
    Gibt alle verfügbaren Saison-Ordner in /data zurück.
    """
    return sorted([
        folder for folder in os.listdir(data_folder)
        if os.path.isdir(os.path.join(data_folder, folder))
    ])

def get_season_games(season):
    """
    Lädt alle CSV-Dateien für die gegebene Saison.
    Gibt einen zusammengefügten DataFrame zurück – bereinigt Mehrfacheinträge in 'Drittel'.
    """
    season_path = os.path.join(data_folder, season)
    if not os.path.exists(season_path):
        raise FileNotFoundError(f"Saisonordner nicht gefunden: {season_path}")

    dfs = []
    for file in os.listdir(season_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(season_path, file))
            df["game"] = os.path.splitext(file)[0]

            # ✅ Drittel-Spalte bereinigen, falls vorhanden
            if "Drittel" in df.columns:
                df["Drittel"] = df["Drittel"].astype(str).str.split(",").str[0].str.strip()

            dfs.append(df)

    if not dfs:
        raise ValueError(f"Keine CSV-Dateien gefunden in {season_path}")

    return pd.concat(dfs, ignore_index=True)
