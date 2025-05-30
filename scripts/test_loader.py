import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import list_seasons, get_season_games

print("Script läuft!")  # Sicherheitslinie

# 🔎 Alle verfügbaren Saisons auflisten
saisons = list_seasons()
print("Verfügbare Saisons:", saisons)

# ✅ Beispiel: Saison 2024-25 laden
df = get_season_games("2024-25")

print("\nHEAD:")
print(df.head())

print("\nSPALTEN:")
print(df.columns)

print("\nUNIQUE GAMES:")
print(df["game"].unique())

print("\nUNIQUE SAISONS:")
print(df["season"].unique())


