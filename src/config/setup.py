import streamlit as st
import sys
import os

def configure_app():
    """
    Führt grundlegende Einstellungen und Konfigurationen für die Streamlit-App durch:
    - Setzt das Seitenlayout und den Titel
    - Fügt das übergeordnete Verzeichnis zum Python-Pfad hinzu
    """
    st.set_page_config(page_title="🏑 Unihockey Dashboard", layout="wide")
    st.title("🏑 Unihockey Tigers Dashboard")

    # Projektpfad ergänzen, damit src-Module gefunden werden
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
