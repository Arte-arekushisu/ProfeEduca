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
        padding: 25px; border-radius: 15px;
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

# 2. Sidebar de Identificación
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("NAVEGACIÓN:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Texto Reflexivo Diario", "📊 Evaluación"])
    
    st.divider()
    st.subheader("📍 Datos de la Comunidad")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar 1º", "Preescolar 2º", "Preescolar 3º",
        "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º",
        "Primaria Multigrado",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º",
        "Secundaria Multigrado"
    ])
    fecha_hoy = st.date_input("Fecha de inicio")

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
        <h1>Tu Planeación con Tiempos Pedagógicos CONAFE 🍎</h1>
        <p style="font-size: 1.1em; color: #cbd5e1;">
            Este sistema ahora integra el <b>Regalo de Lectura</b>, el Pase de Lista y la organización de 
            <b>Relación Tutora</b> antes y después del receso. Todo estructurado por tiempos para que 
            no pierdas el ritmo en el aula.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación Semanal Estandarizada: {nivel}")
    tema_principal = st.text_input("Tema Principal de la semana")
    trayectorias = st.text_area("Trayectorias Educativas de los alumnos")

    if st.button("🚀 Generar Planeación con Horarios CONAFE"):
        prompt = f"""
        Actúa como experto pedagogo CONAFE. Genera una planeación SEMANAL completa para {nivel}.
        TEMA PRINCIPAL: {tema_principal} | TEMAS DE RESERVA: Incluye 2 temas más.
        COMUNIDAD: {comunidad} | EDUCADOR: {nombre_ec}
        
        ESTRUCTURA DIARIA POR TIEMPOS (Usa este formato para cada día):
        1. 8:00 - 8:15: Bienvenida, Pase de Lista y Actividad para empezar bien el día.
        2. 8:15 - 8:45: REGALO DE LECTURA (Sugiere un tipo de lectura o dinámica).
        3. 8:45 - 10:30: TRABAJO EN RELACIÓN TUTORA / ESTACIONES (Primer bloque).
        4. 10:30 - 11:00: RECESO Y JUEGO LIBRE.
        5. 11:00 - 1:30: SEGUNDO BLOQUE (Continuación de tutoría, rincones o demostración pública).
        6. 1:30 - 2:00: PUESTA EN COMÚN Y TEXTO REFLEXIVO.
        
        Además, incluye:
        - Recursos de estudio (YouTube/Google) para el educador.
        - Cómo manejar el multigrado o nivel {nivel} en estos tiempos.
        """
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "✍️ Texto Reflexivo Diario":
    st.header(f"✍️ Bitácora de Observación: {nivel}")
    notas_dia = st.text_area("¿Qué pasó hoy en los tiempos pedagógicos?", height=200)
    if st.button("Redactar Reflexión Profunda"):
        prompt = f"Genera un texto reflexivo ABCD de 2.5 páginas sobre: {notas_dia}. Enfócate en la metacognición del alumno."
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)

elif opcion == "📊 Evaluación":
    st.header(f"📊 Evaluación Trimestral: {nivel}")
    resumen = st.text_area("Notas acumuladas del trimestre:")
    if st.button("Generar Evaluación"):
        prompt = f"Genera una evaluación formal del proceso ABCD para {nivel} basada en: {resumen}."
        resultado = llamar_gemini(prompt)
        st.markdown(resultado)
