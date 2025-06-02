import os
import shutil

# 📂 Verzeichnisse
source_dir = os.path.expanduser("~/Desktop/Analyse")
target_dir = os.path.abspath("assets/shotmaps/2024-25")

# 📷 Erwartete Bildnamen
original_names = [
    "Chance For.jpg",
    "Chance Against.jpg",
    "Tore For.jpg",
    "Tore Against.jpg"
]

# 🔁 Zieldateinamen
output_labels = [
    "Chances_For",
    "Chances_Against",
    "Tore_For",
    "Tore_Against"
]

# 🎮 Spiel-Liste (sortiert nach Datum)
game_ids = [
    "2024-09-28_vs_Chur",
    "2024-10-05_vs_Malans",
    "2024-10-06_vs_Uster",
    "2024-10-13_vs_FBK",
    "2024-10-27_vs_HCR",
    "2024-11-02_vs_FBTG",
    "2024-11-06_vs_GC",
    "2024-11-15_vs_CupFBTG",
    "2024-11-17_vs_Zug",
    "2024-11-23_vs_Basel",
    "2024-11-24_vs_SVWE",
    "2024-12-21_vs_Chur",
    "2025-01-08_vs_GC",
    "2025-01-11_vs_CupHCR",
    "2025-01-12_vs_Malans",
    "2025-01-18_vs_Uster",
    "2025-01-24_vs_FBK",
    "2025-02-08_vs_HCR",
    "2025-02-09_vs_FBTG",
    "2025-02-15_vs_WaSa",
    "2025-02-16_vs_Zug",
    "2025-03-02_vs_Basel",
    "2025-03-08_vs_PFVF1FBTG",
    "2025-03-12_vs_PFVF2FBTG",
    "2025-03-16_vs_PFVF3FBTG",
    "2025-03-20_vs_PFVF4FBTG",
    "2025-03-22_vs_PFVF5FBTG",
    "2025-04-03_vs_PFHF1FBK",
    "2025-04-06_vs_PFHF2FBK",
    "2025-04-10_vs_PFHF3FBK",
    "2025-04-12_vs_PFHF4FBK",
    "2025-04-16_vs_PFHF5FBK",
    "2025-04-27_vs_SFZug",
]

# 📁 Zielordner erstellen, falls nicht vorhanden
os.makedirs(target_dir, exist_ok=True)

print("\n🚀 Interaktiver Shotmap-Uploader gestartet\n")

# 🔁 Spielauswahl-Schleife
while True:
    print("📋 Verfügbare Spiele:")
    for idx, gid in enumerate(game_ids):
        print(f"  {idx+1:2d}) {gid}")
    print("  0) Beenden")

    choice = input("\nBitte Spielnummer eingeben: ")

    if choice == '0':
        print("👋 Beendet.")
        break

    try:
        selected = game_ids[int(choice)-1]
    except (IndexError, ValueError):
        print("❌ Ungültige Eingabe. Versuche es erneut.\n")
        continue

    # 🔍 Datei-Check
    current_files = os.listdir(source_dir)
    missing = [n for n in original_names if n not in current_files]
    if missing:
        print(f"⚠️ Fehlende Dateien in '{source_dir}':")
        for m in missing:
            print(f"   - {m}")
        input("❗Bitte korrigiere das und drücke Enter...")
        continue

    # 💾 Bilder kopieren & umbenennen
    for orig, label in zip(original_names, output_labels):
        src = os.path.join(source_dir, orig)
        dst = os.path.join(target_dir, f"{selected}_{label}.jpg")
        shutil.copyfile(src, dst)
        print(f"✔️  Gespeichert: {dst}")

    # 🧹 Rohbilder löschen
    for orig in original_names:
        os.remove(os.path.join(source_dir, orig))

    print("🧹 Analyse-Ordner geleert.\n")
