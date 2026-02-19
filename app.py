import streamlit as st
import requests
from io import BytesIO
from docx import Document

# 1. Estilo Dark y Profesional
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .welcome-box {
        padding: 30px; border-radius: 15px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #00d4ff; margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; font-weight: bold; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar con Identificación y Niveles
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    st.divider()
    st.subheader("📍 Datos Generales")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar 1º", "Preescolar 2º", "Preescolar 3º",
        "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º", "Primaria Multigrado",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º", "Secundaria Multigrado"
    ])

# 3. Funciones de IA
def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 4096}}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- SECCIONES ---

if opcion == "🏠 Inicio":
    st.markdown(f"""
    <div class="welcome-box">
        <h1>¡Bienvenido a tu Centro de Planeación Inteligente! 🚀</h1>
        <p style="font-size: 1.2em;">
            Diseñado para que tu labor sea impecable. Este sistema coordina con precisión el <b>Regalo de Lectura</b>, 
            la <b>Dinámica de Bienvenida</b> y el <b>Pase de Lista</b>. Reconocemos que tus <b>Rincones y Estaciones</b> 
            son permanentes; aquí optimizamos la <b>Relación Tutora</b> dentro de ellos. 
            <b>Confía en tu capacidad, nosotros cuidamos la estructura pedagógica.</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación Semanal: {nivel}")
    col1, col2 = st.columns(2)
    with col1:
        obj_general = st.text_area("Objetivo General:")
        tema_p = st.text_input("Tema Principal:")
    with col2:
        trayectorias = st.text_area("Trayectorias Educativas:")

    if st.button("🚀 Generar Planeación Semanal"):
        prompt = f"""
        Actúa como experto pedagogo CONAFE para {nivel}. 
        Genera una planeación semanal que incluya:
        1. DINÁMICA DE BIENVENIDA Y PASE DE LISTA (Diferente cada día).
        2. REGALO DE LECTURA (Títulos y actividades sugeridas).
        3. TRABAJO EN RELACIÓN TUTORA: Cómo usar los RINCONES PERMANENTES para el tema {tema_p}.
        4. HORARIOS: Bloques antes y después del receso.
        5. TEMAS DE RESERVA Y RECURSOS (YouTube/Google).
        Contexto: {comunidad}, Educador: {nombre_ec}, Objetivo: {obj_general}.
        """
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        # Aquí iría la función de descarga a Word que ya tenemos configurada

elif opcion == "✍️ Reflexión Diaria":
    st.header("✍️ Bitácora por Alumno (Campo Formativo)")
    nombre_alumno = st.text_input("Nombre del Alumno:")
    campo = st.selectbox("Campo Formativo:", ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"])
    notas = st.text_area("¿Qué observaste hoy en la relación tutora?")
    
    if st.button("Guardar y Redactar Reflexión"):
        prompt = f"Redacta un texto reflexivo extenso de 2.5 páginas para {nombre_alumno} de {nivel} sobre {campo}. Notas: {notas}."
        res = llamar_ia(prompt)
        st.markdown(res)

elif opcion == "📊 Evaluación Trimestral":
    st.header("📊 Texto Reflexivo Trimestral")
    st.info("Genera el documento final por campo formativo con compromisos y firmas.")
    # Lógica de calificaciones y temas dominados...
