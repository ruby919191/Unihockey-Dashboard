import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

# --- Event-Zählung ---
def extract_event_count(action_str, event_name):
    if not isinstance(action_str, str):
        return 0
    pattern = rf"{re.escape(event_name)}(: \\d+)?"
    if re.search(pattern, action_str):
        return 1
    return 0

def extract_goal_count(action_str, team_name):
    if not isinstance(action_str, str):
        return 0
    pattern = rf"Tor {re.escape(team_name)}: (\\d+)"
    match = re.search(pattern, action_str)
    if match:
        return int(match.group(1))
    elif f"Tor {team_name}" in action_str:
        return 1
    return 0

def add_goal_and_event_columns(df):
    df = df.copy()

    def count_goals(row):
        if row.get("season") == "Divers":
            team_for = row.get("team_for", "Tigers")
            team_against = row.get("team_against", "Gegner")
        else:
            team_for = "Tigers"
            team_against = "Gegner"
        return pd.Series({
            "Tor Tigers": extract_goal_count(row["Action"], team_for),
            "Tor Gegner": extract_goal_count(row["Action"], team_against)
        })

    df[["Tor Tigers", "Tor Gegner"]] = df.apply(count_goals, axis=1)

    event_names = [
        "Low Q Chance For", "Mid Q Chance For", "High Q Chance For", "Pot + Chance For", "ZOE For",
        "Low Q Chance Against", "Mid Q Chance Against", "High Q Chance Against", "Pot + Chance Against", "ZOE Gegner"
    ]
    for ev in event_names:
        df[ev] = df["Action"].apply(lambda x: extract_event_count(x, ev))

    return df

# --- Analysefunktionen ---
def render_aggregated_event_summary(df):
    df = df.copy()
    df = add_goal_and_event_columns(df)

    df["Low Q Chance"] = df[["Low Q Chance For", "Low Q Chance Against"]].sum(axis=1)
    df["Mid Q Chance"] = df[["Mid Q Chance For", "Mid Q Chance Against"]].sum(axis=1)
    df["High Q Chance"] = df[["High Q Chance For", "High Q Chance Against"]].sum(axis=1)
    df["Pot + Chance"] = df[["Pot + Chance For", "Pot + Chance Against"]].sum(axis=1)
    df["ZOE"] = df[["ZOE For", "ZOE Gegner"]].sum(axis=1)
    df["Total Events"] = df[["Low Q Chance", "Mid Q Chance", "High Q Chance", "Pot + Chance", "ZOE"]].sum(axis=1)

    total_sums = df[["Low Q Chance", "Mid Q Chance", "High Q Chance", "Pot + Chance", "ZOE"]].sum()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=total_sums.index,
        y=total_sums.values,
        text=total_sums.values,
        textposition='auto'
    ))
    fig.update_layout(title="Gesamtsumme Events über alle Spiele", yaxis_title="Anzahl", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

def render_total_event_bar(df):
    df = df.copy()
    df = add_goal_and_event_columns(df)

    df["Low Q Chance"] = df[["Low Q Chance For", "Low Q Chance Against"]].sum(axis=1)
    df["Mid Q Chance"] = df[["Mid Q Chance For", "Mid Q Chance Against"]].sum(axis=1)
    df["High Q Chance"] = df[["High Q Chance For", "High Q Chance Against"]].sum(axis=1)
    df["Pot + Chance"] = df[["Pot + Chance For", "Pot + Chance Against"]].sum(axis=1)
    df["ZOE"] = df[["ZOE For", "ZOE Gegner"]].sum(axis=1)
    df["Total Events"] = df[["Low Q Chance", "Mid Q Chance", "High Q Chance", "Pot + Chance", "ZOE"]].sum(axis=1)

    total_events = df["Total Events"].sum()
    st.metric("📊 Total Events insgesamt", int(total_events))

def render_median_events_per_game(df):
    df = df.copy()
    df = add_goal_and_event_columns(df)

    df["Low Q Chance"] = df[["Low Q Chance For", "Low Q Chance Against"]].sum(axis=1)
    df["Mid Q Chance"] = df[["Mid Q Chance For", "Mid Q Chance Against"]].sum(axis=1)
    df["High Q Chance"] = df[["High Q Chance For", "High Q Chance Against"]].sum(axis=1)
    df["Pot + Chance"] = df[["Pot + Chance For", "Pot + Chance Against"]].sum(axis=1)
    df["ZOE"] = df[["ZOE For", "ZOE Gegner"]].sum(axis=1)
    df["Total Events"] = df[["Low Q Chance", "Mid Q Chance", "High Q Chance", "Pot + Chance", "ZOE"]].sum(axis=1)

    # Gruppierung auf Spielniveau
    grouped = df.groupby("game")["Total Events"].sum().reset_index()

    median_events = grouped["Total Events"].median()
    st.metric("📈 Median Events pro Spiel", f"{median_events:.0f}")


def render_event_win_correlation(df):
    df = df.copy()
    df = add_goal_and_event_columns(df)

    df["Low Q Chance"] = df[["Low Q Chance For", "Low Q Chance Against"]].sum(axis=1)
    df["Mid Q Chance"] = df[["Mid Q Chance For", "Mid Q Chance Against"]].sum(axis=1)
    df["High Q Chance"] = df[["High Q Chance For", "High Q Chance Against"]].sum(axis=1)
    df["Pot + Chance"] = df[["Pot + Chance For", "Pot + Chance Against"]].sum(axis=1)
    df["ZOE"] = df[["ZOE For", "ZOE Gegner"]].sum(axis=1)
    df["Total Events"] = df[["Low Q Chance", "Mid Q Chance", "High Q Chance", "Pot + Chance", "ZOE"]].sum(axis=1)

    grouped = df.groupby("game").agg({
        "Total Events": "sum",
        "Tor Tigers": "sum",
        "Tor Gegner": "sum"
    }).reset_index()

    grouped["Outcome"] = grouped.apply(
        lambda row: "Sieg" if row["Tor Tigers"] > row["Tor Gegner"] else ("Unentschieden" if row["Tor Tigers"] == row["Tor Gegner"] else "Niederlage"),
        axis=1
    )

    bins = [0, 40, 60, 80, 100, 150, 9999]
    labels = ["<40", "40–60", "60–80", "80–100", "100–150", "150+"]
    grouped["Event-Gruppe"] = pd.cut(grouped["Total Events"], bins=bins, labels=labels, right=False)

    siegquoten = grouped.groupby("Event-Gruppe")["Outcome"].value_counts(normalize=True).unstack().fillna(0)
    siegquoten["Sieg %"] = siegquoten.get("Sieg", 0) * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=siegquoten.index.astype(str),
        y=siegquoten["Sieg %"],
        text=siegquoten["Sieg %"].round(1).astype(str) + "%",
        textposition="auto",
        marker_color="seagreen"
    ))
    fig.update_layout(
        title="Siegquote nach Total Events (gruppiert)",
        xaxis_title="Eventanzahl (Gruppen)",
        yaxis_title="Siegquote (%)",
        yaxis=dict(range=[0, 100]),
        template="plotly_white",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)