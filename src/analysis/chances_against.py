import pandas as pd

def get_chances_against(df):
    return df[df["Action"].str.contains("Chance Against", na=False)].reset_index(drop=True)

def count_chances_by_quality(df):
    qualities = ["Low Q", "Mid Q", "High Q", "Pot +"]
    rows = []

    for q in qualities:
        subset = df[df["Action"].str.contains(f"{q} Chance Against", na=False)]
        count = len(subset)
        xg = subset["XG"].sum()

        on = (subset["Schussmetrik"] == "Auf Tor").sum()
        off = (subset["Schussmetrik"] == "Neben Tor").sum()
        blocked = (subset["Schussmetrik"] == "Geblockt").sum()

        pct = lambda x: round(x / count * 100, 1) if count else 0
        rows.append([q, count, round(xg, 2), on, pct(on), off, pct(off), blocked, pct(blocked)])

    df_summary = pd.DataFrame(rows, columns=[
        "Qualität", "Anzahl", "xG", "Auf Tor", "% Auf Tor", 
        "Neben Tor", "% Neben Tor", "Geblockt", "% Geblockt"
    ])

    total = pd.DataFrame([[
        "Total", df_summary["Anzahl"].sum(), df_summary["xG"].sum(),
        df_summary["Auf Tor"].sum(), "", df_summary["Neben Tor"].sum(), "",
        df_summary["Geblockt"].sum(), ""
    ]], columns=df_summary.columns)

    return pd.concat([df_summary, total], ignore_index=True)

def count_chances_by_line(df):
    df = get_chances_against(df).dropna(subset=["Linien For"])
    lines = []

    for line, group in df.groupby("Linien For"):
        data = {
            "Linie": line,
            "Low Q": group["Action"].str.contains("Low Q", na=False).sum(),
            "Mid Q": group["Action"].str.contains("Mid Q", na=False).sum(),
            "High Q": group["Action"].str.contains("High Q", na=False).sum(),
            "Pot +": group["Action"].str.contains("Pot +", na=False).sum()
        }
        data["Total"] = sum(data[q] for q in ["Low Q", "Mid Q", "High Q", "Pot +"])
        data["xG"] = round(group["XG"].sum(), 2)
        data["% Auf Tor"] = round(
            (group["Schussmetrik"] == "Auf Tor").sum() / data["Total"] * 100, 1
        ) if data["Total"] else 0
        lines.append(data)

    return pd.DataFrame(lines).sort_values("Total", ascending=False)

def count_chances_by_period(df):
    df = get_chances_against(df).dropna(subset=["Drittel"])
    df["Drittel"] = df["Drittel"].str.upper()

    grouped = df.groupby("Drittel").agg(Anzahl=("Action", "count"), xG=("XG", "sum")).reset_index()
    grouped["xG"] = grouped["xG"].round(2)

    total = pd.DataFrame([{
        "Drittel": "Total",
        "Anzahl": grouped["Anzahl"].sum(),
        "xG": round(grouped["xG"].sum(), 2)
    }])

    return pd.concat([grouped, total], ignore_index=True)

def count_chances_by_tactical_situation(df):
    df = get_chances_against(df).dropna(subset=["Taktische Spielsituation"])
    result = df.groupby("Taktische Spielsituation").size().reset_index(name="Anzahl Chancen")
    return result.sort_values("Anzahl Chancen", ascending=False).reset_index(drop=True)
