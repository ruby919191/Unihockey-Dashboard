import sys
import os
import pandas as pd

# Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.zone_entries_for import (
    get_zone_entries_for,
    count_zone_entries_by_quality,
    count_zone_entries_by_period,
    count_zone_entries_by_line
)

# Daten laden
df = get_season_games("2024-25")

print("\n📥 Alle Zone Entries For:")
print(get_zone_entries_for(df))

print("\n📊 Zone Entries For nach Qualität (Good/Bad):")
print(count_zone_entries_by_quality(df))

print("\n📊 Zone Entries For pro Drittel:")
print(count_zone_entries_by_period(df))

print("\n📊 Zone Entries For pro Linie:")
print(count_zone_entries_by_line(df))
