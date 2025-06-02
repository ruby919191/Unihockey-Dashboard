import os

# ⚙️ Einstellungen
folder = os.path.abspath("assets/shotmaps/2024-25")
expected_labels = [
    "Chances_For", "Chances_Against", "Tore_For", "Tore_Against"
]

# 🔁 Spiel-IDs (aus vorherigem Prozess oder aus Dateinamen extrahieren)
game_ids = sorted(set(
    "_".join(filename.split("_")[:3])
    for filename in os.listdir(folder)
    if filename.endswith(".jpg")
))

print(f"🔍 Überprüfe {len(game_ids)} Spiele im Ordner: {folder}")

# ✅ Check pro Spiel
for game_id in game_ids:
    print(f"\n🎮 {game_id}")
    for label in expected_labels:
        expected_file = f"{game_id}_{label}.jpg"
        if not os.path.exists(os.path.join(folder, expected_file)):
            print(f"   ❌ Fehlt: {expected_file}")
        else:
            print(f"   ✔️ {expected_file} vorhanden")
