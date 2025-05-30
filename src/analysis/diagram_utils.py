import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_chances_by_game(df, metric="Anzahl", for_or_against="For"):
    """
    Zeigt Chancen pro Spiel über Zeit (For oder Against).
    """
    filtered = df[df["Action"].str.contains(f"Chance {for_or_against}", na=False)]
    if filtered.empty:
        return None

    grouped = filtered.groupby("game").agg(
        Anzahl=("Action", "count"),
        xG=("XG", "sum")
    ).reset_index()

    fig = px.bar(
        grouped,
        x="game",
        y=metric,
        title=f"Chancen {for_or_against} pro Spiel ({metric})",
        labels={metric: metric, "game": "Spiel"},
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def plot_save_percentage_trend(df):
    """
    Plottet den Verlauf der Save % über die Spiele.
    Erwartet Spalten: 'game', 'Shots Against', 'Goals Against'
    """
    if "game" not in df.columns or "Shots Against" not in df.columns or "Goals Against" not in df.columns:
        return go.Figure()

    df = df.copy()
    df["Save %"] = df.apply(
        lambda row: round((1 - (row["Goals Against"] / row["Shots Against"])) * 100, 1)
        if row["Shots Against"] > 0 else None,
        axis=1
    )
    df = df.dropna(subset=["Save %"])

    return px.line(df, x="game", y="Save %", title="Save Percentage Verlauf", markers=True)


def plot_xg_difference(df):
    """
    Visualisiert die xG Differenz zwischen Chancen For und Against über die Spiele.
    Erwartet Spalten: 'game', 'xG For', 'xG Against'
    """
    if "game" not in df.columns or "xG For" not in df.columns or "xG Against" not in df.columns:
        return go.Figure()

    df = df.copy()
    df["xG Diff"] = df["xG For"] - df["xG Against"]

    return px.bar(df, x="game", y="xG Diff", title="xG Differenz pro Spiel", color="xG Diff",
                  color_continuous_scale="RdYlGn", range_color=[-2, 2])