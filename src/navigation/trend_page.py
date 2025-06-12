import streamlit as st
from src.utils.filter_leagues import filter_data_for_trends  
import pandas as pd
import plotly.graph_objects as go

def aggregate_events(df):
    df = df.copy()
    df["Action"] = df["Action"].fillna("")

    event_patterns = {
        "ZOE For": "ZOE For",
        "ZOE Against": "ZOE Gegner",
        "Low Q Chance For": "Low Q Chance For",
        "Mid Q Chance For": "Mid Q Chance For",
        "High Q Chance For": "High Q Chance For",
        "Tor Tigers": "Tor Tigers",
        "Tor Gegner": "Tor Gegner",
    }

    event_sums = {}
    for key, pattern in event_patterns.items():
        mask = df["Action"].str.contains(pattern, na=False)
        event_sums[key] = mask.sum()

    return event_sums

def plot_event_sums(event_sums):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(event_sums.keys()),
        y=list(event_sums.values()),
        text=list(event_sums.values()),
        textposition='auto'
    ))

    fig.update_layout(
        title="Summe der Events",
        xaxis_title="Event-Kategorie",
        yaxis_title="Anzahl",
        yaxis=dict(tickformat="d"),
        template="plotly_white"
    )

    return fig

def render_event_summary_chart(df):
    event_sums = aggregate_events(df)
    fig = plot_event_sums(event_sums)
    st.plotly_chart(fig, use_container_width=True)

def render_trend_page(all_df):
    filtered_df = filter_data_for_trends(all_df)

    st.header("📈 Trend-Analyse")

    # Hier wird die Chart tatsächlich angezeigt
    render_event_summary_chart(filtered_df)

    st.info("Diese Seite befindet sich noch im Aufbau. Hier wird bald eine Trendanalyse mit xG, Tore und weiteren Metriken im Zeitverlauf erscheinen.")
