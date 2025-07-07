import pandas as pd

def get_chances_for(df):
    return df[df["Action"].str.contains("Chance For", na=False)].reset_index(drop=True)

def count_chances_by_quality(df):
    qualities = ["Low Q", "Mid Q", "High Q", "Pot +"]
    rows = []

    for q in qualities:
        subset = df[df["Action"].str.contains(f"{q} Chance For", na=False)]

        count = len(subset)
        xg_series = pd.to_numeric(subset.get("XG", pd.Series(dtype=float)), errors="coerce")
        xg = xg_series.sum(skipna=True)

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
        "Total", df_summary["Anzahl"].sum(), round(df_summary["xG"].sum(), 2),
        df_summary["Auf Tor"].sum(), "", df_summary["Neben Tor"].sum(), "",
        df_summary["Geblockt"].sum(), ""
    ]], columns=df_summary.columns)

    return pd.concat([df_summary, total], ignore_index=True)

def count_chances_by_line(df):
    df = get_chances_for(df).dropna(subset=["Linien For"])
    lines = []

    for line, group in df.groupby("Linien For"):
        xg_series = pd.to_numeric(group.get("XG", pd.Series(dtype=float)), errors="coerce")

        data = {
            "Linie": line,
            "Low Q": group["Action"].str.contains("Low Q", na=False).sum(),
            "Mid Q": group["Action"].str.contains("Mid Q", na=False).sum(),
            "High Q": group["Action"].str.contains("High Q", na=False).sum(),
            "Pot +": group["Action"].str.contains("Pot +", na=False).sum()
        }
        data["Total"] = sum(data[q] for q in ["Low Q", "Mid Q", "High Q", "Pot +"])
        data["xG"] = round(xg_series.sum(skipna=True), 2)
        data["% Auf Tor"] = round(
            (group["Schussmetrik"] == "Auf Tor").sum() / data["Total"] * 100, 1
        ) if data["Total"] else 0
        lines.append(data)

    df_result = pd.DataFrame(lines)

    if df_result.empty or "Total" not in df_result.columns:
        return pd.DataFrame(columns=["Linie", "Low Q", "Mid Q", "High Q", "Pot +", "Total", "xG", "% Auf Tor"])

    return df_result.sort_values("Total", ascending=False)

def count_chances_by_period(df):
    df = get_chances_for(df).dropna(subset=["Drittel"])
    df["Drittel"] = df["Drittel"].str.upper()

    df["XG"] = pd.to_numeric(df.get("XG", pd.Series(dtype=float)), errors="coerce")
    grouped = df.groupby("Drittel").agg(Anzahl=("Action", "count"), xG=("XG", "sum")).reset_index()
    grouped["xG"] = grouped["xG"].round(2)

    total = pd.DataFrame([{
        "Drittel": "Total",
        "Anzahl": grouped["Anzahl"].sum(),
        "xG": round(grouped["xG"].sum(), 2)
    }])

    return pd.concat([grouped, total], ignore_index=True)

def count_chances_by_tactical_situation(df):
    df = get_chances_for(df).dropna(subset=["Taktische Spielsituation"])
    return (
        df.groupby("Taktische Spielsituation")
        .size()
        .reset_index(name="Anzahl Chancen")
        .sort_values("Anzahl Chancen", ascending=False)
        .reset_index(drop=True)
    )

def count_chances_by_tactical_situation_detailed(df):
    df = get_chances_for(df)

    if "Nummerische Spielsituation" in df.columns:
        df = df[df["Nummerische Spielsituation"] == "5:5"]

    df = df.dropna(subset=["Taktische Spielsituation"])
    categories = ["Low Q", "Mid Q", "High Q", "Pot +"]
    result = {}

    for _, row in df.iterrows():
        situation = row["Taktische Spielsituation"]
        action = row["Action"]

        if situation not in result:
            result[situation] = {cat: 0 for cat in categories}

        for cat in categories:
            if f"{cat} Chance For" in action:
                result[situation][cat] += 1

    df_result = pd.DataFrame.from_dict(result, orient="index").fillna(0).astype(int)
    df_result["Total"] = df_result.sum(axis=1)
    total_sum = df_result["Total"].sum()
    df_result["% vom Total"] = df_result["Total"].apply(
        lambda x: round(x / total_sum * 100, 1) if total_sum else 0.0
    )

    df_result = df_result.sort_values("Total", ascending=False).reset_index().rename(
        columns={"index": "Taktische Spielsituation"}
    )

    return df_result

def count_pp_shots_for(df):
    df = df[df["Action"].notna()]
    subset = df[df["Action"].str.contains("PP Shot For", na=False)]

    count = len(subset)
    xg_series = pd.to_numeric(subset.get("XG", pd.Series(dtype=float)), errors="coerce")
    xg = xg_series.sum(skipna=True)

    on = (subset["Schussmetrik"] == "Auf Tor").sum()
    off = (subset["Schussmetrik"] == "Neben Tor").sum()
    blocked = (subset["Schussmetrik"] == "Geblockt").sum()

    pct = lambda x: round(x / count * 100, 1) if count else 0

    df_summary = pd.DataFrame([[
        "PP Shot", count, round(xg, 2), on, pct(on), off, pct(off), blocked, pct(blocked)
    ]], columns=[
        "Qualität", "Anzahl", "xG", "Auf Tor", "% Auf Tor",
        "Neben Tor", "% Neben Tor", "Geblockt", "% Geblockt"
    ])

    total = pd.DataFrame([[
        "Total", count, round(xg, 2), on, "", off, "", blocked, ""
    ]], columns=df_summary.columns)

    return pd.concat([df_summary, total], ignore_index=True)
