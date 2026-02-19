import streamlit as st
import requests
from io import BytesIO
from docx import Document

# 1. Configuración de Estilo Dark e Inspirador
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .welcome-box {
        padding: 30px; border-radius: 15px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #00d4ff; margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; font-weight: bold; border: none; padding: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Navegación y Identificación (Sidebar) con Niveles Corregidos
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("NAVEGACIÓN:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Texto Reflexivo Diario", "📊 Evaluación"])
    
    st.divider()
    st.subheader("📍 Identificación")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    
    # LISTA DE NIVELES CORREGIDA
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar 1º", "Preescolar 2º", "Preescolar 3º",
        "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º",
        "Primaria Multigrado",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º",
        "Secundaria Multigrado"
    ])
    fecha_hoy = st.date_input("Fecha")

# 3. Función de IA
def llamar_gemini(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error al conectar con la IA."

# --- SECCIONES ---

if opcion == "🏠 Inicio":
    st.markdown(f"""
    <div class="welcome-box">
        <h1>¡Bienvenido a tu espacio de confianza, Profe! 🍎</h1>
        <p style="font-size: 1.2em; color: #cbd5e1;">
            Aquí tienes la seguridad de que tu planeación para <b>{nivel}</b> será pedagógicamente sólida. 
            Este sistema entiende los retos de las comunidades y está listo para apoyarte sin errores.
        </p>
        <p style="font-style: italic; color: #00d4ff;">
            "La educación es el arma más poderosa para cambiar el mundo." ¡Manos a la obra!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Nivel Seleccionado", nivel)
    col2.metric("Estatus", "Listo para trabajar")

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación: {nivel}")
    tema_semana = st.text_input("Tema de la semana")
    trayectorias = st.text_area("Trayectorias Educativas (Describe el nivel de avance de tus alumnos)")
    
    if st.button("🚀 Generar Planeación Profesional"):
        prompt = f"""Actúa como experto CONAFE. Genera una planeación ABCD extensa para {nivel}.
        Tema: {tema_semana}. Trayectorias: {trayectorias}. Comunidad: {comunidad}.
        Incluye cronograma detallado, rincones de aprendizaje y desafíos adaptados a {nivel}."""
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "✍️ Texto Reflexivo Diario":
    st.header(f"✍️ Bitácora: {nivel}")
    notas_dia = st.text_area("Notas rápidas de lo que pasó hoy en el aula:", height=200)
    
    if st.button("🪄 Redactar Texto Reflexivo Extenso"):
        prompt = f"""Genera un texto reflexivo ABCD de 2.5 páginas para el nivel {nivel}.
        Usa como base estas notas: {notas_dia}. Habla sobre la relación tutora, el diálogo y el aprendizaje autónomo."""
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "📊 Evaluación":
    st.header(f"📊 Evaluación: {nivel}")
    resumen = st.text_area("Resumen de observaciones de los últimos meses:")
    
    if st.button("📈 Generar Evaluación de Proceso"):
        prompt = f"Genera un reporte evaluatorio trimestral formal para {nivel} basado en: {resumen}. Enfócate en el avance de las trayectorias."
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)
