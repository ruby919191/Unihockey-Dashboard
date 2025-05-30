import sys
import os
import pandas as pd

# 🛠 Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📦 Daten und Analyse importieren
from src.data_loader import get_season_games
from src.analysis.gameplan_momentum import calculate_momentum_by_game

# 🔄 Daten laden
df = get_season_games("2024-25")

# 📊 Momentum berechnen und anzeigen
print("\n📊 Chancen-Momentum pro Spiel:")
print(calculate_momentum_by_game(df))
