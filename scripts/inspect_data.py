import pandas as pd

# 🔄 Pfad zur Beispiel-CSV
file_path = "data/2024-25/2024-09-14_vs_SVWE.csv"

# 📥 CSV einlesen
df = pd.read_csv(file_path)

# 🔎 Erste Zeilen anzeigen
print("HEAD:")
print(df.head())

# 🔤 Spaltennamen prüfen
print("\nCOLUMNS:")
print(df.columns)

# 🧪 Datentypen prüfen
print("\nDATATYPES:")
print(df.dtypes)

# ❓ Fehlende Werte prüfen
print("\nMISSING VALUES:")
print(df.isnull().sum())

# 📏 Zeilenanzahl
print(f"\nTOTAL ROWS: {len(df)}")

