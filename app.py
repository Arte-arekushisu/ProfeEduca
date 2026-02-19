import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Configuración de Estilo Dark
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

# 2. Función para Generar el Archivo Word (Imprimible)
def generar_word(titulo, contenido, datos_id):
    doc = Document()
    # Encabezado
    h = doc.add_heading(titulo, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Datos de Identificación
    table = doc.add_table(rows=3, cols=2)
    table.cell(0, 0).text = f"Comunidad: {datos_id['comunidad']}"
    table.cell(0, 1).text = f"Fecha: {datos_id['fecha']}"
    table.cell(1, 0).text = f"Educador: {datos_id['nombre']}"
    table.cell(1, 1).text = f"Nivel: {datos_id['nivel']}"
    table.cell(2, 0).text = f"ECA: {datos_id['eca']}"
    
    doc.add_paragraph("\n" + "="*50 + "\n")
    
    # Contenido
    para = doc.add_paragraph(contenido)
    para.alignment = WD_ALIGN_PARAGRAPH.BOTH
    
    # Espacio para firmas
    doc.add_paragraph("\n\n\n")
    firmas = doc.add_table(rows=1, cols=2)
    firmas.cell(0, 0).text = "__________________________\nFirma del Educador"
    firmas.cell(0, 1).text = "__________________________\nFirma Padre/APEC"
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Sidebar y Navegación
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Texto Reflexivo Diario", "📊 Evaluación Trimestral"])
    st.divider()
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    nivel = st.selectbox("Nivel:", ["Preescolar 1-3", "Primaria 1-6", "Primaria Multigrado", "Secundaria 1-3", "Secundaria Multigrado"])
    fecha_hoy = st.date_input("Fecha")

datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel, "
