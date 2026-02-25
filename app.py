import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Texto Reflexivo Individual", layout="wide", page_icon="✍️")

# Estilo Visual Oscuro
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1e293b 0%, #020617 100%); 
        color: #f8fafc; 
    }
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: #0f172a;
        color: #38bdf8;
        border: 1px solid #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexivoPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REGISTRO SOCIAL Y TEXTO REFLEXIVO INDIVIDUAL'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, alumno, comunidad, fecha, nivel):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 249, 255)
        # Fila 1: EC y Alumno
        self.cell(95, 8, clean(f" EC: {ec}"), 1, 0, 'L', True)
        self.cell(95, 8, clean(f" ALUMNO: {alumno}"), 1, 1, 'L', True)
        # Fila 2: Comunidad, Fecha y Nivel
        self.cell(63, 8, clean(f" COMUNIDAD: {comunidad}"), 1, 0, 'L', True)
        self.cell(63, 8, clean(f" FECHA: {fecha}"), 1, 0, 'L', True)
        self.cell(64, 8, clean(f" NIVEL: {nivel}"), 1, 1, 'L', True)
        self.ln(5)

# --- INTERFAZ ---
st.markdown('<h1 style="color:#38bdf8;">📝 Registro de Reflexión por Alumno</h1>', unsafe_allow_html=True)

with st.form("Form_Reflexivo"):
    col1, col2 = st.columns(2)
    with col1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Escribe el nombre completo")
        comunidad = st.text_input("Comunidad", "PARAJES")
    with col2:
        fecha = st.date_input("Día del registro", datetime.date.today())
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])

    st.divider()
    
    # Secciones del Texto Reflexivo
    logros = st.text_area("🚀 ¿Qué logró aprender hoy el alumno?", height=100)
    dificultades = st.text_area("⚠️ ¿Qué retos enfrentó y cómo los superó?", height=100)
    emociones = st.text_area("🌈 Registro Social: ¿Cómo se sintió durante la jornada?", height=100)
    compromiso = st.text_area("🤝 Compromiso del alumno para la siguiente sesión", height=80)

    submit = st.form_submit_button("🔨 GENERAR REGISTRO INDIVIDUAL")

if submit:
    if not nombre_alumno:
        st.error("Por favor, ingresa el nombre del alumno.")
    else:
        pdf = ReflexivoPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, nombre_alumno.upper(), comunidad, str(fecha), nivel)
        
        secciones = {
            "APRENDIZAJES Y LOGROS": logros,
            "RETOS Y DIFICULTADES": dificultades,
            "ESTADO SOCIOEMOCIONAL (REGISTRO SOCIAL)": emociones,
            "COMPROMISOS": compromiso
        }

        for titulo, contenido in secciones.items():
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 8, clean(titulo), 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 6, clean(contenido))
            pdf.ln(5)

        pdf_output = pdf.output(dest='S')
        st.success(f"✅ Registro de {nombre_alumno} generado.")
        st.download_button(
            label="📥 DESCARGAR PDF",
            data=bytes(pdf_output),
            file_name=f"Reflexion_{nombre_alumno}_{fecha}.pdf",
            mime="application/pdf"
        )
