import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import time

# 1. ESTILO AVANZADO Y ANIMACIONES (CSS)
st.set_page_config(page_title="Profe.Educa Premium", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    /* Fondo con gradiente y efecto de partículas */
    .stApp {
        background: radial-gradient(circle, #1a1c24 0%, #050505 100%);
        color: #ffffff;
    }
    /* Animación para el título */
    @keyframes neon {
        0% { text-shadow: 0 0 10px #00d4ff; }
        50% { text-shadow: 0 0 20px #0055ff, 0 0 30px #00d4ff; }
        100% { text-shadow: 0 0 10px #00d4ff; }
    }
    h1 { animation: neon 2s infinite; color: #00d4ff !important; text-align: center; }
    
    /* Cajas interactivas */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 25px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .glass-card:hover { transform: scale(1.02); border-color: #00d4ff; }
    
    /* Botones Pro */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        color: white; border: none; border-radius: 8px;
        height: 3em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 15px rgba(0, 85, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGICA DE SESIÓN (REGISTRO)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def registrar_usuario():
    st.session_state.autenticado = True
    st.balloons()
    st.success("¡Cuenta activada! Tienes 7 días de prueba gratis.")

# 3. FUNCIONES DE WORD (Estructura de Cuadro)
def generar_documento(titulo, contenido_ia, d, tipo="tabla", l1=None, l2=None):
    doc = Document()
    # Encabezado con logos
    header = doc.add_table(rows=1, cols=3)
    header.width = Inches(6)
    if l1: header.cell(0, 0).paragraphs[0].add_run().add_picture(l1, width=Inches(0.8))
    header.cell(0, 1).text = titulo
    header.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if l2: header.cell(0, 2).paragraphs[0].add_run().add_picture(l2, width=Inches(0.8))

    doc.add_paragraph(f"\nComunidad: {d['comunidad']} | Educador: {d['nombre']} | ECA: {d['eca']}")
    doc.add_paragraph(f"Nivel: {d['nivel']} | Fecha: {d['fecha']}")
    doc.add_paragraph("-" * 50)

    if tipo == "tabla":
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        cols = ['Actividad', 'Desarrollo / Introducción', 'Materiales', 'Tiempo']
        for i, nombre in enumerate(cols): table.rows[0].cells[i].text = nombre
        
        lineas = contenido_ia.replace("**", "").split('\n')
        for linea in lineas:
            if '|' in linea:
                partes = linea.split('|')
                if len(partes) >= 4:
                    row = table.add_row().cells
                    for i in range(4): row[i].text = partes[i].strip()
    else:
        p = doc.add_paragraph(contenido_ia.replace("**", ""))
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Firmas
    doc.add_paragraph("\n\n\n")
    f_tab = doc.add_table(rows=1, cols=2)
    f_tab.cell(0, 0).text = "__________________________\nFirma del Educador"
    f_tab.cell(0, 1).text = "__________________________\nFirma Padre/APEC"
    
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# 4. INTERFAZ PRINCIPAL
with st.sidebar:
    st.title("🛡️ Profe.Educa v.20")
    if not st.session_state.autenticado:
        st.subheader("🔑 Registro de Usuario")
        user = st.text_input("Correo Electrónico")
        pw = st.text_input("Contraseña", type="password")
        if st.button("Crear Cuenta Gratis"):
            registrar_usuario()
    else:
        st.success(f"Sesión: Activa ✅")
        opcion = st.radio("Menú Principal", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
        st.divider()
        comunidad = st.text_input("Comunidad")
        nombre_ec = st.text_input("Tu Nombre")
        eca = st.text_input("Nombre de ECA")
        nivel_edu = st.selectbox("Nivel Educativo", ["Primaria", "Secundaria"])
        l1 = st.file_uploader("Logo 1", type=["jpg","png"])
        l2 = st.file_uploader("Logo 2", type=["jpg","png"])
        datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel_edu, "fecha": time.strftime("%d/%m/%Y")}

# 5. DESARROLLO DE SECCIONES
if not st.session_state.autenticado:
    st.markdown("<h1>Profe.Educa: Tu Aliado Pedagógico</h1>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/vector-gratis/ilustracion-concepto-educacion-maestro_114360-7815.jpg", width=400)
    st.write("### Por favor, regístrate en el panel izquierdo para comenzar tu semana gratis.")

elif opcion == "🏠 Inicio":
    st.markdown(f"<div class='glass-card'><h1>¡Hola, Profe {nombre_ec}!</h1><p style='text-align:center;'>Recuerda: Tu impacto en la comunidad trasciende el aula. Genera hoy tu planeación limpia y profesional.</p></div>", unsafe_allow_html=True)
    st.write("### ¿Qué necesitas hacer hoy?")
    c1, c2 = st.columns(2)
    with c1: st.info("📅 Planeación Semanal: Tablas ordenadas con horarios."); st.info("✍️ Reflexión Diaria: Seguimiento por alumno.")
    with c2: st.info("📊 Evaluación: Reportes oficiales por campo formativo."); st.info("🆘 Soporte 24/7 para plan Anual.")

elif opcion == "📅 Planeación Semanal":
    st.header("🗓️ Estructura de Planeación Semanal")
    tema = st.text_input("Tema de Interés Principal (UAA)")
    rincón = st.text_input("Rincón Permanente")
    materias = st.text_input("Materias Adicionales (Ej: Español, Matemáticas)")
    
    if st.button("🚀 Generar Planeación"):
        prompt = f"Genera planeación CONAFE para {nivel_edu}. Tema: {tema}. Rincón: {rincón}. Agrega {materias} después del receso. Formato tabla con '|'. Incluye Bienvenida, Pase de Lista y Regalo de Lectura con actividades."
        # Llamar IA (simulado aquí, usa tu función llamar_ia)
        res = "Bienvenida | Juego de sillas | Música | 10 min\nPase de Lista | Menciona tu color | Lista | 5 min\nRegalo Lectura | El Principito | Libro | 20 min\nRelación Tutora | Trabajo en estación | Fichas | 90 min"
        st.markdown(res)
        st.download_button("📥 Descargar Word Profesional", generar_documento("PLANEACIÓN SEMANAL", res, datos_id, "tabla", l1, l2), "Planeacion.docx")

elif opcion == "📊 Evaluación Trimestral":
    st.header("📊 Evaluación Oficial Trimestral")
    alumno = st.text_input("Nombre del Alumno")
    proyecto = st.text_input("Nombre
