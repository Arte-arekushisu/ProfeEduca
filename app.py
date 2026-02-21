import streamlit as st
import random
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="ProfeEduca V0.5", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .stButton>button {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(248, 250, 252, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: #38bdf8;
        color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DEL GENERADOR PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PLANEACIÓN PEDAGÓGICA - MODELO DE DIÁLOGO', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

def crear_planeacion_pdf(d):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # OBJETIVO GENERAL
    pdf.chapter_title("I. OBJETIVO GENERAL")
    pdf.set_font('Arial', '', 10)
    objetivo_texto = (
        f"Esta planeación integral para el nivel {d['nivel']} busca que los alumnos desarrollen "
        f"aprendizajes profundos sobre '{d['tema']}'. A través del diálogo tutorado y estaciones "
        "de trabajo, los estudiantes adquirirán habilidades de investigación científica y pensamiento "
        "crítico. El proceso fomenta la autonomía, permitiendo que cada niño construya su conocimiento "
        "mediante el desafío y la exploración de su entorno inmediato. "
        "Se prioriza la vinculación comunitaria y el uso de materiales locales para garantizar que "
        "lo aprendido sea significativo y aplicable a su realidad cotidiana."
    )
    pdf.multi_cell(0, 5, objetivo_texto)
    pdf.ln(5)

    # DATOS GENERALES
    pdf.chapter_title("II. DATOS DE IDENTIFICACIÓN")
    pdf.set_font('Arial', '', 10)
    info = [
        f"Educador: {d['nombre_ed']}", f"ECA: {d['nombre_eca']}",
        f"Grado: {d['grado']}", f"Comunidad: {d['comunidad']}",
        f"Fecha: {d['fecha']}", f"Rincón: {d['rincon']}"
    ]
    for line in info:
        pdf.cell(0, 6, line, 0, 1)
    pdf.ln(5)

    # RUTINA DE INICIO
    pdf.chapter_title("III. MOMENTO DE INICIO (PEDAGOGÍA DE BIENVENIDA)")
    pdf.cell(0, 6, "1. Pase de lista (5 min): Mencionar una característica del tema.", 0, 1)
    pdf.cell(0, 6, "2. Regalo de lectura (10 min): Texto narrativo sobre el entorno.", 0, 1)
    pdf.cell(0, 6, "3. Actividad de bienvenida (10 min): Juego rítmico grupal.", 0, 1)
    pdf.ln(5)

    # ESTACIONES
    pdf.chapter_title("IV. ESTACIONES DE APRENDIZAJE (45 min c/u)")
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(60, 7, "Estación 1: Lenguaje", 1)
    pdf.cell(60, 7, "Estación 2: Saberes", 1)
    pdf.cell(60, 7, "Estación 3: Ética", 1, 1)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 6, "Actividades diarias rotativas con materiales reciclados (cartón, envases, hojas secas).")
    pdf.ln(5)

    # TUTOREO IA
    pdf.chapter_title(f"V. TUTOREO UNO A UNO: {d['tema'].upper()}")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Preguntas Detonantes (Generadas por IA):", 0, 1)
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(0, 5, f"1. ¿Cómo influye {d['tema']} en lo que hacemos en el pueblo?\n2. ¿Qué pasaría si {d['tema']} desapareciera de un día para otro?")
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Actividades de Tutoreo sugeridas:", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, "A. Experimentación con elementos del rincón.\nB. Diálogo reflexivo y registro en el cuaderno de campo.")
    pdf.ln(5)

    # POST-RECESO
    pdf.chapter_title("VI. ACTIVIDADES POST-RECESO")
    pdf.cell(0, 6, f"1. Materia 1: {d['materia1']} (45 min) - Dinámicas de aula.", 0, 1)
    pdf.cell(0, 6, f"2. Materia 2: {d['materia2']} (45 min) - Incluye Educación Física.", 0, 1)
    pdf.ln(5)

    # REFERENCIAS
    pdf.chapter_title("VII. REFERENCIAS BIBLIOGRÁFICAS")
    pdf.set_font('Arial', 'I', 8)
    pdf.multi_cell(0, 4, "UNESCO (2021). Reimaginar nuestros futuros juntos.\nSEP (2022). Plan de Estudio para la educación preescolar, primaria y secundaria.\nMateriales del entorno y saberes comunitarios.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. INTERFAZ DE USUARIO ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"

col_menu, col_main = st.columns([1, 2.5])

with col_menu:
    st.title("🍎 Menú")
    if st.button("🏠 Inicio", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"

with col_main:
    if st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                nivel = st.selectbox("Nivel educativo", ["Preescolar", "Primaria", "Secundaria"])
                grado = st.text_input("Grado del grupo", placeholder="Ej. 1°, 2° y 3° Multigrado")
                nombre_ed = st.text_input("Nombre del educador")
                nombre_eca = st.text_input("Nombre del ECA")
            with col2:
                comunidad = st.text_input("Comunidad")
                fecha = st.date_input("Fecha de planeación")
                tema = st.text_input("Tema de interés", placeholder="Ej. Las mariposas")
                rincon = st.text_input("Rincón (Opcional)")
            
            st.subheader("Post-Receso")
            m1 = st.text_input("Materia 1", value="Educación Física")
            m2 = st.text_input("Materia 2", placeholder="Ej. Artes")

        if st.button("🚀 GENERAR PLANEACIÓN EN PDF", use_container_width=True):
            datos = {
                "nivel": nivel, "grado": grado, "nombre_ed": nombre_ed,
                "nombre_eca": nombre_eca, "comunidad": comunidad,
                "fecha": str(fecha), "tema": tema, "rincon": rincon,
                "materia1": m1, "materia2": m2
            }
            if not tema or not nombre_ed:
                st.error("Por favor completa los campos principales (Nombre y Tema).")
            else:
                pdf_bytes = crear_planeacion_pdf(datos)
                st.download_button(
                    label="📥 Descargar PDF Listo",
                    data=pdf_bytes,
                    file_name=f"Planeacion_{tema}.pdf",
                    mime="application/pdf"
                )
                st.success("¡Generado en menos de 10 segundos! 🚀")
