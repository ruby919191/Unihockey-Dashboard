import streamlit as st
import sys
import os

def configure_layout():
    st.set_page_config(
        page_title="🏑 Unihockey Tigers Dashboard",
        layout="wide"
    )
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
