import streamlit as st
import pandas as pd
import time
import os
from autogluon.tabular import TabularPredictor

st.set_page_config(page_title="PrognoseTrainer – Modelltraining", layout="wide")
st.title("Trainiere Modelle für Mathematik & Raumvorstellung")

uploaded_csv = st.file_uploader("Lade die vorbereiteten Feature-Daten hoch (CSV aus Teil 1)", type=["csv"])

if uploaded_csv:
    df = pd.read_csv(uploaded_csv)
    st.subheader("Vorschau der Trainingsdaten")
    st.dataframe(df.head(20))

    st.markdown("**Verteilung der Zielwerte**")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df["Mathematik"].dropna())
    with col2:
        st.bar_chart(df["Raumvorstellung"].dropna())

    model_path_math = "models/model_mathematik"
    model_path_raum = "models/model_raumvorstellung"

    df_math = df.dropna(subset=["Mathematik"])
    df_raum = df.dropna(subset=["Raumvorstellung"])

    st.subheader("Trainingsmodus")
    trainingsstufe = st.selectbox("Wähle ein Trainingslevel", [
        "hoch (beste Genauigkeit)", 
        "mittel (ausgewogen)", 
        "schnell (Vorschau)"
    ])

    if trainingsstufe == "hoch (beste Genauigkeit)":
        presets = "best_quality"
        time_limit = None
    elif trainingsstufe == "mittel (ausgewogen)":
        presets = "medium_quality"
        time_limit = 600
    else:
        presets = "fast_train"
        time_limit = 180

    if st.button("Modelle jetzt trainieren"):
        st.info("Training startet... Dies kann einige Minuten dauern.")

        progress = st.progress(0)
        status = st.empty()

        start_time = time.time()
        status.text("Trainiere Mathematik-Modell...")

        predictor_math = TabularPredictor(label="Mathematik", path=model_path_math).fit(
            df_math.drop(columns=["Raumvorstellung"]),
            presets=presets,
            time_limit=time_limit
        )

        progress.progress(50)
        status.text("Trainiere Raumvorstellung-Modell...")

        predictor_raum = TabularPredictor(label="Raumvorstellung", path=model_path_raum).fit(
            df_raum.drop(columns=["Mathematik"]),
            presets=presets,
            time_limit=time_limit
        )

        progress.progress(100)
        status.success(f"Training abgeschlossen in {int(time.time() - start_time)} Sekunden")

        st.success("Beide Modelle erfolgreich trainiert und gespeichert.")

        st.subheader("Mathematik – Top-Modelle")
        leaderboard_math = predictor_math.leaderboard(silent=True)
        st.dataframe(leaderboard_math[["model", "score_val", "fit_time"]])

        st.subheader("Raumvorstellung – Top-Modelle")
        leaderboard_raum = predictor_raum.leaderboard(silent=True)
        st.dataframe(leaderboard_raum[["model", "score_val", "fit_time"]])
      
