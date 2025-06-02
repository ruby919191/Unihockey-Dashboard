import os
import glob
from PIL import Image

# 📁 Pfad zum Analyse-Ordner
source_dir = os.path.expanduser("~/Desktop/Analyse")

# 🎯 Ziel-Dateinamen (alle mit .jpg Endung)
new_names = [
    "Tore For.jpg",
    "Chance For.jpg",
    "Tore Against.jpg",
    "Chance Against.jpg"
]

# 🔍 Unterstützte Bildformate
image_extensions = ("*.jpg", "*.jpeg", "*.png")

# 📦 Alle Bilder sammeln
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(source_dir, ext)))

# 🕓 Neueste zuerst
image_files.sort(key=os.path.getmtime, reverse=True)

# ✅ Nur die letzten 4 nehmen
recent_images = image_files[:4]

if len(recent_images) < 4:
    print("⚠️ Weniger als 4 Bilder gefunden. Bitte prüfen.")
    exit()

# 🔄 Bilder umbenennen und konvertieren (falls nötig)
for i, (old_path, new_name) in enumerate(zip(recent_images, new_names)):
    new_path = os.path.join(source_dir, new_name)

    # 📸 Öffne das Bild und speichere es neu als JPG (konvertiert falls nötig)
    try:
        with Image.open(old_path) as img:
            rgb_img = img.convert("RGB")  # PNG → JPG falls nötig
            rgb_img.save(new_path, format="JPEG")
        os.remove(old_path)
        print(f"✔️ Bild {i+1} gespeichert als: {new_name}")
    except Exception as e:
        print(f"❌ Fehler bei Bild {old_path}: {e}")

print("\n✅ Alle 4 Bilder wurden als JPG gespeichert und korrekt benannt.")
