import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.player_chances_by_tactics import count_player_chances_by_tactics

df = get_season_games("2024-25")

print("\n📊 Chancen pro Spieler pro Taktische Spielsituation:")
print(count_player_chances_by_tactics(df).to_string(index=False))
