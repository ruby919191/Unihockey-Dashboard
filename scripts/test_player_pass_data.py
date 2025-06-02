import sys
import os
import pandas as pd
import os
print("Aktueller Arbeitsordner:", os.getcwd())


# 📦 Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📥 Datenimport
from src.data_loader import get_season_games
from src.analysis.player_pass_data import get_players_from_chances_for

# 🔄 Daten laden
df = get_season_games("2024-25")

# 🧪 Spaltenübersicht anzeigen (optional zum Debuggen)
print("\n🧪 Spaltenübersicht:", df.columns.tolist())

# 📊 Spielerbeteiligung aus Spalte "Spieler Tigers 2"
print("\n📊 Spielerbeteiligung bei Chancen For (Spieler Tigers 2):")
print(get_players_from_chances_for(df))
