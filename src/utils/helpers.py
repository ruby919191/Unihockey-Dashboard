# src/utils/helpers.py

import re

def extract_opponent_from_filename(game_id: str) -> str:
    """
    Extrahiert den Gegner aus der Game-ID.
    Beispiel: 2024-11-02_vs_SVWE → SVWE
    """
    if "_vs_" in game_id:
        return game_id.split("_vs_")[1]
    return "Unbekannt"


def extract_team_from_filename(game_id: str) -> str:
    """
    Extrahiert das eigene Team aus der Game-ID, wenn es nach dem Muster geschrieben ist.
    Beispiel: 2024-11-02_Tigers_vs_SVWE → Tigers
    (optional, nur wenn du das in Zukunft brauchst)
    """
    parts = game_id.split("_vs_")
    if len(parts) == 2 and "_" in parts[0]:
        return parts[0].split("_")[-1]
    return "Tigers"


def get_opponent_display_name(selected_season: str, selected_game: str, fallback: str = "Gegner") -> str:
    """
    Gibt den Namen des Gegners zurück – nur wenn NICHT Season 'Divers'.
    """
    if selected_season != "Divers" and selected_game:
        return extract_opponent_from_filename(selected_game)
    return fallback
