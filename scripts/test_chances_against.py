import sys
import os
import pandas as pd

# 📂 Projektstruktur einbinden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📥 Daten
from src.data_loader import get_season_games
from src.analysis.chances_against import (
    get_chances_against,
    count_chances_by_quality,
    count_chances_by_line,
    count_chances_by_period,
    count_chances_by_tactical_situation,
    count_chances_by_tactical_situation_detailed
)

# 🔄 Daten laden
df = get_season_games("2024-25")

# 🟠 Chancen Against
print("\n🟠 Chancen Gegner (alle Einträge mit 'Chance Against'):")
print(get_chances_against(df).head())

# 📊 Auswertung nach Qualität
print("\n📊 Chancen Against nach Qualität:")
print(count_chances_by_quality(df).to_string(index=False))

# 📊 Auswertung nach Linie
print("\n📊 Chancen Against nach Linie:")
print(count_chances_by_line(df).to_string(index=False))

# 📊 Auswertung nach Drittel
print("\n📊 Chancen Against pro Drittel:")
print(count_chances_by_period(df).to_string(index=False))

# 📊 Anzahl Chancen pro taktische Spielsituation
print("\n📊 Chancen Against pro taktische Spielsituation:")
print(count_chances_by_tactical_situation(df).to_string(index=False))

# 📊 Erweiterte Analyse: 5:5 Chancen nach Qualität & Situation
print("\n📊 Detaillierte Chancen Against bei 5:5 nach taktischer Spielsituation:")
print(count_chances_by_tactical_situation_detailed(df).to_string(index=False))
