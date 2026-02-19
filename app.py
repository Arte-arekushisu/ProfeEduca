import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Configuración de Estilo
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

# 2. Función de Exportación a Word (Versión Planeación Limpia)
def generar_word_planeacion(titulo, contenido, d):
    doc = Document()
    h = doc.add_heading(titulo, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Encabezado sin firmas
    table = doc.add_table(rows=3, cols=2)
    table.cell(0, 0).text = f"Comunidad: {d['comunidad']}"
    table.cell(0, 1).text = f"Fecha: {d['fecha']}"
    table.cell(1, 0).text = f"Educador: {d['nombre']}"
    table.cell(1, 1).text = f"Nivel: {d['nivel']}"
    table.cell(2, 0).text = f"ECA: {d['eca']}"
    
    doc.add_paragraph("\n" + "="*50 + "\n")
    
    # Limpieza de texto (quitar asteriscos de formato markdown para el Word)
    texto_limpio = contenido.replace("**", "").replace("*", "-")
    
    para = doc.add_paragraph(texto_limpio)
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Sidebar
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    st.divider()
    comunidad = st.text_input("Comunidad", "PARAJES DEL VALLE")
    nombre_ec = st.text_input("Educador Comunitario", "AXEL REYES")
    eca = st.text_input("ECA", "MOISES ROSAS")
    nivel = st.selectbox("Nivel Educativo:", ["Secundaria Multigrado", "Primaria Multigrado", "Preescolar", "Primaria 1-6", "Secundaria 1-3"])
    fecha_hoy = st.date_input("Fecha de Inicio")

datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel, "fecha": str(fecha_hoy)}

def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.5}}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- SECCIONES ---

if opcion == "🏠 Inicio":
    st.markdown("""
    <div class="welcome-box">
        <h1>Planeación Estructural ABCD 🚀</h1>
        <p>Genera documentos profesionales sin distracciones visuales. Aquí la planeación es una hoja de ruta clara de Lunes a Viernes con horarios pedagógicos estrictos.</p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación Semanal: {nivel}")
    col1, col2 = st.columns(2)
    with col1:
        tema_p = st.text_input("Tema de la Unidad (UAA):")
        rincón_p = st.text_input("Rincón Permanente a usar:", placeholder="Ej. Rincón de Lectura / Rincón de Ciencia")
    with col2:
        objetivo = st.text_area("Objetivo General:")

    if st.button("🚀 Generar Planeación Completa"):
        prompt = f"""
        Actúa como experto CONAFE. Genera una planeación SEMANAL (Lunes a Viernes) para {nivel}.
        TEMA: {tema_p} | RINCÓN PERMANENTE: {rincón_p} | OBJETIVO: {objetivo}.
        
        FORMATO OBLIGATORIO POR DÍA (Sin usar asteriscos **):
        8:00 - 8:15: Bienvenida y Pase de Lista.
        8:15 - 8:45: Regalo de Lectura (Sugerir dinámica).
        8:45 - 10:30: Relación Tutora - Propón una ESTACIÓN DE TRABAJO específica para el rincón {rincón_p}.
        10:30 - 11:00: Receso.
        11:00 - 13:30: Continuación de Tutoría y demostración pública.
        13:30 - 14:00: Puesta en común y cierre.
        
        Al final, incluye 2 temas de reserva y recursos de estudio. NO incluyas espacios de firmas aquí.
        """
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        st.download_button("📥 Descargar Word", generar_word_planeacion("PLANEACIÓN SEMANAL", resultado, datos_id), "Planeacion.docx")

# ... (Las otras secciones se mantienen con sus funciones de firma correspondientes)
