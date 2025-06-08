import streamlit as st
import os
from PIL import Image

def render_shotmaps_tab(selected_game, selected_season):
    st.subheader("🗺️ Shotmaps")

    if not selected_game or not selected_season:
        st.warning("Bitte genau ein Spiel auswählen, um Shotmaps zu sehen.")
        return

    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.abspath(os.path.join(base_path, "..", ".."))
    shotmap_dir = os.path.join(base_path, "assets", "shotmaps", selected_season)

    if not os.path.exists(shotmap_dir):
        st.error(f"❌ Verzeichnis existiert nicht: {shotmap_dir}")
        return

    try:
        all_files = os.listdir(shotmap_dir)
    except Exception as e:
        st.error(f"Fehler beim Lesen des Ordners: {e}")
        return

    labels = ["Chances_For", "Chances_Against", "Tore_For", "Tore_Against"]
    cols = st.columns(2)
    images_found = False

    for i, label in enumerate(labels):
        pattern_prefix = f"{selected_game}_"
        pattern_suffix = f"_{label}.jpg"

        matched_files = [
            file for file in all_files
            if file.startswith(pattern_prefix) and file.endswith(pattern_suffix)
        ]

        if matched_files:
            image_path = os.path.join(shotmap_dir, matched_files[0])
            try:
                image = Image.open(image_path)
                cols[i % 2].image(image, caption=label.replace("_", " "), use_container_width=True)
                images_found = True
            except Exception as e:
                cols[i % 2].error(f"Fehler beim Laden von {matched_files[0]}: {e}")

    if not images_found:
        st.info("Keine Shotmap-Bilder gefunden. Bitte Game-ID und Dateinamen prüfen.")
