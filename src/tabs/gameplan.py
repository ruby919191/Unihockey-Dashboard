import streamlit as st
import matplotlib.pyplot as plt
from src.analysis.gameplan_momentum import calculate_momentum_by_game, plot_momentum_chart
from src.analysis.gameplan_corsi_fenwick import calculate_corsi_fenwick

def render_gameplan_tab(df):
    st.subheader("📈 Momentum pro Spiel")

    # Tabelle (z. B. bei Saisonansicht trotzdem sichtbar)
    st.dataframe(calculate_momentum_by_game(df), use_container_width=True)

    # Momentum Chart (einzelnes Spiel)
    if df["Spiel"].nunique() == 1:
        spiel_name = df["Spiel"].iloc[0]
        st.markdown(f"### 📊 Momentum Chart – {spiel_name}")
        fig = plot_momentum_chart(df, spiel_name)
        fig.set_dpi(120)  # Bild kleiner rendern
        st.pyplot(fig, use_container_width=False)  # Containerbreite deaktivieren
    else:
        st.info("Bitte ein einzelnes Spiel filtern, um das Momentum-Diagramm anzuzeigen.")

    st.subheader("🔁 Corsi & Fenwick")
    st.dataframe(calculate_corsi_fenwick(df), use_container_width=True)
