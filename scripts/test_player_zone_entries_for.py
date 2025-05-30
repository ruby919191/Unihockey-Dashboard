import sys
import os
import pandas as pd

# 🔧 Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📦 Import aus Analyse-Modul
from src.data_loader import get_season_games
from src.analysis.player_zone_entries_for import get_player_zone_entries

# 🔄 Daten laden
df = get_season_games("2024-25")

# 🧠 ZOE For pro Spieler analysieren
print("\n📊 Zone Entries For pro Spieler:")
print(get_player_zone_entries(df))
