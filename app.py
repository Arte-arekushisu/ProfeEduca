import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Escritos", layout="wide", page_icon="👤")

def clean(txt):
    if not txt: return ""
    # Quita acentos y normaliza texto para FPDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'replace').decode('latin-1')

class RegistroPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, "ESCRITO REFLEXIVO: SEGUIMIENTO DEL ALUMNO", 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, com, alumno, niv, gra, fec, periodo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        w, h = 95, 8
        self.cell(w, h, f" EDUCADOR: {ec}", 1, 0, 'L', True)
        self.cell(w, h, f" COMUNIDAD: {com}", 1, 1, 'L', True)
        self.cell(w, h, f" ALUMNO: {alumno}", 1, 0, 'L', True)
        self.cell(w, h, f" TRIMESTRE: {periodo}", 1, 1, 'L', True)
        self.cell(w, h, f" NIVEL: {niv}", 1, 0, 'L', True)
        self.cell(w, h, f" GRADO: {gra} | FECHA: {fec}", 1, 1, 'L', True)
        self.ln(10)

# --- INTERFAZ ---
st.title("👤 Registro de Reflexión Individual")

c1, c2, c3 = st.columns(3)
with c1:
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Alumno")
with c2:
    comunidad = st.text_input("Comunidad", "CRUZ")
    fecha_reg = st.date_input("Fecha", datetime.date.today())
with c3:
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    trimestre = st.selectbox("Trimestre", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    grados_op = ["1", "2", "3", "4", "5", "6", "Multigrado"]
    grado_edu = st.selectbox("Grado", grados_op)

st.divider()
col_a, col_b = st.columns(2)
que_hizo = col_a.text_area("¿Qué hizo hoy?", height=200)
como_hizo = col_b.text_area("¿Cómo fue su desempeño?", height=200)

if st.button("📝 GUARDAR Y GENERAR PDF", use_container_width=True):
    if not nombre_alumno or not que_hizo:
        st.error("⚠️ Datos incompletos.")
    else:
        try:
            pdf = RegistroPDF()
            pdf.add_page()
            
            # Encabezado de datos
            pdf.tabla_datos(
                clean(nombre_ec), clean(comunidad), clean(nombre_alumno), 
                clean(nivel_edu), clean(grado_edu), str(fecha_reg), clean(trimestre)
            )
            
            # Bloque 1
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, " 1. ACTIVIDADES REALIZADAS", 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 6, clean(que_hizo))
            pdf.ln(5)

            # Bloque 2
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, " 2. PROCESO Y DESEMPEÑO", 0, 1, 'L', True)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'I', 11)
            pdf.multi_cell(0, 6, clean(como_hizo))

            # Generar salida
            pdf_out = pdf.output()
            st.download_button(
                label="📥 DESCARGAR PDF", 
                data=bytes(pdf_out), 
                file_name=f"Reflexion_{nombre_alumno}.pdf", 
                mime="application/pdf"
            )
            st.success("¡PDF listo!")
            
        except Exception as e:
            st.error(f"Error técnico: {e}")
