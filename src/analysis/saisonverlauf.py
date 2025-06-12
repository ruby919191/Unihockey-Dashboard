import pandas as pd

def calculate_saisonverlauf_stats(all_df, ausgewählte_saisons):
    saison_df = all_df[all_df["season"] != "Divers"]
    if ausgewählte_saisons:
        saison_df = saison_df[saison_df["season"].isin(ausgewählte_saisons)]

    spiele = saison_df["game"].unique()
    daten = []

    siege = 0
    niederlagen = 0
    unentschieden = 0

    for spiel in spiele:
        df_spiel = saison_df[saison_df["game"] == spiel]

        tore_tigers = df_spiel[df_spiel["Action"].fillna("").str.startswith("Tor Tigers")].shape[0]
        tore_gegner = df_spiel[df_spiel["Action"].fillna("").str.startswith("Tor Gegner")].shape[0]

        if tore_tigers > tore_gegner:
            resultat = "Sieg"
            siege += 1
        elif tore_tigers < tore_gegner:
            resultat = "Niederlage"
            niederlagen += 1
        else:
            resultat = "Unentschieden"
            unentschieden += 1

        daten.append({
            "Spiel": spiel,
            "Tore Tigers": tore_tigers,
            "Tore Gegner": tore_gegner,
            "Resultat": resultat
        })

    anzahl_spiele = len(spiele)
    siege_prozent = round((siege / anzahl_spiele) * 100, 1) if anzahl_spiele > 0 else 0

    df_ergebnisse = pd.DataFrame(daten)

    return {
        "siege": siege,
        "niederlagen": niederlagen,
        "unentschieden": unentschieden,
        "anzahl_spiele": anzahl_spiele,
        "siege_prozent": siege_prozent,
        "df_ergebnisse": df_ergebnisse
    }
