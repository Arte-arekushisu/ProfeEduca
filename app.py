import streamlit as st
import requests
from io import BytesIO
from docx import Document

# 1. Configuración General
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

# Estilo para mejorar la intuición visual
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Menú de Navegación Lateral
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429433.png", width=100)
    st.title("Menú Principal")
    opcion = st.radio("Ir a:", ["🏠 Inicio", "📅 Planeación Semanal", "📝 Reflexión y Evaluación"])
    
    st.divider()
    st.info("**Datos Fijos:**")
    comunidad = st.text_input("Comunidad", "Ej: El Salitre")
    educador = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA de apoyo")

# 3. Funciones de Inteligencia Artificial
def llamar_gemini(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error al conectar con la IA. Inténtalo de nuevo."

# --- SECCIÓN: INICIO ---
if opcion == "🏠 Inicio":
    st.header("¡Bienvenido a Profe.Educa!")
    st.subheader("Sistema Inteligente para el Modelo ABCD")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **¿Qué puedes hacer hoy?**
        * **Planear:** Diseña tus temas de la semana, estaciones y tiempos.
        * **Reflexionar:** Convierte tus notas rápidas en textos profesionales.
        * **Evaluar:** Analiza el progreso de tus alumnos automáticamente.
        """)
    with col2:
        st.info("👈 Selecciona una opción en el menú de la izquierda para comenzar.")

# --- SECCIÓN: PLANEACIÓN ---
elif opcion == "📅 Planeación Semanal":
    st.header("🗓️ Planeador de Temas y Tiempos")
    
    with st.container():
        col_a, col_b = st.columns(2)
        with col_a:
            fecha_p = st.date_input("Fecha de inicio")
            horario = st.text_input("Tiempos pedagógicos (IE)", "8:00 AM - 2:00 PM")
        with col_b:
            tema_p = st.text_input("Tema de la semana")
            
    st.subheader("Detalles del Aula")
    estaciones_manual = st.checkbox("¿Quieres que la IA sugiera los Rincones y Estaciones?")
    
    if st.button("Generar Planeación Completa"):
        prompt_p = f"""
        Actúa como experto CONAFE. Diseña una planeación para el tema '{tema_p}' en la comunidad '{comunidad}'.
        Incluye: 1. Objetivo General, 2. Temas diarios (Lunes-Viernes), 3. Tiempos pedagógicos detallados para {horario}, 
        4. Sugerencia de Rincones y Estaciones de aprendizaje.
        """
        with st.spinner("Diseñando ruta de aprendizaje..."):
            resultado = llamar_gemini(prompt_p)
            st.markdown(resultado)

# --- SECCIÓN: REFLEXIÓN Y EVALUACIÓN ---
elif opcion == "📝 Reflexión y Evaluación":
    st.header("✍️ Bitácora Diaria: Reflexión y Evaluación")
    
    col_x, col_y = st.columns([1, 2])
    with col_x:
        fecha_r = st.date_input("Fecha del reporte")
        tema_r = st.text_input("Tema abordado hoy")
    with col_y:
        notas_aula = st.text_area("¿Qué pasó hoy en el aula?", 
                                  placeholder="Ej: Sofía logró el desafío usando semillas, pero se distrajo con el rincón de lectura...")

    if st.button("Generar Reflexión y Evaluación"):
        prompt_r = f"""
        Basado en el tema '{tema_r}' y estas notas: '{notas_aula}'.
        Genera para el educador '{educador}' en la comunidad '{comunidad}':
        1. UN TEXTO REFLEXIVO profesional (modelo ABCD).
        2. UN EVALUATORIO: Análisis del avance del alumno hoy.
        """
        with st.spinner("Redactando bitácora profesional..."):
            resultado_r = llamar_gemini(prompt_r)
            st.markdown(resultado_r)
