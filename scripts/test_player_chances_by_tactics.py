import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.player_chances_by_tactics import count_player_chances_by_tactics

# 🔄 Daten laden
df = get_season_games("2024-25")

# 📊 Chancen pro Spieler und Taktik
print("\n📊 Chancen pro Spieler (eine Zeile pro Spieler, Spalten = Taktiken):")
print(count_player_chances_by_tactics(df).to_string(index=False))
