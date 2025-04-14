import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="PrognoseTrainer – Daten vorbereiten", layout="wide")
st.title("Daten vorbereiten für PrognoseTrainer")

uploaded_file = st.file_uploader("Lade deine Excel-Datei hoch:", type=["xlsx"])

def extract_features(df_long: pd.DataFrame) -> pd.DataFrame:
    feature_rows = []

    for teilnehmer_id, gruppe in df_long.groupby("Teilnehmer-ID"):
        gruppe = gruppe.sort_values("Woche")
        for woche in range(2, 17):  # ab Woche 2 möglich
            bisher = gruppe[gruppe["Woche"] < woche]
            if bisher.empty:
                continue

            letzte_math = bisher["Mathematik"].dropna().values[-1] if not bisher["Mathematik"].dropna().empty else np.nan
            letzte_raum = bisher["Raumvorstellung"].dropna().values[-1] if not bisher["Raumvorstellung"].dropna().empty else np.nan

            Ø_math = bisher["Mathematik"].mean()
            Ø_raum = bisher["Raumvorstellung"].mean()

            trend_math = Ø_math - bisher["Mathematik"].iloc[0]
            trend_raum = Ø_raum - bisher["Raumvorstellung"].iloc[0]

            row = {
                "Teilnehmer-ID": teilnehmer_id,
                "Woche": woche,
                "Ø_Mathe_bis_Woche": Ø_math,
                "Letzte_Mathe": letzte_math,
                "Trend_Mathe": trend_math,
                "Ø_Raum_bis_Woche": Ø_raum,
                "Letzte_Raum": letzte_raum,
                "Trend_Raum": trend_raum
            }

            ziel = gruppe[gruppe["Woche"] == woche]
            if not ziel.empty:
                row["Mathematik"] = ziel["Mathematik"].values[0]
                row["Raumvorstellung"] = ziel["Raumvorstellung"].values[0]

            feature_rows.append(row)

    df_features = pd.DataFrame(feature_rows)
    return df_features

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    df_raw = df_raw.replace("Ne", np.nan)

    # Umwandlung in Long Format
    df_long = pd.DataFrame()
    for i, row in df_raw.iterrows():
        for woche in range(1, 17):
            math_col = f"Woche {woche} - Mathematik (%)"
            raum_col = f"Woche {woche} - Raumvorstellung (%)"
            if math_col in df_raw.columns and raum_col in df_raw.columns:
                df_long = pd.concat([
                    df_long,
                    pd.DataFrame({
                        "Teilnehmer-ID": [row["Teilnehmer-ID"]],
                        "Woche": [woche],
                        "Mathematik": [pd.to_numeric(row[math_col], errors='coerce')],
                        "Raumvorstellung": [pd.to_numeric(row[raum_col], errors='coerce')],
                    })
                ], ignore_index=True)

    st.subheader("Vorschau der aufbereiteten Rohdaten")
    st.dataframe(df_long.head(30))

    df_features = extract_features(df_long)

    st.subheader("Feature-Tabelle für AutoGluon")
    st.dataframe(df_features.head(30))

    csv_data = df_features.to_csv(index=False).encode("utf-8")
    st.download_button("Feature-Tabelle als CSV herunterladen", csv_data, file_name="trainingsdaten_autogluon.csv", mime="text/csv")
  
