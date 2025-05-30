import sys
import os
import pandas as pd

# 🔧 Pfad zur src hinzufügen, damit du nicht wieder in ein Import-Loch fällst
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📦 Importiere wie ein Profi
from src.data_loader import get_season_games
from src.analysis.gameplan_kpi_summary import generate_kpi_summary

# 🔄 Daten herholen
df = get_season_games("2024-25")

# 📊 KPIs anzeigen, damit dein Dashboard auch mal Eindruck macht
print("\n📊 Gameplan KPI Summary:")
print(generate_kpi_summary(df))
