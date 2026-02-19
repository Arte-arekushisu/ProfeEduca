import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Configuración de Estilo y Página
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

# 2. Funciones de Exportación a Word
def generar_word_limpio(titulo, contenido, d, con_firmas=False):
    doc = Document()
    h = doc.add_heading(titulo, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    table = doc.add_table(rows=3, cols=2)
    table.cell(0, 0).text = f"Comunidad: {d['comunidad']}"
    table.cell(0, 1).text = f"Fecha: {d['fecha']}"
    table.cell(1, 0).text = f"Educador: {d['nombre']}"
    table.cell(1, 1).text = f"Nivel: {d['nivel']}"
    table.cell(2, 0).text = f"ECA: {d['eca']}"
    
    doc.add_paragraph("\n" + "="*50 + "\n")
    
    texto_limpio = contenido.replace("**", "").replace("*", "-")
    para = doc.add_paragraph(texto_limpio)
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if con_firmas:
        doc.add_paragraph("\n\n\n")
        f_table = doc.add_table(rows=1, cols=2)
        f_table.cell(0, 0).text = "__________________________\nFirma del Educador"
        f_table.cell(0, 1).text = "__________________________\nFirma Padre/APEC"
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Identificación y Menú
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    st.divider()
    comunidad = st.text_input("Comunidad", "PARAJES DEL VALLE")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    eca = st.text_input("ECA", "MOISES ROSAS")
    nivel = st.selectbox("Nivel:", ["Secundaria Multigrado", "Primaria Multigrado", "Preescolar", "Primaria 1-6", "Secundaria 1-3"])
    fecha_hoy = st.date_input("Fecha")

# DICCIONARIO CORREGIDO (Línea 72 de tu imagen original)
datos_id = {
    "comunidad": comunidad, 
    "nombre": nombre_ec, 
    "eca": eca, 
    "nivel": nivel, 
    "fecha": str(fecha_hoy)
}

# 4. Función de IA
def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.5}}
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error al conectar. Revisa tu API Key."

# --- SECCIONES ---

if opcion == "🏠 Inicio":
    st.markdown("""
    <div class="welcome-box">
        <h1>Planeación Estructural ABCD 🚀</h1>
        <p>Tu espacio seguro para organizar la comunidad. Genera planeaciones con horarios pedagógicos, enlaces de estudio y estaciones renovables.</p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación: {nivel}")
    tema = st.text_input("Tema de la Unidad (UAA):")
    rincón = st.text_input("Rincón Permanente:")
    obj = st.text_area("Objetivo General:")
    
    if st.button("🚀 Generar Planeación Completa"):
        prompt = f"Genera planeación SEMANAL CONAFE para {nivel}. Tema: {tema}. Rincón: {rincón}. HORARIOS DIARIOS (8:00 a 14:00): - Bienvenida, Pase de Lista, Regalo de Lectura. - Relación Tutora: Propón una ESTACIÓN DE TRABAJO semanal para el rincón {rincón}. CAJA DE HERRAMIENTAS: - Incluye frases de búsqueda para YouTube y Google sobre {tema} para que el educador estudie. - 3 conceptos clave. Sin asteriscos ni firmas."
        res = llamar_ia(prompt)
        st.markdown(res)
        st.download_button("📥 Descargar Planeación (Word)", generar_word_limpio("PLANEACIÓN SEMANAL", res, datos_id), "Planeacion.docx")

elif opcion == "✍️ Reflexión Diaria":
    st.header("✍️ Reflexión Diaria")
    alumno = st.text_input("Nombre del Alumno:")
    notas = st.text_area("Notas del día:")
    if st.button("🪄 Redactar"):
        prompt = f"Redacta reflexión diaria de 2.5 páginas para {alumno} en {nivel}. Basado en: {notas}. Con firmas."
        res = llamar_ia(prompt)
        st.markdown(res)
        st.download_button("📥 Descargar (Word)", generar_word_limpio(f"REFLEXIÓN - {alumno}", res, datos_id, True), f"Reflexion_{alumno}.docx")

elif opcion == "📊 Evaluación Trimestral":
    st.header("📊 Evaluación Trimestral")
    alumno_ev = st.text_input("Alumno:")
    resumen = st.text_area("Notas del trimestre:")
    if st.button("📈 Generar Evaluación"):
        prompt = f"Genera texto evaluatorio trimestral para {alumno_ev} nivel {nivel} por campos formativos. Basado en: {resumen}. Con firmas."
        res = llamar_ia(prompt)
        st.markdown(res)
        st.download_button("📥 Descargar (Word)", generar_word_limpio(f"EVALUACIÓN - {alumno_ev}", res, datos_id, True), f"Evaluacion_{alumno_ev}.docx")
