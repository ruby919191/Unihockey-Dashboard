import streamlit as st
import sys
import os

def configure_layout():
    """
    Führt grundlegende Einstellungen und Konfigurationen für die Streamlit-App durch:
    - Setzt das Seitenlayout (wide)
    - Ergänzt den Projektpfad, damit Module aus /src gefunden werden
    """
    st.set_page_config(
        page_title="🏑 Unihockey Tigers Dashboard",
        layout="wide"
    )

    # Pfad zu /src ergänzen
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
