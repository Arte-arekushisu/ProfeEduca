import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Estilo Visual Dark & Inspiring
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    
    /* Caja de Bienvenida */
    .welcome-box {
        padding: 30px;
        border-radius: 15px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #00d4ff;
        margin-bottom: 25px;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Navegación y Datos (Sidebar)
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("NAVEGACIÓN:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Texto Reflexivo Diario", "📊 Evaluación"])
    
    st.divider()
    st.subheader("📍 Identificación")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar", "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º", "Secundaria 4º", "Secundaria 5º"
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
            Sabemos que tu labor en la comunidad transforma vidas. Aquí, no solo generas papeles; 
            <b>construyes el futuro.</b> Siéntete seguro: este sistema ha sido diseñado para que 
            cada planeación y reflexión sea impecable, pedagógicamente sólida y libre de errores.
        </p>
        <hr style="border-color: #334155;">
        <p style="font-style: italic; color: #00d4ff;">
            "La educación no cambia al mundo, cambia a las personas que van a cambiar al mundo." 
            ¡Vamos a planear con excelencia hoy!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Nivel", nivel)
    col2.metric("Comunidad", comunidad if comunidad else "---")
    col3.metric("Estatus", "Listo para trabajar")

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación: {nivel}")
    tema_semana = st.text_input("Tema de la semana")
    trayectorias = st.text_area("Trayectorias Educativas del alumno")
    
    if st.button("🚀 Generar Planeación"):
        prompt = f"Genera planeación ABCD nivel {nivel} para {tema_semana} con trayectorias {trayectorias} en comunidad {comunidad}. Sé extenso y profesional."
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "✍️ Texto Reflexivo Diario":
    st.header(f"✍️ Bitácora: {nivel}")
    notas_dia = st.text_area("¿Qué observaste hoy?", height=200)
    
    if st.button("🪄 Redactar Reflexión Profunda"):
        prompt = f"Genera texto reflexivo ABCD de 2.5 páginas para {nivel} basado en: {notas_dia}. Usa lenguaje de relación tutora y diálogo."
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "📊 Evaluación":
    st.header(f"📊 Evaluación: {nivel}")
    resumen = st.text_area("Notas acumuladas:")
    
    if st.button("📈 Generar Evaluación"):
        prompt = f"Genera evaluación trimestral formal para {nivel} en {comunidad} basándote en: {resumen}."
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)
