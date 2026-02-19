import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import datetime
from supabase import create_client, Client
import google.generativeai as genai

# --- 1. CONEXIÓN A MOTORES (SUPABASE Y GEMINI) ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    
    # Configurar Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Error de configuración: {e}")

# --- 2. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Profe.Educa IA", layout="wide", page_icon="🍎")
st.sidebar.title("🍎 Profe.Educa IA")
menu = st.sidebar.radio("Menú Principal", ["Inicio", "Planeación Semanal", "Texto Reflexivo Diario", "Evaluación Trimestral"])

# --- 3. MÓDULO: PLANEACIÓN SEMANAL CON IA ---
if menu == "Planeación Semanal":
    st.title("📋 Planeación Inteligente (Modelo ABCD)")
    
    with st.expander("🤖 Asistente de IA para el Modelo ABCD"):
        tema_ia = st.text_input("¿Qué tema vas a enseñar? (Ej: Fracciones, Ecosistemas, Historia)")
        if st.button("Generar Propuesta ABCD"):
            with st.spinner("La IA está diseñando el desafío..."):
                prompt = f"""Actúa como un experto en el modelo ABCD de CONAFE. 
                Para el tema '{tema_ia}', genera una planeación breve que incluya:
                1. Un DESAFÍO motivador.
                2. Una RUTA DE APRENDIZAJE simple.
                3. Sugerencia de DEMOSTRACIÓN PÚBLICA."""
                response = model.generate_content(prompt)
                st.session_state['propuesta_ia'] = response.text
                st.info(response.text)

    with st.form("form_p"):
        col1, col2 = st.columns(2)
        with col1:
            ec = st.text_input("Educador Comunitario")
        with col2:
            eca = st.text_input("E.C. de Acompañamiento")
        
        # Si la IA generó algo, lo ponemos aquí, si no, queda vacío
        meta = st.text_area("Meta de la semana / Propósito", value=st.session_state.get('propuesta_ia', ''))
        actividades = st.text_area("Actividades (Diálogo y Registro de proceso)")
        
        enviar = st.form_submit_button("Guardar Planeación")

    if enviar:
        data_p = {"educador_nombre": ec, "ec_acompaniamiento": eca, "meta_semana": meta, "actividades": actividades}
        supabase.table("planeaciones").insert(data_p).execute()
        st.success("✅ ¡Guardado en la nube!")
        
        doc = Document()
        doc.add_heading('PLANEACIÓN ABCD - CONAFE', 0)
        doc.add_paragraph(f"Fecha: {datetime.date.today()}\nEC: {ec}\nMeta: {meta}\nActividades: {actividades}")
        buffer = BytesIO(); doc.save(buffer); buffer.seek(0)
        st.download_button("📥 Descargar Word", buffer, f"Planeacion_{ec}.docx")

# --- 4. MÓDULO: REFLEXIÓN DIARIA ---
elif menu == "Texto Reflexivo Diario":
    st.title("✍️ Registro de Relación Tutora")
    with st.form("registro"):
        alumno = st.text_input("Nombre del Alumno")
        notas = st.text_area("Anotaciones del día (Lo que observaste)")
        if st.form_submit_button("Guardar en la Nube"):
            supabase.table("reflexiones").insert({"alumno_nombre": alumno, "contenido_reflexivo": notas}).execute()
            st.success("✅ Guardado permanentemente")

# --- 5. MÓDULO: EVALUACIÓN (RESUMEN IA) ---
elif menu == "Evaluación Trimestral":
    st.title("📊 Resumen Trimestral con IA")
    busqueda = st.text_input("Nombre del alumno")
    if st.button("Analizar Proceso con IA"):
        res = supabase.table("reflexiones").select("*").ilike("alumno_nombre", f"%{busqueda}%").execute()
        if res.data:
            textos = " ".join([r['contenido_reflexivo'] for r in res.data])
            with st.spinner("Analizando todas las reflexiones..."):
                prompt_ev = f"Basado en estas notas de clase: '{textos}', redacta un breve reporte de evaluación trimestral destacando logros y áreas de mejora para el alumno {busqueda}."
                response_ev = model.generate_content(prompt_ev)
                st.subheader("Resultado del Análisis:")
                st.write(response_ev.text)
        else:
            st.warning("No hay datos para analizar.")
