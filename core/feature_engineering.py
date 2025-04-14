import pandas as pd

def prepare_features_for_prediction(df_eingabe: pd.DataFrame, letzte_woche: int):
    """
    Nimmt die bisher bekannten Wochen-Daten eines Teilnehmers
    und erstellt die Feature-Daten für die Prognose der nächsten Wochen (bis Woche 16).
    """
    df_sorted = df_eingabe.sort_values("Woche")
    teilnehmer_id = df_sorted["Teilnehmer-ID"].iloc[0]

    # Durchschnitt bisheriger Leistungen
    df_mathe = df_sorted["Mathematik"]
    df_raum = df_sorted["Raumvorstellung"]

    durchschnitt_mathe = df_mathe.mean()
    durchschnitt_raum = df_raum.mean()

    letzte_mathe = df_mathe.iloc[-1]
    letzte_raum = df_raum.iloc[-1]

    trend_mathe = df_mathe.diff().mean()
    trend_raum = df_raum.diff().mean()

    # Feature-Vorbereitung pro zukünftige Woche
    prognose_daten = {}

    for woche in range(letzte_woche + 1, 17):
        prognose_daten[woche] = {
            "Woche": woche,
            "Teilnehmer-ID": teilnehmer_id,
            "Ø_Mathe_bis_Woche": durchschnitt_mathe,
            "Letzte_Mathe": letzte_mathe,
            "Trend_Mathe": trend_mathe,
            "Ø_Raum_bis_Woche": durchschnitt_raum,
            "Letzte_Raum": letzte_raum,
            "Trend_Raum": trend_raum
        }

    return prognose_daten
  
