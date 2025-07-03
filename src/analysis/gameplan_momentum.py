import pandas as pd
import matplotlib.pyplot as plt
import re

def calculate_momentum_by_game(df):
    """
    Berechnet das Chancen-Momentum pro Spiel basierend auf:
    Chancen For vs. Chancen Against.
    Gibt DataFrame mit Spiel, Chancen For, Chancen Against, Momentum und Momentum-% zurück.
    """
    df = df.copy()
    df = df[df["Action"].notna()]

    df["is_chance_for"] = df["Action"].str.contains("Chance For", na=False)
    df["is_chance_against"] = df["Action"].str.contains("Chance Against", na=False)

    grouped = df.groupby("Spiel").agg({
        "is_chance_for": "sum",
        "is_chance_against": "sum"
    }).reset_index()

    grouped = grouped.rename(columns={
        "is_chance_for": "Chancen For",
        "is_chance_against": "Chancen Against"
    })

    grouped["Momentum"] = grouped["Chancen For"] - grouped["Chancen Against"]
    grouped["Momentum %"] = grouped.apply(
        lambda row: round((row["Chancen For"] / (row["Chancen For"] + row["Chancen Against"])) * 100, 1)
        if (row["Chancen For"] + row["Chancen Against"]) > 0 else 0.0,
        axis=1
    )

    return grouped.sort_values(by="Spiel").reset_index(drop=True)


def plot_momentum_chart(df, spiel_name):
    """
    Kompaktes Momentum-Diagramm pro Drittel ohne Textinterpretation.
    """
    df = df[df["Spiel"] == spiel_name].copy().reset_index(drop=True)

    # Regex für Chancen
    chance_pattern_for = r"^(Low Q Chance|Mid Q Chance|High Q Chance|Pot \+ Chance) For"
    chance_pattern_against = r"^(Low Q Chance|Mid Q Chance|High Q Chance|Pot \+ Chance) Against"

    df["momentum"] = df["Action"].apply(
        lambda x: 1 if re.match(chance_pattern_for, str(x)) else
                  -1 if re.match(chance_pattern_against, str(x)) else 0
    )

    df["Drittel"] = df["Drittel"].astype(str)

    # Kompakter Plot
    fig, ax = plt.subplots(figsize=(4.5, 1.8))
    for drittel, group in df.groupby("Drittel"):
        group = group.reset_index(drop=True)
        group["momentum_cumsum"] = group["momentum"].cumsum()
        ax.plot(group.index, group["momentum_cumsum"], label=f'Drittel {drittel}', linewidth=1.2)

    ax.axhline(0, color='black', linewidth=0.7)
    ax.set_title(f"Momentum – {spiel_name}", fontsize=8)
    ax.set_xlabel("Chancen", fontsize=7)
    ax.set_ylabel("Momentum", fontsize=7)
    ax.tick_params(labelsize=6)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.legend(fontsize=6, loc="upper right")

    plt.tight_layout()
    return fig
