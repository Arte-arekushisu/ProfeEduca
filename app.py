import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Registro de Reflexión", layout="wide", page_icon="👤")

def clean(txt):
    if not txt: return ""
    # Eliminamos acentos para evitar errores de codificación en el PDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt

class RegistroPDF(FPDF):
    def header(self):
        # Franja institucional roja
        self.set_fill_color(128, 0, 0)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('ESCRITO REFLEXIVO: SEGUIMIENTO DEL ALUMNO'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, com, alumno, niv, gra, fec, periodo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        w, h = 95, 8
        # Tabla de identificación con Trimestre
        self.cell(w, h, clean(f" EDUCADOR: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {com}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" ALUMNO: {alumno}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" TRIMESTRE: {periodo}"), 1, 1, 'L', True) # Campo nuevo
        self.cell(w, h, clean(f" NIVEL: {niv}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO: {gra}"), 1, 0, 'L', True)
        self.cell(95, h, clean(f" FECHA: {fec}"), 1, 1, 'L', True)
        self.ln(10)

# --- INTERFAZ ---
st.title("👤 Registro de Reflexión Individual")

# Datos de Identificación
c1, c2, c3 = st.columns(3)
with c1:
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno")
with c2:
    comunidad = st.text_input("Comunidad", "CRUZ")
    fecha_registro = st.date_input("Fecha de Registro", datetime.date.today())
with c3:
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    # Apartado para Trimestre
    trimestre = st.selectbox("Trimestre de Evaluación", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    
    # Lógica de grados según nivel
    grados_op = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel_edu == "Primaria" else ["1", "2", "3", "Multigrado"]
    grado_edu = st.selectbox("Grado", grados_op)

st.divider()

# Descripción Manual
st.subheader("📝 Descripción del Desempeño")
col_a, col_b = st.columns(2)
with col_a:
    que_hizo = st.text_area("¿Qué hizo el alumno hoy?", height=250, placeholder="Ej: Leer el tema de tortugas marinas...")
with col_b:
    como_hizo = st.text_area("¿Cómo realizó las actividades?", height=250, placeholder="Ej: Realizó un producto final con dibujos...")

# --- GENERACIÓN DEL PDF ---
if st.button("📝 GUARDAR Y GENERAR ESCRITO REFLEXIVO", use_container_width=True):
    if not nombre_alumno or not que_hizo:
        st.error("⚠️ Falta completar el nombre del alumno o las actividades.")
    else:
        try:
            pdf = RegistroPDF()
            pdf.add_page()
            # Se añade el parámetro 'trimestre' a la tabla
            pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, str(fecha_registro), trimestre)

            # Bloque 1: Actividades
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, clean(" 1. ACTIVIDADES REALIZADAS"), 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 6, clean(que_hizo))
            pdf.ln(10)

            # Bloque 2: Desempeño
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, clean(" 2. PROCESO Y DESEMPEÑO"), 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'I', 11)
            pdf.multi_cell(0, 6, clean(como_hizo))

            # Generación de bytes para descarga
            pdf_output = pdf.output()
