import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from core.predictor_utils import load_predictor, predict_weeks
from core.feature_engineering import prepare_features_for_prediction

st.set_page_config(page_title="03 - Teilnehmer Prognose", layout="wide")

st.title("📈 Teilnehmer-Prognose")
st.markdown("Gib die bekannten Werte ein – der PrognoseTrainer sagt dir, wie es weitergeht!")

# === 1. Modelle laden ===
predictor_mathe = load_predictor("models/model_mathematik")
predictor_raum = load_predictor("models/model_raumvorstellung")

if predictor_mathe is None or predictor_raum is None:
    st.error("❗ Modelle nicht gefunden. Bitte zuerst trainieren (Seite: 02 - Training).")
    st.stop()

# === 2. Teilnehmerdaten eingeben ===
with st.form("prognose_formular"):
    teilnehmer_id = st.number_input("Teilnehmer-ID", min_value=1, max_value=9999, step=1)
    letzte_woche = st.slider("Letzte bekannte Woche", min_value=1, max_value=16, value=6)

    col1, col2 = st.columns(2)
    mathe_values = []
    raum_values = []

    for w in range(1, letzte_woche + 1):
        with col1:
            mathe = st.slider(f"Woche {w} – Mathematik (%)", 0, 100, 50, key=f"mathe_{w}")
        with col2:
            raum = st.slider(f"Woche {w} – Raumvorstellung (%)", 0, 100, 50, key=f"raum_{w}")
        mathe_values.append(mathe)
        raum_values.append(raum)

    submitted = st.form_submit_button("🚀 Prognose starten")

if submitted:
    # === 3. Datenframe erstellen ===
    eingabe_df = pd.DataFrame({
        "Woche": list(range(1, letzte_woche + 1)),
        "Mathematik": mathe_values,
        "Raumvorstellung": raum_values,
        "Teilnehmer-ID": [teilnehmer_id] * letzte_woche
    })

    # === 4. Prognose durchführen ===
    prognose_daten = prepare_features_for_prediction(eingabe_df, letzte_woche)
    df_ergebnis = predict_weeks(
        prognose_daten=prognose_daten,
        predictor_mathe=predictor_mathe,
        predictor_raum=predictor_raum,
        letzte_woche=letzte_woche,
        teilnehmer_id=teilnehmer_id
    )

    # === 5. Ausgabe Tabelle ===
    st.subheader("📊 Prognose-Tabelle")
    st.dataframe(df_ergebnis, use_container_width=True)

    # === 6. Plot erstellen ===
    fig = go.Figure()
    wochen_gesamt = list(range(1, 17))

    # Echte Werte
    fig.add_trace(go.Scatter(
        x=wochen_gesamt[:letzte_woche],
        y=mathe_values,
        mode="lines+markers",
        name="📘 Mathematik (bisher)",
        line=dict(dash="solid")
    ))
    fig.add_trace(go.Scatter(
        x=wochen_gesamt[:letzte_woche],
        y=raum_values,
        mode="lines+markers",
        name="📗 Raumvorstellung (bisher)",
        line=dict(dash="solid")
    ))

    # Prognosen
    fig.add_trace(go.Scatter(
        x=df_ergebnis["Woche"],
        y=df_ergebnis["Mathematik (prognostiziert)"],
        mode="lines+markers",
        name="🔮 Mathematik (Prognose)",
        line=dict(dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df_ergebnis["Woche"],
        y=df_ergebnis["Raumvorstellung (prognostiziert)"],
        mode="lines+markers",
        name="🔮 Raumvorstellung (Prognose)",
        line=dict(dash="dash")
    ))

    fig.update_layout(
        title=f"📈 Prognose für Teilnehmer: {teilnehmer_id}",
        xaxis_title="Woche",
        yaxis_title="Leistung (%)",
        xaxis=dict(tickmode="linear", dtick=1),
        yaxis=dict(range=[0, 100]),
        template="simple_white"
    )
    st.plotly_chart(fig, use_container_width=True)
  
