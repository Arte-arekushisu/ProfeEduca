import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import time

# 1. ESTILO AVANZADO Y EFECTOS VISUALES
st.set_page_config(page_title="Profe.Educa Premium", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c24 0%, #050505 100%); color: #ffffff; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 10px #00d4ff; text-align: center; font-family: 'Arial Black'; }
    .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(0, 212, 255, 0.3); backdrop-filter: blur(10px); margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #00d4ff, #0055ff); color: white; border-radius: 8px; font-weight: bold; width: 100%; box-shadow: 0 4px 15px rgba(0, 85, 255, 0.4); border: none; height: 3em; }
    .stDownloadButton>button { background: linear-gradient(90deg, #22c55e, #16a34a) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE REGISTRO Y SESIÓN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# 3. FUNCIÓN DE GENERACIÓN DE WORD (TABLA ESTRUCTURADA)
def generar_word_oficial(titulo, contenido_ia, d, tipo="tabla", l1=None, l2=None):
    doc = Document()
    # Encabezado con Logos
    section = doc.sections[0]
    header_table = doc.add_table(rows=1, cols=3)
    header_table.width = Inches(6.5)
    
    if l1:
        img1 = Image.open(l1)
        b1 = BytesIO(); img1.save(b1, format="PNG"); b1.seek(0)
        header_table.cell(0, 0).paragraphs[0].add_run().add_picture(b1, width=Inches(0.9))
    
    header_table.cell(0, 1).text = titulo
    header_table.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    if l2:
        img2 = Image.open(l2)
        b2 = BytesIO(); img2.save(b2, format="PNG"); b2.seek(0)
        header_table.cell(0, 2).paragraphs[0].add_run().add_picture(b2, width=Inches(0.9))

    doc.add_paragraph(f"\nComunidad: {d['comunidad']} | Educador: {d['nombre']} | ECA: {d['eca']}")
    doc.add_paragraph(f"Nivel: {d['nivel']} | Fecha: {d['fecha']}")
    doc.add_paragraph("-" * 80)

    if tipo == "tabla":
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdrs = table.rows[0].cells
        for i, txt in enumerate(['Actividad', 'Desarrollo / Explicación', 'Materiales', 'Tiempo']):
            hdrs[i].text = txt
            hdrs[i].paragraphs[0].runs[0].bold = True
        
        # Procesar líneas de la IA (divididas por '|')
        lineas = contenido_ia.replace("**", "").split('\n')
        for linea in lineas:
            if '|' in linea:
                partes = linea.split('|')
                if len(partes) >= 4:
                    row = table.add_row().cells
                    for i in range(4): row[i].text = partes[i].strip()
    else:
        para = doc.add_paragraph(contenido_ia.replace("**", ""))
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Sección de Firmas
    doc.add_paragraph("\n\n\n")
    f_table = doc.add_table(rows=1, cols=2)
    f_table.cell(0, 0).text = "__________________________\nFirma del Educador"
    f_table.cell(0, 1).text = "__________________________\nFirma del Padre/APEC"

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 4. FUNCIÓN IA
def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except: return "Error al generar contenido. Revisa tu conexión."

# 5. INTERFAZ Y NAVEGACIÓN
with st.sidebar:
    st.title("🛡️ Profe.Educa v.21")
    if not st.session_state.autenticado:
        st.subheader("🔑 Registro")
        user = st.text_input("Usuario (Email)")
        plan = st.selectbox("Plan", ["7 Días Gratis", "Mensual ($699)", "Anual ($6,400)"])
        if st.button("Activar Mi Cuenta"):
            st.session_state.autenticado = True
            st.balloons()
            st.rerun()
    else:
        opcion = st.radio("Menú", ["🏠 Inicio", "📅 Planeación", "✍️ Reflexión", "📊 Evaluación"])
        st.divider()
        com = st.text_input("Comunidad", "PARAJES DEL VALLE")
        ed = st.text_input("Educador", "AXEL REYES")
        ec_n = st.text_input("ECA", "MOISES ROSAS")
        niv = st.selectbox("Nivel", ["Primaria", "Secundaria"])
        l_izq = st.file_uploader("Logo Ofic. 1", type=["jpg", "png"])
        l_der = st.file_uploader("Logo Ofic. 2", type=["jpg", "png"])
        datos = {"comunidad": com, "nombre": ed, "eca": ec_n, "nivel": niv, "fecha": time.strftime("%d/%m/%Y")}

# 6. SECCIONES DE LA APP
if not st.session_state.autenticado:
    st.markdown("<h1>Transforma tu Práctica Educativa</h1>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/vector-gratis/fondo-educacion-dibujado-mano_23-2149450917.jpg")
    st.write("### Registrate para acceder a planeaciones, reflexiones y evaluaciones oficiales.")

elif opcion == "🏠 Inicio":
    st.markdown(f"<div class='glass-card'><h1>¡Bienvenido, Profe {ed}!</h1><p style='text-align:center;'>Tu plataforma está lista. Genera documentos con validez oficial en segundos.</p></div>", unsafe_allow_html=True)

elif opcion == "📅 Planeación":
    st.header("
