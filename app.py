import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import datetime
from supabase import create_client, Client
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE MOTORES ---
try:
    # Conexión Supabase
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    
    # Conexión Gemini (IA)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Usamos pro para mayor estabilidad
    model = genai.GenerativeModel('gemini-1.5-pro') 
except Exception as e:
    st.error(f"⚠️ Error en configuración de llaves: {e}")

# --- 2. DISEÑO DE LA APP ---
st.set_page_config(page_title="Profe.Educa IA", layout="wide", page_icon="🍎")
st.sidebar.title("🍎 Profe.Educa IA")
menu = st.sidebar.radio("Menú Principal", ["Inicio", "Planeación Semanal", "Texto Reflexivo Diario", "Evaluación Trimestral"])

# --- 3. MÓDULO: PLANEACIÓN SEMANAL ---
if menu == "Planeación Semanal":
    st.title("📋 Planeación Inteligente Modelo ABCD")
    
    # Asistente de IA
    with st.expander("🤖 Asistente de IA (Modelo ABCD)", expanded=True):
        tema = st.text_input("¿Qué tema quieres planear hoy?")
        if st.button("Generar con IA"):
            with st.spinner("Diseñando desafío pedagógico..."):
                prompt = f"Actúa como un tutor experto en el modelo ABCD de CONAFE. Crea una meta y actividades para el tema: {tema}. Usa lenguaje sencillo y enfocado al diálogo tutora."
                response = model.generate_content(prompt)
                st.session_state['propuesta'] = response.text
                st.info("✅ Propuesta generada. Puedes copiarla abajo.")

    with st.form("form_plan"):
        ec = st.text_input("Nombre del Educador")
        meta_ia = st.text_area("Meta de la semana", value=st.session_state.get('propuesta', ''))
        actividades = st.text_area("Actividades y Registro de proceso")
        
        boton_guardar = st.form_submit_button("Guardar Planeación")
        
        if boton_guardar:
            datos = {"educador_nombre": ec, "meta_semana": meta_ia, "actividades": actividades}
            supabase.table("planeaciones").insert(datos).execute()
            st.success("🎉 ¡Guardado en Supabase!")

# --- 4. MÓDULO: REFLEXIÓN DIARIA ---
elif menu == "Texto Reflexivo Diario":
    st.title("✍️ Registro de Relación Tutora")
    with st.form("form_ref"):
        alumno = st.text_input("Alumno")
        notas = st.text_area("Notas del proceso")
        if st.form_submit_button("Guardar"):
            supabase.table("reflexiones").insert({"alumno_nombre": alumno, "contenido_reflexivo": notas}).execute()
            st.success("✅ Registrado")

# --- 5. MÓDULO: EVALUACIÓN ---
elif menu == "Evaluación Trimestral":
    st.title("📊 Análisis de Avance")
    nombre = st.text_input("Nombre del alumno a analizar")
    if st.button("Generar Reporte con IA"):
        res = supabase.table("reflexiones").select("contenido_reflexivo").eq("alumno_nombre", nombre).execute()
        if res.data:
            todo_texto = " ".join([r['contenido_reflexivo'] for r in res.data])
            analisis = model.generate_content(f"Resume el avance académico de este alumno basándote en estas notas: {todo_texto}")
            st.write(analisis.text)
        else:
            st.warning("No hay notas para este alumno.")
