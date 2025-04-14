# CODE FÜR pages/04_manage_models.py

page04_code = '''
import streamlit as st
import shutil
import os
from datetime import datetime

st.set_page_config(page_title="PrognoseTrainer – Modelle verwalten", layout="wide")
st.title("Modellverwaltung – Laden, Löschen, Backup")

model_path_math = "models/model_mathematik"
model_path_raum = "models/model_raumvorstellung"
backup_path = "models/_backups/"

def model_info(path):
    if not os.path.exists(path):
        return "❌ Nicht vorhanden"
    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, filenames in os.walk(path) for f in filenames)
    size_mb = size / 1024 / 1024
    last_modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
    return f"✅ {round(size_mb,1)} MB – geändert am {last_modified}"

def backup_model(src, name):
    dst = os.path.join(backup_path, f"{name}_backup")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def restore_model(name):
    src = os.path.join(backup_path, f"{name}_backup")
    dst = name
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        return True
    return False

st.subheader("Modellstatus & Info")
st.write(f"**Mathematik-Modell:** {model_info(model_path_math)}")
st.write(f"**Raumvorstellung-Modell:** {model_info(model_path_raum)}")

st.subheader("Modelle sichern (Backup)")
col1, col2 = st.columns(2)
with col1:
    if os.path.exists(model_path_math):
        if st.button("Backup: Mathematik-Modell"):
            backup_model(model_path_math, model_path_math)
            st.success("Backup erstellt.")
with col2:
    if os.path.exists(model_path_raum):
        if st.button("Backup: Raumvorstellung-Modell"):
            backup_model(model_path_raum, model_path_raum)
            st.success("Backup erstellt.")

st.subheader("Modelle wiederherstellen (Restore)")
col3, col4 = st.columns(2)
with col3:
    if st.button("Restore: Mathematik aus Backup"):
        if restore_model(model_path_math):
            st.success("Mathematik-Modell wiederhergestellt.")
        else:
            st.warning("Kein Backup gefunden.")
with col4:
    if st.button("Restore: Raumvorstellung aus Backup"):
        if restore_model(model_path_raum):
            st.success("Raumvorstellung-Modell wiederhergestellt.")
        else:
            st.warning("Kein Backup gefunden.")

st.subheader("Modelle löschen (Vorsicht!)")
if st.button("Beide Modelle löschen"):
    if os.path.exists(model_path_math):
        shutil.rmtree(model_path_math)
    if os.path.exists(model_path_raum):
        shutil.rmtree(model_path_raum)
    st.success("Beide Modelle gelöscht.")

col_del1, col_del2 = st.columns(2)
with col_del1:
    if os.path.exists(model_path_math):
        if st.button("Nur Mathematik-Modell löschen"):
            shutil.rmtree(model_path_math)
            st.success("Mathematik-Modell gelöscht.")
with col_del2:
    if os.path.exists(model_path_raum):
        if st.button("Nur Raumvorstellung-Modell löschen"):
            shutil.rmtree(model_path_raum)
            st.success("Raumvorstellung-Modell gelöscht.")
'''

with open("/mnt/data/prognosetrainer/pages/04_manage_models.py", "w") as f:
    f.write(page04_code)

"/mnt/data/prognosetrainer/pages/04_manage_models.py gespeichert"
