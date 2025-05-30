import sys
import os
import pandas as pd

# Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.chances_for import (
    get_chances_for,
    count_chances_by_quality,
    count_chances_by_line,
    count_chances_by_period
)

# 🔄 Daten laden
df = get_season_games("2024-25")

# 🔍 Alle Chancen auflisten
print("\n🟢 Chancen Tigers (alle Einträge mit 'Chance For'):")
print(get_chances_for(df))

# 📊 Auswertung nach Qualität
print("\n📊 Chancen nach Qualität:")
print(count_chances_by_quality(df))

print("\n📊 Chancen nach Linie:")
print(count_chances_by_line(df))

# 📊 Auswertung nach Drittel
print("\n📊 Chancen pro Drittel:")
print(count_chances_by_period(df))