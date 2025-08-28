import streamlit as st
from src.analysis.goals import (
    get_goal_situation_counts,
    get_opponent_goal_situation_counts,
    get_plus_minus_line_table
)
from src.analysis.gameplan_save_percentage import calculate_dynamic_save_percentages


def render_tore_tab(df, team_for_name, team_against_name):
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

    # --- Tore & Gegentore nebeneinander ---
    col1, col2 = st.columns(2)
    with col1:
        table_box(f"🟢 Tore {team_for_name} (5:5, taktisch)", get_goal_situation_counts(df, team_for_name), "#dff0d8")
    with col2:
        table_box(f"🔴 Gegentore {team_against_name} (5:5, taktisch)", get_opponent_goal_situation_counts(df), "#f2dede")

    # --- Save Percentage ---
    st.markdown("---")
    save_df = calculate_dynamic_save_percentages(df, team_for_name, team_against_name)
    table_box("🧤 Save Percentage", save_df, "#f5f5f5")

    col_for = f"Save % {team_for_name}"
    col_against = f"Save % {team_against_name}"

    if not save_df.empty and col_for in save_df.columns and col_against in save_df.columns:
        last_game = save_df.iloc[-1]
        tigers_sv = last_game.get(col_for)
        opp_sv = last_game.get(col_against)

        if tigers_sv is not None and opp_sv is not None:
            if tigers_sv > opp_sv:
                st.success(f"🟢 {team_for_name} Goalie war stärker: {tigers_sv:.1f}% vs. {opp_sv:.1f}%")
            elif tigers_sv < opp_sv:
                st.error(f"🔴 Gegnerischer Goalie war stärker: {opp_sv:.1f}% vs. {tigers_sv:.1f}%")
            else:
                st.info(f"⚖️ Gleichstand: Beide Save % bei {tigers_sv:.1f}%")
        else:
            st.warning("Nicht genügend Daten zur Save %-Analyse.")
    else:
        st.warning("Keine Save %-Daten verfügbar.")

    # --- Linien-Bilanz ---
    st.markdown("---")
    table_box("➕➖ Linien-Bilanz bei 5:5", get_plus_minus_line_table(df), "#f5f5f5")
