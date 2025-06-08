import pandas as pd
import re

def get_goals_by_team(df, team_for_name, team_against_name):
    pattern_team1 = re.compile(rf"Tor {re.escape(team_for_name)}:\s*\d+", re.IGNORECASE)
    pattern_team2 = re.compile(rf"Tor {re.escape(team_against_name)}:\s*\d+", re.IGNORECASE)

    goals_team1 = df[df["Action"].apply(lambda x: bool(pattern_team1.search(str(x))))].shape[0]
    goals_team2 = df[df["Action"].apply(lambda x: bool(pattern_team2.search(str(x))))].shape[0]
    return goals_team1, goals_team2

def get_goals_per_period(df, team_for_name, team_against_name):
    pattern_team1 = re.compile(rf"Tor {re.escape(team_for_name)}:\s*\d+", re.IGNORECASE)
    pattern_team2 = re.compile(rf"Tor {re.escape(team_against_name)}:\s*\d+", re.IGNORECASE)

    periods = sorted(df["Drittel"].dropna().unique())
    results = []

    for period in periods:
        df_period = df[df["Drittel"] == period]
        goals_team1 = df_period["Action"].apply(lambda x: bool(pattern_team1.search(str(x)))).sum()
        goals_team2 = df_period["Action"].apply(lambda x: bool(pattern_team2.search(str(x)))).sum()
        results.append(f"{goals_team1}:{goals_team2}")

    return " / ".join(results)

def get_chances_and_xg(df):
    chances_team1 = df[df["Action"].str.contains("Chance For", na=False)].shape[0]
    chances_team2 = df[df["Action"].str.contains("Chance Against", na=False)].shape[0]

    xg_for = pd.to_numeric(df[df["Action"].str.contains("Chance For", na=False)]["XG"], errors='coerce')
    xg_against = pd.to_numeric(df[df["Action"].str.contains("Chance Against", na=False)]["XG"], errors='coerce')

    xg_team1 = xg_for.sum()
    xg_team2 = xg_against.sum()

    return chances_team1, chances_team2, round(xg_team1, 2), round(xg_team2, 2)

def get_corsi_fenwick_percentage(df):
    corsi_for = df["Action"].str.contains("Chance For", na=False).sum()
    corsi_against = df["Action"].str.contains("Chance Against", na=False).sum()
    
    fenwick_for = df[
        df["Action"].str.contains("Chance For", na=False) &
        (df["Schussmetrik"] != "Geblockt")
    ].shape[0]
    
    fenwick_against = df[
        df["Action"].str.contains("Chance Against", na=False) &
        (df["Schussmetrik"] != "Geblockt")
    ].shape[0]
    
    total_corsi = corsi_for + corsi_against
    total_fenwick = fenwick_for + fenwick_against
    
    corsi_pct = round((corsi_for / total_corsi) * 100, 1) if total_corsi else None
    fenwick_pct = round((fenwick_for / total_fenwick) * 100, 1) if total_fenwick else None

    return corsi_pct, fenwick_pct
