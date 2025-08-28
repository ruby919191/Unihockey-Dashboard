import streamlit as st

from src.analysis.chances_for import (
    count_chances_by_quality as chances_for_quality,
    count_chances_by_line as chances_for_line,
    count_chances_by_period as chances_for_period,
    count_chances_by_tactical_situation_detailed as chances_for_tactics,
    count_pp_shots_for as count_pp_shots_for
)

from src.analysis.chances_against import (
    count_chances_by_quality as chances_against_quality,
    count_chances_by_line as chances_against_line,
    count_chances_by_period as chances_against_period,
    count_chances_by_tactical_situation_detailed as chances_against_tactics,
    count_pp_shots_against as count_pp_shots_against   
)


def render_chancen_tab(df, team_for_name, team_against_name):
    # CSS für einheitliches Table-Styling
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
            background-color: #f0f0f0;
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
            background-color: #fafafa;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Filter-Auswahl
    option = st.selectbox(
        "🔎 Wähle eine KPI-Kategorie:",
        [
            "Chancen",
            "Chancen nach Linien",
            "Chancen nach Drittel",
            "Chancen nach Spielsituation",
            "PP Chancen"
        ],
        index=0,  # Default = Erste Kategorie
        key="chancen_selectbox"
    )

    # Helper-Funktion für Boxen
    def table_box(title, df, color="#f5f5f5"):
        html_table = df.to_html(classes="styled-table")
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

    # Inhalte je nach Filter
    if option == "Chancen":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"🟢 Chancen {team_for_name}", chances_for_quality(df), "#e8f5e9")
        with col2:
            table_box(f"🔴 Chancen {team_against_name}", chances_against_quality(df), "#ffebee")

    elif option == "Chancen nach Linien":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"📊 Chancen nach Linie (For - {team_for_name})", chances_for_line(df))
        with col2:
            table_box(f"📊 Chancen nach Linie (Against - {team_against_name})", chances_against_line(df))

    elif option == "Chancen nach Drittel":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"📊 Chancen pro Drittel (For - {team_for_name})", chances_for_period(df))
        with col2:
            table_box(f"📊 Chancen pro Drittel (Against - {team_against_name})", chances_against_period(df))

    elif option == "Chancen nach Spielsituation":
        col1, col2 = st.columns(2)
        with col1:
            table_box(f"📋 Chancen For nach Taktik (5:5 - {team_for_name})", chances_for_tactics(df))
        with col2:
            table_box(f"📋 Chancen Against nach Taktik (5:5 - {team_against_name})", chances_against_tactics(df))

    elif option == "PP Chancen":
        col1, col2 = st.columns(2)
        with col1:
            table_box("🟪 PP Shots For", count_pp_shots_for(df))
        with col2:
            table_box("🟪 PP Shots Against", count_pp_shots_against(df))
