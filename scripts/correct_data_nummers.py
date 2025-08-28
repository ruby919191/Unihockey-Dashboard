import pandas as pd
import os

# 🧭 Benutzer nach Pfad fragen
csv_path = input("🔍 Gib den Pfad zur CSV-Datei ein: ").strip()

# ✅ Datei prüfen
if not os.path.isfile(csv_path):
    raise FileNotFoundError(f"❌ Datei nicht gefunden: {csv_path}")

# 📥 CSV laden
df = pd.read_csv(csv_path)

if "Action" not in df.columns:
    raise ValueError("❌ Die Spalte 'Action' ist nicht im CSV enthalten.")

# 🧠 Zähler
action_counts = {}
new_actions = []

for action in df["Action"]:
    if ":" in action:
        new_actions.append(action)  # schon nummeriert
    else:
        base = action.strip()
        count = action_counts.get(base, 0) + 1
        action_counts[base] = count
        new_actions.append(f"{base}: {count}")

# 🔄 Spalte aktualisieren
df["Action"] = new_actions

# 💾 Speichern
df.to_csv(csv_path, index=False)

print(f"✅ CSV erfolgreich überschrieben: {csv_path}")
