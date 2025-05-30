import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.goals import (
    get_game_goals,
    get_team_goals_with_situation,
    get_opponent_goals_with_situation,
    get_goal_situation_counts,
    get_opponent_goal_situation_counts
)

# Daten laden
df = get_season_games("2024-25")

print("🟢 Tore im Spiel (gesamt):")
print(get_game_goals(df, "Tigers", "Gegner"))

print("\n🟢 Tigers-Tore (nur 5:5) mit taktischer Spielsituation:")
print(get_team_goals_with_situation(df, "Tigers"))

print("\n🔴 Gegner-Tore (nur 5:5) mit taktischer Spielsituation:")
print(get_opponent_goals_with_situation(df))

print("\n📊 Anzahl 5:5-Tore Tigers pro taktischer Spielsituation:")
print(get_goal_situation_counts(df, "Tigers").to_string(index=False))

print("\n📊 Anzahl 5:5-Gegentore pro taktischer Spielsituation:")
print(get_opponent_goal_situation_counts(df).to_string(index=False))
