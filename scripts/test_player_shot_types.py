import sys
import os
import pandas as pd

# 🛠 Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📦 Importiere deine brillante Analysefunktion
from src.data_loader import get_season_games
from src.analysis.player_shot_types import get_shot_types_by_player

# 📅 Daten abrufen
df = get_season_games("2024-25")

# 📊 Schussarten-Pivot anzeigen
print("\n🎯 Pivot-Tabelle: Schussarten pro Spieler:")
print(get_shot_types_by_player(df))
