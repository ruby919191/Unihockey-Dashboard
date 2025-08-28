import streamlit as st
from src.analysis.zone_entries_for import (
    count_zone_entries_by_quality as zoe_for_quality,
    count_zone_entries_by_period as zoe_for_period,
    count_zone_entries_by_line as zoe_for_line
)
from src.analysis.zone_entries_against import (
    count_zone_entries_against_by_quality as zoe_against_quality,
    count_zone_entries_against_by_period as zoe_against_period,
    count_zone_entries_against_by_line as zoe_against_line
)
from src.analysis.player_zone_entries_for import get_player_zone_entries


def render_zone_entries_tab(df, team_for_name, team_against_name):
    # CSS für Tabellen (gleich wie bei Chancen/Tore)
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
        "🔎 Wähle eine KPI-Kategorie:",
        [
            "Zone-Entries",
            "Zone-Entries nach Drittel",
            "Zone-Entries nach Linien",
            "Zone-Entries nach Spielern"
        ],
        index=0,
        key="zoe_selectbox"
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
    if option == "Zone-Entries":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"📥 ZOE For - {team_for_name}", zoe_for_quality(df), "#dff0d8")
        with col2:
            table_box(f"📤 ZOE Against - {team_against_name}", zoe_against_quality(df), "#f2dede")

    elif option == "Zone-Entries nach Drittel":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"📊 ZOE nach Drittel (For - {team_for_name})", zoe_for_period(df), "#f5f5f5")
        with col2:
            table_box(f"📊 ZOE nach Drittel (Against - {team_against_name})", zoe_against_period(df), "#f5f5f5")

    elif option == "Zone-Entries nach Linien":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"📋 ZOE nach Linie (For - {team_for_name})", zoe_for_line(df), "#f5f5f5")
        with col2:
            table_box(f"📋 ZOE nach Linie (Against - {team_against_name})", zoe_against_line(df), "#f5f5f5")

    elif option == "Zone-Entries nach Spielern":
        table_box("🧍‍♂️ Zonen Entries Spieleraktivität", get_player_zone_entries(df), "#f5f5f5")
