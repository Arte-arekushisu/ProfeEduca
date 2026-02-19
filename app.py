import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import datetime
from supabase import create_client, Client
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Profe.Educa IA", layout="wide")

# --- CONEXIÓN SUPABASE ---
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("Error en llaves de Supabase")

# --- CONEXIÓN IA CON RELOJ DE ESPERA ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos 1.5-flash que es más rápido para evitar que se quede pensando
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al configurar IA: {e}")
else:
    st.warning("Falta la GEMINI_API_KEY en Secrets")

# --- INTERFAZ ---
st.sidebar.title("🍎 Profe.Educa IA")
menu = st.sidebar.radio("Menú", ["Planeación Semanal", "Texto Reflexivo Diario"])

if menu == "Planeación Semanal":
    st.title("📋 Planeación Modelo ABCD")
    
    tema = st.text_input("Escribe el tema para la IA:")
    
    if st.button("Generar Propuesta con IA"):
        if not api_key or "AIza" not in api_key:
            st.error("La llave de la IA no es válida. Revisa que no tenga espacios o puntos.")
        else:
            with st.spinner("Conectando con el cerebro de Google..."):
                try:
                    # Instrucción clara para el modelo ABCD
                    prompt = f"Eres un tutor de CONAFE. Crea un desafío breve y una meta para el tema: {tema} usando el modelo ABCD."
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state['propuesta'] = response.text
                        st.success("¡Logrado!")
                    else:
                        st.error("La IA respondió vacío. Revisa tu conexión.")
                except Exception as e:
                    st.error(f"La IA no pudo responder. Error: {e}")

    # Formulario para guardar
    with st.form("f_guardar"):
        meta_final = st.text_area("Resultado de la IA / Meta:", value=st.session_state.get('propuesta', ''))
        if st.form_submit_button("Guardar Planeación"):
            supabase.table("planeaciones").insert({"meta_semana": meta_final}).execute()
            st.success("Guardado en la base de datos.")
