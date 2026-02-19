import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Estilo y Configuración
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

# 2. Función para Generar el Word con Tabla Estructurada
def generar_word_tabla(titulo, contenido_ia, d):
    doc = Document()
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

    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Momento / Actividad'
    hdr_cells[1].text = 'Desarrollo y Explicación'
    hdr_cells[2].text = 'Materiales'
    hdr_cells[3].text = 'Tiempo'

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
    fecha_hoy = st.date_input("Fecha de Inicio")

datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel, "fecha": str(fecha_hoy)}

def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- SECCIÓN PLANEACIÓN ---
if opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación de Jornada Completa: {nivel}")
    col1, col2 = st.columns(2)
    with col1:
        tema_interes = st.text_input("Tema Principal (UAA):")
        materias_extra = st.text_input("Materias post-receso:", placeholder="Ej. Matemáticas (Fracciones) y Ciencias")
    with col2:
        rincón = st.text_input("Rincón Permanente:")
        objetivo = st.text_area("Objetivo de la Semana:")

    if st.button("🚀 Generar Planeación Estructurada"):
        prompt = f"""Actúa como experto pedagogo CONAFE. Genera la planeación de Lunes a Viernes para {nivel}.
        Tema UAA: {tema_interes} | Materias post-receso: {materias_extra} | Rincón: {rincón}.
        Usa el formato de tabla con '|'. NO USES ASTERISCOS.
        
        ESTRUCTURA DIARIA OBLIGATORIA:
        1. BIENVENIDA | Propon dinámica lúdica específica | Varios | 10 min
        2. PASE DE LISTA | Propon temática creativa diaria | Lista | 5 min
        3. REGALO DE LECTURA | Título de texto y estrategia de mediación | Libro | 15 min
        4. RELACIÓN TUTORA | Desarrollo en el rincón {rincón} con una estación de trabajo sobre {tema_interes} | Material rincón | 90 min
        5. RECESO | Tiempo de alimentación y juego libre | Alimentos | 30 min
        6. BLOQUE ASIGNATURAS | Desarrolla temas y ACTIVIDADES PRÁCTICAS de {materias_extra}. Si es matemáticas, incluye ejemplos de ejercicios | Cuadernos, pizarrón | 90 min
        7. PUESTA EN COMÚN | Reflexión de lo aprendido | Cuaderno | 20 min
        
        Al final agrega 'Caja de Herramientas' con enlaces para el educador."""
        
        resultado = llamar_ia(prompt)
        st.markdown(resultado)
        st.download_button("📥 Descargar Planeación (Word)", generar_word_tabla("PLANEACIÓN SEMANAL", resultado, datos_id), "Planeacion.docx")
