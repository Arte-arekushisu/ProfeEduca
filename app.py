import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Estilo Dark y Configuración
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

# 2. Función de Exportación a Word (Corregida)
def generar_word(titulo, contenido, d):
    doc = Document()
    h = doc.add_heading(titulo, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Encabezado profesional
    table = doc.add_table(rows=3, cols=2)
    table.cell(0, 0).text = f"Comunidad: {d['comunidad']}"
    table.cell(0, 1).text = f"Fecha: {d['fecha']}"
    table.cell(1, 0).text = f"Educador: {d['nombre']}"
    table.cell(1, 1).text = f"Nivel: {d['nivel']}"
    table.cell(2, 0).text = f"ECA: {d['eca']}"
    
    doc.add_paragraph("\n" + "="*50 + "\n")
    para = doc.add_paragraph(contenido)
    para.alignment = WD_ALIGN_PARAGRAPH.BOTH
    
    # Espacio para firmas
    doc.add_paragraph("\n\n\n")
    f_table = doc.add_table(rows=1, cols=2)
    f_table.cell(0, 0).text = "__________________________\nFirma del Educador"
    f_table.cell(0, 1).text = "__________________________\nFirma Padre/APEC"
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Menú y Datos (Línea 72 corregida aquí)
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    st.divider()
    comunidad = st.text_input("Comunidad", "PARAJES DEL VALLE")
    nombre_ec = st.text_input("Educador Comunitario", "AXEL REYES")
    eca = st.text_input("ECA", "MOISES ROSAS")
    nivel = st.selectbox("Nivel:", ["Secundaria Multigrado", "Primaria Multigrado", "Preescolar", "Primaria 1-6", "Secundaria 1-3"])
    fecha_hoy = st.date_input("Fecha")

# ESTA ES LA LÍNEA 72 CORREGIDA
datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel, "fecha": str(fecha_hoy)}

# 4. Función de IA
def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 4096}}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- SECCIONES ---
if opcion == "🏠 Inicio":
    st.markdown("""
    <div class="welcome-box">
        <h1>¡Bienvenido a tu Espacio de Confianza! 🍎</h1>
        <p style="font-size: 1.2em;">
            Aquí tienes la seguridad de que tu labor docente está respaldada. 
            Este sistema coordina el <b>Regalo de Lectura</b>, el <b>Pase de Lista</b> y la 
            <b>Relación Tutora</b>. Confía en el proceso: estamos aquí para que tu 
            planeación sea perfecta y sin errores.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header(f"📅 Planeación: {nivel}")
    tema = st.text_input("Tema Principal de la Semana:")
    if st.button("🚀 Generar Planeación Semanal"):
        prompt = f"Genera planeación semanal ABCD nivel {nivel} para {tema}. Incluye Bienvenida, Pase de Lista, Regalo de Lectura y creación de Estaciones de Trabajo temporales en Rincones permanentes. Estructura por tiempos pedagógicos."
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        st.download_button("📥 Descargar Planeación (Word)", generar_word("PLANEACIÓN SEMANAL", resultado, datos_id), "Planeacion.docx")

elif opcion == "✍️ Reflexión Diaria":
    st.header("✍️ Texto Reflexivo Diario")
    alumno = st.text_input("Nombre del Alumno:")
    notas = st.text_area("Notas del aprendizaje observado hoy:")
    if st.button("🪄 Redactar Reflexión"):
        prompt = f"Redacta un texto reflexivo diario extenso (2.5 páginas) para {alumno} en {nivel}. Notas: {notas}. Usa lenguaje de relación tutora y Modelo ABCD."
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        st.download_button("📥 Descargar Reflexión (Word)", generar_word(f"REFLEXIÓN - {alumno}", resultado, datos_id), f"Reflexion_{alumno}.docx")

elif opcion == "📊 Evaluación Trimestral":
    st.header("📊 Evaluación Trimestral")
    alumno_ev = st.text_input("Alumno:")
    resumen = st.text_area("Notas acumuladas por campo formativo:")
    if st.button("📈 Generar Evaluación"):
        prompt = f"Genera texto reflexivo trimestral extenso para {alumno_ev} en {nivel} analizando los 4 campos formativos de CONAFE basados en: {resumen}. Incluye espacio de compromisos."
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        st.download_button("📥 Descargar Evaluación (Word)", generar_word(f"EVALUACIÓN TRIMESTRAL - {alumno_ev}", resultado, datos_id), f"Evaluacion_{alumno_ev}.docx")
