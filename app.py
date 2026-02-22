import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Planeación CONAFE", layout="wide", page_icon="📝")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0) # Rojo oscuro institucional
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'CONAFE - MODELO ABCD', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 5, 'Sistema de Estructuracion Pedagógica', 0, 1, 'C')
        self.ln(10)

    def seccion(self, titulo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f" {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

# --- INTERFAZ ---
st.title("🛡️ PROFEEDUCA: Gestión de Planeación")

with st.form("Formulario_ABCD"):
    st.subheader("📋 Datos de Identificación")
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC (Educador Comunitario)", "AXEL REYES")
        nombre_eca = st.text_input("Nombre del ECA (Enlace de Cultura)")
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha de la Jornada", datetime.date.today())

    st.divider()
    
    st.subheader("🍎 Actividades Post-Receso")
    temas_post = st.text_area("Temas o materias post-receso:", placeholder="Ej: Matematicas, Lectura, Artes...")
    detalles_post = st.text_area("Descripción de la planeación post-receso:", height=150)
    
    # Botón con el nombre solicitado
    submit = st.form_submit_button("🔨 PLANEACIONES ABCD")

# --- PROCESAMIENTO Y VISUALIZACIÓN ---
if submit:
    if not temas_post or not detalles_post:
        st.error("Por favor, completa los temas y la descripción del post-receso.")
    else:
        # 1. Visualización previa en la app
        st.success("### 👁️ Vista Previa de la Planeación")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**EC:** {nombre_ec}")
            st.write(f"**ECA:** {nombre_eca}")
        with col_b:
            st.write(f"**Comunidad:** {comunidad}")
            st.write(f"**Fecha:** {fecha}")
        
        st.info(f"**Materias Post-Receso:** {temas_post}")
        st.write(detalles_post)

        # 2. Generación de PDF
        pdf = PlaneacionPDF()
        pdf.add_page()
        
        pdf.seccion("DATOS GENERALES")
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 7, clean(f"EC: {nombre_ec}"), 0, 1)
        pdf.cell(0, 7, clean(f"ECA: {nombre_eca}"), 0, 1)
        pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | Fecha: {fecha}"), 0, 1)
        
        pdf.ln(5)
        pdf.seccion("CONTENIDO POST-RECESO")
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, clean(f"Materias/Temas: {temas_post}"), 0, 1)
        pdf.ln(2)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 6, clean(detalles_post))
        
        pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
        
        st.divider()
        st.download_button(
            label="📥 DESCARGAR PDF OFICIAL",
            data=pdf_out,
            file_name=f"Planeacion_ABCD_{fecha}.pdf",
            mime="application/pdf"
        )
