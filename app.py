import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Configuración de Estilo
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; font-weight: bold; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Función para Generar Tabla Profesional en Word
def generar_word_tabla(titulo, contenido_ia, d):
    doc = Document()
    
    # Encabezado General
    h = doc.add_heading(titulo, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    header_table = doc.add_table(rows=3, cols=2)
    header_table.style = 'Table Grid'
    header_table.cell(0, 0).text = f"Comunidad: {d['comunidad']}"
    header_table.cell(0, 1).text = f"Fecha: {d['fecha']}"
    header_table.cell(1, 0).text = f"Educador: {d['nombre']}"
    header_table.cell(1, 1).text = f"Nivel: {d['nivel']}"
    header_table.cell(2, 0).text = f"ECA: {d['eca']}"

    doc.add_paragraph("\n")

    # Tabla de Actividades
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Actividad / Momento'
    hdr_cells[1].text = 'Desarrollo Sugerido'
    hdr_cells[2].text = 'Materiales'
    hdr_cells[3].text = 'Tiempo'

    # Procesar filas enviadas por la IA
    lineas = contenido_ia.replace("**", "").split('\n')
    for linea in lineas:
        if '|' in linea:
            partes = linea.split('|')
            if len(partes) >= 4:
                row_cells = table.add_row().cells
                for i in range(4):
                    row_cells[i].text = partes[i].strip()

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Sidebar y Datos
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    comunidad = st.text_input("Comunidad", "PARAJES DEL VALLE")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    eca = st.text_input("ECA", "MOISES ROSAS")
    nivel = st.selectbox("Nivel:", ["Secundaria Multigrado", "Primaria Multigrado", "Preescolar"])
    fecha_hoy = st.date_input("Fecha")

datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel, "fecha": str(fecha_hoy)}

def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- SECCIONES ---
if opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación Semanal: {nivel}")
    tema = st.text_input("Tema de la Unidad (UAA):")
    rincón = st.text_input("Rincón Permanente:")
    
    if st.button("🚀 Generar Tabla de Planeación con Temas de Inicio"):
        prompt = f"""Actúa como experto CONAFE. Genera la planeación de Lunes a Viernes para {tema}.
        Usa el formato de tabla separando columnas con '|'. NO USES ASTERISCOS.
        
        IMPORTANTE: Para cada día, los primeros 3 registros de la tabla DEBEN ser:
        1. Bienvenida | Propon una dinámica lúdica específica | Ninguno o materiales simples | 10 min
        2. Pase de Lista | Propon una temática creativa para el pase de lista | Lista de asistencia | 5 min
        3. Regalo de Lectura | Propon un título de cuento o texto y cómo leerlo | Libro o lectura sugerida | 15 min
        
        Luego continua con: Estación de trabajo en {rincón}, Relación Tutora y Cierre.
        Al final agrega enlaces de YouTube y Google para que el educador estudie sobre {tema}."""
        
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        st.download_button("📥 Descargar Word con Tabla", generar_word_tabla("PLANEACIÓN SEMANAL", resultado, datos_id), "Planeacion.docx")
