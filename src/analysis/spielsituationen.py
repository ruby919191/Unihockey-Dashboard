import pandas as pd
import re

# Liste der neuen Aktionen direkt hier definiert
NEUE_AKTIONEN = [
    "Zone-Exits For", "Zone-Exits Against",
    "Nachsetzen For", "Nachsetzen Against",
    "Pressing For", "Pressing Against",
    "ZOE For gg. Pressing", "ZOE Against gg. Pressing"
]

def calculate_spielsituationen(df: pd.DataFrame) -> pd.DataFrame:
    # Vorbereitung
    df = df.copy()
    df = df[df["Action"].notna()]

    # Ergebnis-Speicher
    result = []

    for aktion in NEUE_AKTIONEN:
        pattern = rf"{re.escape(aktion)}:"
        is_for = "For" in aktion
        bewertungsspalte = "ZOE_For" if is_for else "ZOE_Against"

        # Filtern der betreffenden Zeilen
        mask = df["Action"].str.contains(pattern, na=False)
        relevant_rows = df[mask]

        # Zählung
        good = (relevant_rows[bewertungsspalte] == "Good").sum()
        bad = (relevant_rows[bewertungsspalte] == "Bad").sum()

        # Differenzberechnung
        diff = good - bad

        # Aktionstyp extrahieren
        aktionstyp = aktion.split(" For")[0].split(" Against")[0]

        # Eintrag erstellen
        eintrag = {
            "Aktion": aktion,
            "Aktionstyp": aktionstyp,
            "For Good": good if is_for else 0,
            "For Bad": bad if is_for else 0,
            "Against Good": good if not is_for else 0,
            "Against Bad": bad if not is_for else 0,
            "Diff For": diff if is_for else 0,
            "Diff Against": diff if not is_for else 0,
        }
        result.append(eintrag)

    # In DataFrame umwandeln
    result_df = pd.DataFrame(result)
    return result_df