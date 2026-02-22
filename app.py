import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Seguimiento Alumno", layout="wide", page_icon="📝")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class SeguimientoPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('ESCRITO REFLEXIVO: SEGUIMIENTO DIARIO'), 0, 1, 'C')
        self.ln(5)

    def tabla_identificacion(self, ec, eca, com, alumno, niv, gra):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(245, 245, 245)
        w, h = 95, 7
        self.cell(w, h, clean(f" NOMBRE DEL EC: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" NOMBRE DEL ECA: {eca}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {com}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" ALUMNO: {alumno}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" NIVEL: {niv}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO: {gra}"), 1, 1, 'L', True)
        self.ln(10)

# --- INTERFAZ LATERAL ---
with st.sidebar:
    st.header("📌 Datos de Identificación")
    nombre_ec = st.text_input("Nombre EC", "AXEL REYES")
    nombre_eca = st.text_input("Nombre ECA")
    comunidad = st.text_input("Comunidad", "CRUZ")
    nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Ej. Juan Pérez")
    nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grados = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel == "Primaria" else ["1", "2", "3", "Multigrado"]
    grado = st.selectbox("Grado", grados)

# --- CUERPO PRINCIPAL ---
st.title("📔 Bitácora de Reflexión Diaria")
st.info(f"Registrando avance para: **{nombre_alumno if nombre_alumno else 'Alumno no especificado'}**")

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
registros = {}

for dia in dias:
    with st.expander(f"📅 REGISTRO DEL {dia.upper()}", expanded=(dia == "Lunes")):
        col1, col2 = st.columns(2)
        with col1:
            que_hizo = st.text_area(f"¿Qué actividades realizó el alumno?", key=f"que_{dia}", height=150, placeholder="Describe los temas o ejercicios trabajados...")
        with col2:
            como_hizo = st.text_area(f"¿Cómo realizó las actividades?", key=f"como_{dia}", height=150, placeholder="Describe su desempeño de forma sencilla (ej. con ayuda, rápido, se le dificultó...)")
        registros[dia] = {"que": que_hizo, "como": como_hizo}

# --- GENERACIÓN DEL PDF ---
st.divider()
if st.button("📝 GENERAR ESCRITO REFLEXIVO DIARIO", use_container_width=True):
    if not nombre_alumno:
        st.warning("⚠️ Por favor, escribe el nombre del alumno en la barra lateral.")
    else:
        pdf = SeguimientoPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        pdf.tabla_identificacion(nombre_ec, nombre_eca, comunidad, nombre_alumno, nivel, grado)

        for dia, contenido in registros.items():
            if contenido['que'].strip() or contenido['como'].strip():
                # Título del día
                pdf.set_font('Helvetica', 'B', 11)
                pdf.set_fill_color(128, 0, 0)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 8, clean(f" JORNADA: {dia.upper()}"), 0, 1, 'L', True)
                
                # Sección ¿Qué hizo?
                pdf.ln(2)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(0, 6, clean("¿Qué hizo el alumno?"), 0, 1)
                pdf.set_font('Helvetica', '', 10)
                pdf.multi_cell(0, 5, clean(contenido['que']))
                
                # Sección ¿Cómo lo hizo?
                pdf.ln(2)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(0, 6, clean("¿Cómo realizó las actividades? (Descripción sencilla)"), 0, 1)
                pdf.set_font('Helvetica', 'I', 10)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 5, clean(contenido['como']))
                pdf.ln(5)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.success(f"✅ Bitácora de {nombre_alumno} lista para descargar.")
        st.download_button(
            label="📥 DESCARGAR ESCRITO REFLEXIVO",
            data=pdf_bytes,
            file_name=f"Reflexion_{nombre_alumno}_{comunidad}.pdf",
            mime="application/pdf"
        )
