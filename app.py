import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import datetime
from supabase import create_client, Client
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Profe.Educa IA", layout="wide", page_icon="🍎")

# --- 1. CONEXIÓN A MOTORES ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except:
        return None

supabase = init_connection()

# Configurar IA con seguridad
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key and "AIza" in api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ La API Key de Gemini no parece válida. Revisa tus Secrets.")
    model = None

# --- 2. INTERFAZ ---
st.sidebar.title("🍎 Profe.Educa IA")
menu = st.sidebar.radio("Menú", ["Inicio", "Planeación Semanal", "Texto Reflexivo Diario", "Evaluación Trimestral"])

if menu == "Planeación Semanal":
    st.title("📋 Planeación Modelo ABCD")
    
    with st.expander("🤖 Asistente IA CONAFE", expanded=True):
        tema = st.text_input("Tema de la clase:")
        if st.button("Generar Propuesta") and model:
            with st.spinner("Pensando..."):
                prompt = f"Eres un tutor de CONAFE. Crea un desafío y una meta para el tema: {tema} bajo el modelo ABCD."
                res = model.generate_content(prompt)
                st.session_state['propuesta'] = res.text
                st.info("¡Listo! Copia el texto abajo.")

    with st.form("f_plan"):
        meta = st.text_area("Meta de la semana", value=st.session_state.get('propuesta', ''))
        if st.form_submit_button("Guardar"):
            if supabase:
                supabase.table("planeaciones").insert({"meta_semana": meta}).execute()
                st.success("Guardado en la nube")

elif menu == "Texto Reflexivo Diario":
    st.title("✍️ Registro")
    # ... (Tu código de registro anterior)
