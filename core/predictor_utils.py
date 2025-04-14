import os
from autogluon.tabular import TabularPredictor
import pandas as pd

def load_predictor(model_path):
    """
    Lädt ein AutoGluon-Modell aus dem gegebenen Pfad.
    Gibt None zurück, wenn der Pfad nicht existiert.
    """
    if not os.path.exists(model_path):
        return None
    return TabularPredictor.load(model_path)

def predict_weeks(prognose_daten, predictor_mathe, predictor_raum, letzte_woche, teilnehmer_id):
    """
    Führt die Prognose für Mathematik und Raumvorstellung durch.
    Gibt ein DataFrame mit Wochen und Vorhersagen zurück.
    """
    prognose_ergebnis = {
        "Woche": [],
        "Mathematik (prognostiziert)": [],
        "Raumvorstellung (prognostiziert)": [],
        "Teilnehmer-ID": []
    }

    for woche, features in prognose_daten.items():
        df_features = pd.DataFrame([features])

        mathe_pred = predictor_mathe.predict(df_features)[0]
        raum_pred = predictor_raum.predict(df_features)[0]

        prognose_ergebnis["Woche"].append(woche)
        prognose_ergebnis["Mathematik (prognostiziert)"].append(mathe_pred)
        prognose_ergebnis["Raumvorstellung (prognostiziert)"].append(raum_pred)
        prognose_ergebnis["Teilnehmer-ID"].append(teilnehmer_id)

    return pd.DataFrame(prognose_ergebnis)
  
