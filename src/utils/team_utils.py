# src/utils/team_utils.py

def determine_team_names(df, selected_season):
    if selected_season == "Divers" and "team_for" in df.columns and "team_against" in df.columns:
        team_for_name = df["team_for"].iloc[0]
        team_against_name = df["team_against"].iloc[0]
    else:
        team_for_name = "Tigers"
        team_against_name = "Gegner"
    return team_for_name, team_against_name
