import sys
import os
import pandas as pd

# Pfad zur src hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import get_season_games
from src.analysis.zone_entries_against import (
    get_zone_entries_against,
    count_zone_entries_against_by_quality,
    count_zone_entries_against_by_period,
    count_zone_entries_against_by_line
)

# Daten laden
df = get_season_games("2024-25")

print("\n📥 Alle Zone Entries Against:")
print(get_zone_entries_against(df))

print("\n📊 Zone Entries Against nach Qualität (Good/Bad):")
print(count_zone_entries_against_by_quality(df))

print("\n📊 Zone Entries Against pro Drittel:")
print(count_zone_entries_against_by_period(df))

print("\n📊 Zone Entries Against pro Linie:")
print(count_zone_entries_against_by_line(df))
