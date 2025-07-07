import pandas as pd

print("🧠 calculate_spielsituationen() wurde neu geladen")

AKTIONEN = [
    "Zone-Exits For",
    "Zone-Exits Against",
    "Nachsetzen For",
    "Nachsetzen Against",
    "Pressing For",
    "Pressing Against",
    "ZOE For gg. Pressing",
    "ZOE Against gg. Pressing"
]

def calculate_spielsituationen(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[df["Action"].notna()]

    result = []

    for aktion in AKTIONEN:
        count = df["Action"].str.startswith(aktion).sum()
        aktionstyp = aktion.split(" For")[0].split(" Against")[0].strip()

        is_for = "For" in aktion
        is_against = "Against" in aktion

        result.append({
            "Aktion": aktion,
            "Aktionstyp": aktionstyp,
            "For Good": count if is_for else 0,
            "For Bad": 0,
            "Against Good": count if is_against else 0,
            "Against Bad": 0,
            "Diff For": count if is_for else 0,
            "Diff Against": count if is_against else 0,
        })

    return pd.DataFrame(result)
