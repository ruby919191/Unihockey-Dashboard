import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

def extract_event_count(action_str, event_name):
    if not isinstance(action_str, str):
        return 0
    pattern = rf"{re.escape(event_name)}: (\d+)"
    match = re.search(pattern, action_str)
    if match:
        return int(match.group(1))
    else:
        # Wenn Event ohne Zahl vorkommt, zähle als 1
        if event_name in action_str:
            return 1
    return 0

def add_event_columns(df):
    events = [
        "ZOE For",
        "ZOE Against",
        "Low Q Chance For",
        "Low Q Chance Against",
        "Mid Q Chance For",
        "Mid Q Chance Against",
        "High Q Chance For",
        "High Q Chance Against",
    ]

    # Tore: Unterscheidung Divers vs Saison
    # Für Divers: team_for, team_against
    # Für Saison: Tigers, Gegner
    def count_goals(row, team, prefix):
        if not isinstance(row["Action"], str):
            return 0
        # Beispiel: "Tor Tigers: 1" oder "Tor team_for: 2"
        # Falls Divers, suche Tor team_for bzw. Tor team_against
        if row["season"] == "Divers":
            event_name = f"Tor {row[team]}"
        else:
            event_name = f"Tor {prefix}"
        return extract_event_count(row["Action"], event_name)

    df = df.copy()

    for event in events:
        df[event] = df["Action"].apply(lambda x: extract_event_count(x, event))

    # Tore Tigers / team_for
    df["Tor For"] = df.apply(lambda row: count_goals(row, "team_for", "Tigers"), axis=1)
    # Tore Gegner / team_against
    df["Tor Against"] = df.apply(lambda row: count_goals(row, "team_against", "Gegner"), axis=1)

    return df

def filter_data_for_trends(all_df, selected_ligas):
    # L-UPL = alle Saisons außer Divers
    if "L-UPL" in selected_ligas:
        df_filtered = all_df[(all_df["season"] != "Divers") | (all_df["league"] == "L-UPL")]
        other_ligas = [liga for liga in selected_ligas if liga != "L-UPL"]
        if other_ligas:
            df_filtered = pd.concat([
                df_filtered,
                all_df[all_df["league"].isin(other_ligas)]
            ]).drop_duplicates()
    else:
        df_filtered = all_df[all_df["league"].isin(selected_ligas)]
    return df_filtered

def safe_startswith(value, prefix):
    if isinstance(value, str):
        return value.startswith(prefix)
    return False

def plot_event_sums(event_sums, title="Summe der Events"):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(event_sums.keys()),
        y=list(event_sums.values()),
        text=list(event_sums.values()),
        textposition='auto'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Event-Kategorie",
        yaxis_title="Anzahl",
        yaxis=dict(tickformat="d"),
        template="plotly_white",
        height=400
    )

    return fig

def aggregate_events(df):
    event_cols = [
        "ZOE For",
        "Low Q Chance For",
        "Mid Q Chance For",
        "High Q Chance For",
        "Tor For",       # neu
        "ZOE Against",
        "Low Q Chance Against",
        "Mid Q Chance Against",
        "High Q Chance Against",
        "Tor Against"    # neu
    ]
    event_sums = {col: df[col].sum() for col in event_cols}
    return event_sums

def render_event_summary_chart(df):
    event_sums = aggregate_events(df)
    fig = plot_event_sums(event_sums, title="Summe der Events For & Against")
    st.plotly_chart(fig, use_container_width=True)

    # Total Events For / Against
    total_for = sum(event_sums[col] for col in ["ZOE For", "Low Q Chance For", "Mid Q Chance For", "High Q Chance For", "Tor For"])
    total_against = sum(event_sums[col] for col in ["ZOE Against", "Low Q Chance Against", "Mid Q Chance Against", "High Q Chance Against", "Tor Against"])

    # Balkendiagramm Total For / Against
    total_fig = go.Figure()
    total_fig.add_trace(go.Bar(
        x=["Total Events For", "Total Events Against"],
        y=[total_for, total_against],
        text=[total_for, total_against],
        textposition='auto'
    ))
    total_fig.update_layout(
        title="Total Events For vs. Against",
        yaxis_title="Anzahl",
        template="plotly_white",
        height=300
    )
    st.plotly_chart(total_fig, use_container_width=True)

def render_event_summary_box(df_summary):
    # Berechne Total Events For & Against pro Spiel
    df_summary["Total Events For"] = df_summary[[
        "ZOE For",
        "Low Q Chance For",
        "Mid Q Chance For",
        "High Q Chance For",
        "Tor For"
    ]].sum(axis=1)

    df_summary["Total Events Against"] = df_summary[[
        "ZOE Against",
        "Low Q Chance Against",
        "Mid Q Chance Against",
        "High Q Chance Against",
        "Tor Against"
    ]].sum(axis=1)

    sieg_df = df_summary[df_summary["Ergebnis"] == "Sieg"]
    nicht_sieg_df = df_summary[df_summary["Ergebnis"] != "Sieg"]

    median_for_sieg = sieg_df["Total Events For"].median() if not sieg_df.empty else None
    median_for_nicht_sieg = nicht_sieg_df["Total Events For"].median() if not nicht_sieg_df.empty else None

    median_against_sieg = sieg_df["Total Events Against"].median() if not sieg_df.empty else None
    median_against_nicht_sieg = nicht_sieg_df["Total Events Against"].median() if not nicht_sieg_df.empty else None

    st.markdown("---")
    st.subheader("📊 Zusammenfassung: Events For & Against")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏆 Total Events For (Median)", round(median_for_sieg, 2) if median_for_sieg is not None else "Keine Daten")
        st.metric("📉 Total Events For bei Nicht-Siegen (Median)", round(median_for_nicht_sieg, 2) if median_for_nicht_sieg is not None else "Keine Daten")
    with col2:
        st.metric("🔴 Total Events Against (Median)", round(median_against_sieg, 2) if median_against_sieg is not None else "Keine Daten")
        st.metric("📉 Total Events Against bei Nicht-Siegen (Median)", round(median_against_nicht_sieg, 2) if median_against_nicht_sieg is not None else "Keine Daten")

    if median_for_nicht_sieg is not None and median_for_sieg is not None:
        if median_for_sieg > median_for_nicht_sieg:
            st.success("Mehr Events For korrelieren mit einer höheren Siegchance.")
        elif median_for_sieg < median_for_nicht_sieg:
            st.warning("Weniger Events For scheinen mit mehr Siegen verbunden zu sein.")
        else:
            st.info("Events For zeigen keinen klaren Unterschied bei Sieg/Nicht-Sieg.")

    if median_against_nicht_sieg is not None and median_against_sieg is not None:
        if median_against_sieg < median_against_nicht_sieg:
            st.success("Weniger Events Against korrelieren mit einer höheren Siegchance.")
        elif median_against_sieg > median_against_nicht_sieg:
            st.warning("Mehr Events Against scheinen mit mehr Niederlagen verbunden zu sein.")
        else:
            st.info("Events Against zeigen keinen klaren Unterschied bei Sieg/Nicht-Sieg.")

def render_trend_page(all_df):
    st.header("📈 Trend-Analyse")

    ligas = [
        "SSL",
        "Fliiga",
        "L-UPL",
        "Superliga",
        "International Men",
        "International Women"
    ]
    selected_ligas = st.multiselect("Ligen auswählen:", ligas, default=["L-UPL"])

    filtered_df = filter_data_for_trends(all_df, selected_ligas)

    st.write(f"Gefilterte Daten: {len(filtered_df)} Zeilen")

    if filtered_df.empty:
        st.warning("Keine Daten für die gewählten Ligen verfügbar.")
        return

    filtered_df = add_event_columns(filtered_df)

    def safe_startswith(value, prefix):
        if isinstance(value, str):
            return value.startswith(prefix)
        return False

    filtered_df["Ergebnis"] = filtered_df.apply(
        lambda row: "Sieg" if safe_startswith(row["Action"], f"Tor {row.get('team_for', 'Tigers')}") else (
            "Niederlage" if safe_startswith(row["Action"], f"Tor {row.get('team_against', 'Gegner')}") else "Unentschieden"
        ),
        axis=1
    )

    event_cols = [
        "ZOE For",
        "ZOE Against",
        "Low Q Chance For",
        "Low Q Chance Against",
        "Mid Q Chance For",
        "Mid Q Chance Against",
        "High Q Chance For",
        "High Q Chance Against",
        "Tor For",
        "Tor Against"
    ]

    df_summary = filtered_df.groupby(["game", "Ergebnis"], dropna=False)[event_cols].sum().reset_index()

    render_event_summary_chart(filtered_df)
    render_event_summary_box(df_summary)

    st.info("Diese Seite befindet sich noch im Aufbau.")
