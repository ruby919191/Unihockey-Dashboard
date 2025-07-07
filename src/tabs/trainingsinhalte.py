import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Feste Kategorien für Dropdowns und Pie-Charts
INHALTE_LISTE = [
    "Technik", "Taktik", "Powerplay", "Boxplay", "Conditioned Game",
    "Small-Games", "5v5", "Skills"
]

SPIELSITUATION_LISTE = [
    "Zone-Entry", "Zone-Entry gg. Pressing", "Festsetzen", "Kontersituation +", "Zone-Exits",
    "Nachsetzen", "Kontersituation -", "Pressing", "Zone-Defense", "Forechecking",
    "Unkontrollierte Spielsituation"
]

# Initialisiere DataFrame im Session State
if "trainings" not in st.session_state:
    st.session_state.trainings = pd.DataFrame(columns=[
        "Datum", "Inhalte", "Spielsituation", "Erkenntnisse", "Offene Übungen", "Maßnahmen"
    ])

def count_and_fill(categories, series):
    counts = series.value_counts()
    return pd.Series({cat: counts.get(cat, 0) for cat in categories})

def plot_pie_chart(data, title):
    fig, ax = plt.subplots(figsize=(6, 6))

    def autopct_filter(pct):
        return ('%1.1f%%' % pct) if pct > 3 else ''

    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=None,
        autopct=autopct_filter,
        startangle=90,
        textprops=dict(color="black")
    )

    ax.set_title(title)
    ax.axis('equal')

    # Legende außerhalb rechts
    ax.legend(data.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    st.pyplot(fig)

def render_filter_panel(df):
    st.sidebar.header("Filter")

    if df.empty:
        return df  # Keine Filterung nötig bei leerem DF

    start_date, end_date = st.sidebar.date_input(
        "Zeitraum wählen",
        value=[df["Datum"].min(), df["Datum"].max()]
    )

    selected_inhalte = st.sidebar.multiselect("Inhalte filtern", options=INHALTE_LISTE, default=INHALTE_LISTE)
    selected_spielsituationen = st.sidebar.multiselect("Spielsituationen filtern", options=SPIELSITUATION_LISTE, default=SPIELSITUATION_LISTE)

    # Filter anwenden
    filtered_df = df[
        (df["Datum"] >= pd.to_datetime(start_date)) &
        (df["Datum"] <= pd.to_datetime(end_date))
    ]

    # Inhalte filtern (Kommagetrennt)
    mask_inhalte = filtered_df["Inhalte"].apply(
        lambda x: any(item in x.split(", ") for item in selected_inhalte)
    )
    filtered_df = filtered_df[mask_inhalte]

    # Spielsituation filtern (Kommagetrennt)
    mask_spielsituation = filtered_df["Spielsituation"].apply(
        lambda x: any(item in x.split(", ") for item in selected_spielsituationen)
    )
    filtered_df = filtered_df[mask_spielsituation]

    return filtered_df

def render_trainingsinhalte_tab():
    st.header("📋 Trainingsinhalte erfassen")

    datum = st.date_input("Datum des Trainings", value=date.today())

    inhalte = st.multiselect(
        "Inhalte des Trainings",
        INHALTE_LISTE
    )

    spielsituation = st.multiselect(
        "Spielsituation",
        SPIELSITUATION_LISTE
    )

    erkenntnisse = st.text_area("Erkenntnisse aus dem Training")

    offene_uebungen_input = st.text_input("Offene Übungen (Komma-getrennt)")
    offene_uebungen = [tag.strip() for tag in offene_uebungen_input.split(",") if tag.strip()]

    massnahmen = st.text_area("Maßnahmen für das nächste Training")

    if st.button("Eintrag speichern"):
        neuer_eintrag = {
            "Datum": datum,
            "Inhalte": ", ".join(inhalte),
            "Spielsituation": ", ".join(spielsituation),
            "Erkenntnisse": erkenntnisse,
            "Offene Übungen": ", ".join(offene_uebungen),
            "Maßnahmen": massnahmen
        }
        st.session_state.trainings = pd.concat(
            [st.session_state.trainings, pd.DataFrame([neuer_eintrag])],
            ignore_index=True
        )
        st.success("Eintrag gespeichert!")

    # Filterung anwenden
    filtered_df = render_filter_panel(st.session_state.trainings)

    st.subheader("Gefilterte Trainingsinhalte")
    st.dataframe(filtered_df)

    if not filtered_df.empty:
        # Löschfunktion für gefilterte Tabelle
        index_to_delete = st.selectbox(
            "Eintrag zum Löschen auswählen (Index)",
            options=filtered_df.index.tolist()
        )
        if st.button("Ausgewählten Eintrag löschen"):
            # Löschen aus dem globalen DataFrame
            st.session_state.trainings = st.session_state.trainings.drop(index=index_to_delete).reset_index(drop=True)
            st.success(f"Eintrag {index_to_delete} wurde gelöscht!")
            st.experimental_rerun()

        # Diagramme mit gefilterten Daten
        inhalte_series = filtered_df["Inhalte"].str.split(", ").explode()
        inhalte_counts = count_and_fill(INHALTE_LISTE, inhalte_series)

        spielsituation_series = filtered_df["Spielsituation"].str.split(", ").explode()
        spielsituation_counts = count_and_fill(SPIELSITUATION_LISTE, spielsituation_series)

        st.subheader("Verteilung Inhalte des Trainings")
        plot_pie_chart(inhalte_counts, "Inhalte des Trainings")

        st.subheader("Verteilung Spielsituationen")
        plot_pie_chart(spielsituation_counts, "Spielsituationen")
