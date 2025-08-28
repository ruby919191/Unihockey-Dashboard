import streamlit as st
from src.analysis.player_chances_for import get_chances_by_player
from src.analysis.player_chances_by_tactics import count_player_chances_by_tactics
from src.analysis.player_chances_by_high_mid import get_high_mid_chances_by_player
from src.analysis.player_shot_types import get_shot_types_by_player
from src.analysis.player_pass_data import get_player_pass_participation


def render_player_data_tab(df, team_for_name):
    # CSS für Tabellen
    st.markdown(
        """
        <style>
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            font-family: Arial, sans-serif;
        }
        .styled-table th {
            background-color: rgba(0,0,0,0.05);
            padding: 8px;
            text-align: center;
            border-bottom: 2px solid #ddd;
        }
        .styled-table td {
            padding: 8px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        .styled-table tr:nth-child(even) {
            background-color: rgba(255,255,255,0.5);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Filter-Auswahl
    option = st.selectbox(
        "🔎 Wähle eine Spieler-Kategorie:",
        [
            "Chancen pro Spieler",
            "Chancen nach Spielsituation",
            "High/Mid Q Chancen",
            "Schusstypen",
            "Spielerbeteiligung"
        ],
        index=0,
        key="playerdata_selectbox"
    )

    # Helper-Funktion für Boxen
    def table_box(title, df, color="#f5f5f5"):
        html_table = df.to_html(classes="styled-table", index=False)
        st.markdown(
            f"""
            <div style="
                border-radius:10px;
                padding:15px;
                margin-bottom:15px;
                background-color:{color};
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            ">
                <h4 style="margin-top:0;margin-bottom:10px;">{title}</h4>
                {html_table}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Inhalte je nach Auswahl
    if option == "Chancen pro Spieler":
        table_box(f"🎯 Chancen pro Spieler - {team_for_name}", get_chances_by_player(df), "#dff0d8")  # hellgrün

    elif option == "Chancen nach Spielsituation":
        table_box(f"🧠 Chancen nach Spielsituation - {team_for_name}", count_player_chances_by_tactics(df), "#f5f5f5")

    elif option == "High/Mid Q Chancen":
        table_box(f"📐 High/Mid Q Chancen - {team_for_name}", get_high_mid_chances_by_player(df), "#f5f5f5")

    elif option == "Schusstypen":
        table_box(f"🥍 Schusstypen pro Spieler - {team_for_name}", get_shot_types_by_player(df), "#f5f5f5")

    elif option == "Spielerbeteiligung":
        table_box(f"🤝 Spielerbeteiligung bei Chancen - {team_for_name}", get_player_pass_participation(df), "#f5f5f5")
