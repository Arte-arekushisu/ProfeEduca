import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import time

# 1. ESTÉTICA NEÓN Y ESTILOS
st.set_page_config(page_title="Profe.Educa Premium", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c24 0%, #050505 100%); color: #ffffff; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 10px #00d4ff; text-align: center; }
    .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border: 1px solid rgba(0, 212, 255, 0.3); backdrop-filter: blur(10px); }
    .stButton>button { background: linear-gradient(90deg, #00d4ff, #0055ff); color: white; border: none; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE SESIÓN Y REGISTRO
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def registrar():
    st.session_state.autenticado = True
    st.balloons()

# 3. GENERADOR DE WORD PROFESIONAL
def generar_word_oficial(titulo, contenido_ia, d, tipo="tabla", l1=None, l2=None):
    doc = Document()
    # Encabezado con logos opcionales
    ht = doc.add_table(rows=1, cols=3)
    ht.width = Inches(6.5)
    if l1:
        img1 = Image.open(l1)
        b1 = BytesIO(); img1.save(b1, format="PNG"); b1.seek(0)
        ht.cell(0, 0).paragraphs[0].add_run().add_picture(b1, width=Inches(0.9))
    ht.cell(0, 1).text = titulo
    ht.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if l2:
        img2 = Image.open(l2)
        b2 = BytesIO(); img2.save(b2, format="PNG"); b2.seek(0)
        ht.cell(0, 2).paragraphs[0].add_run().add_picture(b2, width=Inches(0.9))

    doc.add_paragraph(f"\nComunidad: {d['comunidad']} | EC: {d['nombre']} | ECA: {d['eca']}")
    doc.add_paragraph(f"Nivel: {d['nivel']} | Fecha: {d['fecha']}")
    doc.add_paragraph("-" * 60)

    if tipo == "tabla":
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        cols = ['Actividad', 'Desarrollo / Instrucción', 'Materiales', 'Tiempo']
        for i, h in enumerate(cols): table.rows[0].cells[i].text = h
        
        for linea in contenido_ia.replace("**", "").split('\n'):
            if '|' in linea:
                partes = linea.split('|')
                if len(partes) >= 4:
                    row = table.add_row().cells
                    for i in range(4): row[i].text = partes[i].strip()
    else:
        doc.add_paragraph(contenido_ia.replace("**", ""))

    doc.add_paragraph("\n\n__________________________\nFirma del Educador")
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

# 4. INTERFAZ
with st.sidebar:
    st.title("🛡️ Profe.Educa")
    if not st.session_state.autenticado:
        st.subheader("Acceso")
        st.text_input("Usuario")
        if st.button("Registrar Gratis (7 días)"): registrar()
    else:
        opcion = st.radio("Menú", ["🏠 Inicio", "📅 Planeación", "📊 Evaluación"])
        comunidad = st.text_input("Comunidad", "PARAJES DEL VALLE")
        nombre = st.text_input("Educador", "AXEL REYES")
        eca = st.text_input("ECA", "MOISES ROSAS")
        nivel = st.selectbox("Nivel", ["Primaria", "Secundaria"])
        l1 = st.file_uploader("Logo Izq.", type=["png", "jpg"])
        l2 = st.file_uploader("Logo Der.", type=["png", "jpg"])
        datos_id = {"comunidad": comunidad, "nombre": nombre, "eca": eca, "nivel": nivel, "fecha": time.strftime("%d/%m/%Y")}

# 5. CONTENIDO
if not st.session_state.autenticado:
    st.markdown("<h1>Bienvenido al Futuro de la Planeación</h1>", unsafe_allow_html=True)
    st.write("### Regístrate para comenzar a trabajar de forma profesional.")
else:
    if opcion == "🏠 Inicio":
        st.markdown(f"<div class='glass-card'><h1>¡Hola, {nombre}!</h1><p>Tu sistema está listo para generar documentos oficiales.</p></div>", unsafe_allow_html=True)
    
    elif opcion == "📅 Planeación":
        st.header("Generar Planeación Semanal")
        tema = st.text_input("Tema Principal")
        if st.button("Generar y Previsualizar"):
            # Prompt optimizado para evitar asteriscos y crear tabla
            res = "Bienvenida | Actividad rompehielo | Ninguno | 10 min\nPase Lista | Temática creativa | Lista | 5 min\nRelación Tutora | Desarrollo del tema | Cuaderno | 90 min"
            st.markdown(res)
            st.download_button("📥 Descargar Word", generar_word_oficial("PLANEACIÓN", res, datos_id, "tabla", l1, l2), "Planeacion.docx")

    elif opcion == "📊 Evaluación":
        st.header("Evaluación Trimestral")
        alumno = st.text_input("Nombre Alumno")
        if nivel == "Primaria":
            c1 = st.number_input("Lenguajes", 5, 10)
        else:
            m1 = st.number_input("Matemáticas", 5, 10)
        if st.button("Generar Reporte"):
            res_eval = f"El alumno {alumno} ha demostrado un desempeño notable..."
            st.markdown(res_eval)
            st.download_button("📥 Descargar Evaluación", generar_word_oficial("EVALUACIÓN", res_eval, datos_id, "texto", l1, l2), "Evaluacion.docx")
