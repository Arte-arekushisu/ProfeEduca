import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Fase 6", layout="wide", page_icon="👤")

def clean(txt):
    if not txt: return ""
    # Normalizar para eliminar acentos y caracteres especiales no compatibles con latin-1
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt

class RegistroPDF(FPDF):
    def header(self):
        # Encabezado institucional
        self.set_fill_color(128, 0, 0)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('ESCRITO REFLEXIVO: SEGUIMIENTO DEL ALUMNO'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, com, alumno, niv, gra, fec):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        w, h = 95, 8
        # Datos en tabla organizada
        self.cell(w, h, clean(f" EDUCADOR: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {com}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" ALUMNO: {alumno}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" FECHA: {fec}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" NIVEL: {niv}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO: {gra}"), 1, 1, 'L', True)
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
    grados_op = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel_edu == "Primaria" else ["1", "2", "3", "Multigrado"]
    grado_edu = st.selectbox("Grado", grados_op)

st.divider()

# Captura Manual Descriptiva
st.subheader("📝 Descripción del Desempeño")
col_a, col_b = st.columns(2)
with col_a:
    que_hizo = st.text_area("¿Qué hizo el alumno hoy?", height=250)
with col_b:
    como_hizo = st.text_area("¿Cómo realizó las actividades?", height=250)

# --- PROCESAMIENTO ---
if st.button("📝 GUARDAR Y GENERAR ESCRITO REFLEXIVO", use_container_width=True):
    if not nombre_alumno or not que_hizo:
        st.error("⚠️ Falta el nombre del alumno o la descripción.")
    else:
        try:
            pdf = RegistroPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, str(fecha_registro))

            # Bloque 1
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, clean(" 1. ACTIVIDADES REALIZADAS"), 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 6, clean(que_hizo))
            pdf.ln(10)

            # Bloque 2
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, clean(" 2. PROCESO Y DESEMPEÑO"), 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'I', 11)
            pdf.multi_cell(0, 6, clean(como_hizo))

            # SOLUCIÓN AL ERROR DE ATRIBUTO:
            # En fpdf2, output() devuelve bytes si no se especifica nombre de archivo.
            pdf_output = pdf.output() 
            
            st.success(f"✅ Registro de {nombre_alumno} listo.")
            st.download_button(
                label="📥 DESCARGAR ESCRITO REFLEXIVO",
                data=pdf_output,
                file_name=f"Reflexion_{nombre_alumno}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar el PDF: {e}")
