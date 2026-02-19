import streamlit as st
import requests
from io import BytesIO
from docx import Document

# 1. Configuración de Estilo Oscuro
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Navegación y Datos en el Sidebar
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Texto Reflexivo Diario", "📊 Evaluación"])
    
    st.divider()
    st.subheader("📍 Datos de Identificación")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    
    # NUEVO: Selección de Nivel Educativo
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar", 
        "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º", "Secundaria 4º", "Secundaria 5º"
    ])
    fecha_hoy = st.date_input("Fecha")

# 3. Función de IA (Extensiva)
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

# --- Lógica de Secciones ---

if opcion == "🏠 Inicio":
    st.header(f"¡Bienvenido, Profe!")
    st.write(f"Nivel actual configurado: **{nivel}**")
    st.info("Configura tus datos en el menú lateral y selecciona una herramienta para comenzar.")

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación: {nivel}")
    col1, col2 = st.columns(2)
    with col1:
        tema_semana = st.text_input("Tema de la semana")
        tiempos = st.text_input("Horario IE", "8:00 AM - 2:30 PM")
    with col2:
        trayectorias = st.text_area("Trayectorias Educativas del alumno")

    if st.button("Generar Planeación ABCD"):
        prompt = f"""
        Actúa como experto CONAFE. Genera una PLANEACIÓN ABCD EXTENSA para el nivel {nivel}.
        COMUNIDAD: {comunidad} | EDUCADOR: {nombre_ec} | ECA: {eca}
        TEMA: {tema_semana} | TIEMPOS: {tiempos} | TRAYECTORIAS: {trayectorias}
        
        Adecua el lenguaje y los desafíos al nivel {nivel}. 
        Incluye: Objetivo, Cronograma Lunes-Viernes y Rincones de aprendizaje específicos.
        """
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "✍️ Texto Reflexivo Diario":
    st.header(f"✍️ Bitácora Diaria: {nivel}")
    notas_dia = st.text_area("Notas breves de lo observado hoy:", height=200)

    if st.button("Redactar Reflexión Profunda"):
        prompt = f"""
        Genera un TEXTO REFLEXIVO DIARIO MUY EXTENSO (2 a 2.5 páginas).
        NIVEL: {nivel} | COMUNIDAD: {comunidad} | EDUCADOR: {nombre_ec}
        NOTAS DEL DÍA: '{notas_dia}'
        
        Usa terminología ABCD: relación tutora, diálogo, autonomía. Analiza el proceso de aprendizaje 
        específicamente para un alumno de {nivel}. Sé muy detallado en la narrativa pedagógica.
        """
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "📊 Evaluación":
    st.header(f"📊 Evaluación de Proceso: {nivel}")
    resumen = st.text_area("Notas acumuladas del trimestre:")

    if st.button("Generar Texto Evaluatorio"):
        prompt = f"""
        Genera un TEXTO EVALUATORIO TRIMESTRAL extenso para {nivel}.
        EDUCADOR: {nombre_ec} | COMUNIDAD: {comunidad}
        NOTAS ACUMULADAS: {resumen}
        
        Evalúa el avance en la trayectoria educativa, la autonomía y el dominio del modelo ABCD.
        """
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)
