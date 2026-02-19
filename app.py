import streamlit as st
import requests
from io import BytesIO
from docx import Document

# 1. Configuración de Estilo y Modo Oscuro
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    /* Fondo oscuro y fuentes */
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    
    /* Botones personalizados */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    
    /* Inputs y Textareas */
    textarea { background-color: #262730 !important; color: white !important; }
    input { background-color: #262730 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Navegación Lateral
with st.sidebar:
    st.title("🍎 Profe.Educa")
    st.markdown("---")
    opcion = st.radio("MENÚ DE NAVEGACIÓN:", 
                      ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Texto Reflexivo Diario", "📊 Evaluación Trimestral"])
    
    st.divider()
    st.subheader("📍 Datos Generales")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA (Acompañamiento)")
    fecha_hoy = st.date_input("Fecha de hoy")

# 3. Función para llamar a Gemini (Extensivo)
def llamar_gemini(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000} # Aumentado para textos largos
    }
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error de conexión con la IA."

# --- SECCIÓN 🏠 INICIO ---
if opcion == "🏠 Inicio":
    st.header("¡Bienvenido, Profe!")
    st.subheader("Sistema Inteligente de Gestión ABCD")
    st.markdown(f"""
    Hola **{nombre_ec if nombre_ec else "Colega"}**, esta herramienta está diseñada para facilitar tu labor docente.
    
    - **📅 Planeación:** Organiza tus temas, tiempos y trayectorias.
    - **✍️ Reflexión Diaria:** Captura lo que sucede en el tutoría o estaciones.
    - **📊 Evaluación:** Genera reportes profundos basados en tus reflexiones diarias.
    """)
    st.info("Utiliza el menú de la izquierda para navegar por las secciones.")

# --- SECCIÓN 📅 PLANEACIÓN ---
elif opcion == "📅 Planeación Semanal":
    st.header("🗓️ Planeación Semanal ABCD")
    
    col1, col2 = st.columns(2)
    with col1:
        tema_semana = st.text_input("Tema de la semana")
        tiempos = st.text_input("Tiempos pedagógicos (IE)", "8:00 AM - 2:30 PM")
    with col2:
        trayectorias = st.text_area("Trayectorias Educativas (Ingresa los niveles o metas de los alumnos)")

    if st.button("Generar Planeación Completa"):
        prompt = f"""
        Actúa como experto CONAFE. Genera una PLANEACIÓN extensa para la comunidad {comunidad}.
        EDUCADOR: {nombre_ec} | ECA: {eca} | FECHA: {fecha_hoy}
        TEMA: {tema_semana} | TIEMPOS: {tiempos} | TRAYECTORIAS: {trayectorias}
        
        Desglosa: Objetivo General, Cronograma Lunes-Viernes, Rincones/Estaciones sugeridos y 
        cómo vincular las trayectorias mencionadas con el modelo ABCD.
        """
        resultado = llamar_gemini(prompt)
        st.session_state.temp_content = resultado
        st.markdown(resultado)

# --- SECCIÓN ✍️ REFLEXIÓN DIARIA ---
elif opcion == "✍️ Texto Reflexivo Diario":
    st.header("✍️ Texto Reflexivo (Bitácora Diaria)")
    st.info("Captura tus observaciones sobre los aprendizajes en tutoría, rincones o estaciones.")
    
    notas_dia = st.text_area("¿Qué observaste hoy con tus alumnos?", height=200,
                             placeholder="Ej: Durante la tutoría en el rincón de matemáticas, Luis logró entender la suma...")

    if st.button("Redactar Reflexión Profunda"):
        prompt = f"""
        Genera un TEXTO REFLEXIVO DIARIO EXTENSO (mínimo 1.5 a 2 páginas de contenido teórico-práctico).
        BASADO EN: '{notas_dia}'
        COMUNIDAD: {comunidad} | EDUCADOR: {nombre_ec} | FECHA: {fecha_hoy}
        
        Usa terminología del Modelo ABCD: diálogo, aprendizaje autónomo, relación tutora, metacognición.
        Analiza cómo el alumno interactuó en las estaciones o rincones. Debe ser una narrativa profesional y profunda.
        """
        resultado = llamar_gemini(prompt)
        st.session_state.temp_content = resultado
        st.markdown(resultado)

# --- SECCIÓN 📊 EVALUACIÓN ---
elif opcion == "📊 Evaluación Trimestral":
    st.header("📊 Texto Evaluatorio Trimestral")
    st.info("Este documento une tus reflexiones diarias para dar un veredicto del avance del alumno.")
    
    resumen_notas = st.text_area("Pega aquí un resumen de tus reflexiones diarias o notas clave de los últimos meses:")

    if st.button("Generar Evaluación de Proceso"):
        prompt = f"""
        Actúa como supervisor pedagógico CONAFE. Genera un TEXTO EVALUATORIO extenso.
        CONTEXTO: {comunidad} | EDUCADOR: {nombre_ec}
        NOTAS DEL PROCESO: {resumen_notas}
        
        Analiza el avance trimestral del alumno, los logros en su trayectoria educativa, 
        el nivel de autonomía alcanzado y áreas de oportunidad. El texto debe ser muy formal y detallado.
        """
        resultado = llamar_gemini(prompt)
        st.session_state.temp_content = resultado
        st.markdown(resultado)
