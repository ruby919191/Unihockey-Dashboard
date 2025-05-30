import sys
import os
import pandas as pd

# 🔧 Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Richtiger Import für dein Genie
from src.data_loader import get_season_games
from src.analysis.player_chances_by_high_mid import get_high_mid_chances_by_player

# 🔄 Daten laden
df = get_season_games("2024-25")

# 📊 High- und Mid-Q Chancen pro Spieler anzeigen
print("\n📊 High- und Mid-Q Chancen pro Spieler:")
print(get_high_mid_chances_by_player(df))
