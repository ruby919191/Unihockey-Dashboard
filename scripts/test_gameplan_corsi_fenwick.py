import sys
import os
import pandas as pd

# Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.gameplan_corsi_fenwick import calculate_corsi_fenwick

# Daten laden
df = get_season_games("2024-25")

print("\n📊 Corsi & Fenwick Analyse:")
print(calculate_corsi_fenwick(df))
