import streamlit as st
import pandas as pd
from datetime import date
import re

THEMEN = [
    "Game-Plan und Vorbereitung inkl. Trainings",
    "In-Game Coaching generell",
    "Timeout",
    "Entscheid auf 2 Linien",
    "Line-Up",
    "Taktische Umstellung",
    "Spielphase OFF: Festsetzen",
    "Spielphase OFF: Entries",
    "Spielphase OFF: Entries gg. Pressing",
    "Spielphase DEF: Zone-Defense",
    "Spielphase DEF: Forechecking",
    "Spielphase TRN: Nachsetzen",
    "Spielphase TRN: Kontersituation -",
    "Spielphase TRN: Kontersituation +",
    "Spielphase UNKR: Unkontrollierte Spielphase",
    "Specials: Boxplay",
    "Specials Powerplay",
    "Specials 5:6",
    "Specials 6:5",
    "Staffmanagement"
]

if "aar" not in st.session_state:
    st.session_state.aar = pd.DataFrame(columns=[
        "Game-ID", "Datum", "Autor", "Thema", "Bewertung", "Kommentar"
    ])

if "top_learnings" not in st.session_state:
    st.session_state.top_learnings = ""

def validiere_game_id(game_id):
    pattern = r"^\d{4}:\d{2}:\d{2}:.+$"
    return re.match(pattern, game_id) is not None

def validiere_autor(name):
    # Mindestens zwei Wörter für Vor- und Nachname
    return len(name.strip().split()) >= 2

def render_aar_tab():
    st.header("📝 After Action Review erfassen")

    game_id = st.text_input("Game-ID (Format: Jahr:Monat:Tag:Gegner, z.B. 2025:07:07:Zug)")
    if game_id and not validiere_game_id(game_id):
        st.error("Game-ID hat nicht das richtige Format! Bitte Jahr:Monat:Tag:Gegner eingeben.")
        return

    datum = st.date_input("Datum des Reviews", value=date.today())
    autor = st.text_input("Autor / Coach (Vor- und Nachname)")

    kommentar_gesamt = st.text_area("Gesamter Kommentar (optional)", height=80)

    bewertungen = {}
    kommentare = {}

    st.markdown("### Bewertungen und Kommentare zu den Themen")
    for thema in THEMEN:
        st.markdown(f"**{thema}**")
        bewertung = st.selectbox(
            f"Bewertung (1 = schlecht, 5 = sehr gut) für {thema}",
            options=[1, 2, 3, 4, 5],
            index=2,
            key=f"bewertung_{thema}"
        )
        kommentar = st.text_area(
            f"Kommentar zu {thema} (optional)",
            key=f"kommentar_{thema}",
            height=80
        )
        bewertungen[thema] = bewertung
        kommentare[thema] = kommentar

    if st.button("Review speichern"):
        if not game_id:
            st.error("Bitte eine gültige Game-ID eingeben.")
        elif not autor:
            st.error("Bitte den Autor eingeben.")
        elif not validiere_autor(autor):
            st.error("Bitte Vor- und Nachnamen eingeben.")
        else:
            neue_eintraege = []
            for thema in THEMEN:
                kommentar_thema = kommentare[thema].strip()
                if not kommentar_thema:
                    kommentar_thema = kommentar_gesamt.strip()
                neue_eintraege.append({
                    "Game-ID": game_id,
                    "Datum": datum,
                    "Autor": autor,
                    "Thema": thema,
                    "Bewertung": bewertungen[thema],
                    "Kommentar": kommentar_thema
                })
            df_neu = pd.DataFrame(neue_eintraege)
            st.session_state.aar = pd.concat([st.session_state.aar, df_neu], ignore_index=True)
            st.success("Review gespeichert!")

    st.subheader("Gefilterte Reviews")

    if st.session_state.aar.empty:
        st.info("Noch keine Reviews vorhanden.")
        return

    with st.expander("Filter"):
        filter_game_id = st.text_input("Filter: Game-ID (Teilstring)")
        filter_autor = st.text_input("Filter: Autor")
        min_datum, max_datum = st.date_input(
            "Filter: Datum von - bis",
            value=[st.session_state.aar["Datum"].min(), st.session_state.aar["Datum"].max()]
        )

    df_filter = st.session_state.aar.copy()

    if filter_game_id:
        df_filter = df_filter[df_filter["Game-ID"].str.contains(filter_game_id, case=False, na=False)]
    if filter_autor:
        df_filter = df_filter[df_filter["Autor"].str.contains(filter_autor, case=False, na=False)]

    if not pd.api.types.is_datetime64_any_dtype(df_filter["Datum"]):
        df_filter["Datum"] = pd.to_datetime(df_filter["Datum"])

    df_filter = df_filter[
        (df_filter["Datum"] >= pd.to_datetime(min_datum)) &
        (df_filter["Datum"] <= pd.to_datetime(max_datum))
    ]

    st.dataframe(df_filter.reset_index(drop=True))

    if not df_filter.empty:
        index_to_delete = st.selectbox(
            "Eintrag zum Löschen auswählen (Index)",
            options=df_filter.index.tolist()
        )
        if st.button("Ausgewählten Eintrag löschen"):
            st.session_state.aar = st.session_state.aar.drop(index=index_to_delete).reset_index(drop=True)
            st.success(f"Eintrag {index_to_delete} wurde gelöscht!")
            st.experimental_rerun()

    st.subheader("Durchschnittliche Bewertung je Thema")
    avg = df_filter.groupby("Thema")["Bewertung"].mean().sort_values(ascending=False)
    st.bar_chart(avg)

    st.subheader("📌 Top-Learnings")

    neue_learnings = st.text_area(
        "Bitte hier die wichtigsten Learnings eintragen",
        value=st.session_state.top_learnings,
        height=150
    )

    if st.button("Top-Learnings speichern"):
        st.session_state.top_learnings = neue_learnings
        st.success("Top-Learnings wurden gespeichert!")

    if st.session_state.top_learnings:
        st.markdown("**Aktuelle Top-Learnings:**")
        st.markdown(st.session_state.top_learnings)
