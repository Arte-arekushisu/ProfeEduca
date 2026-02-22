import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Planeación Semanal ABCD", layout="wide", page_icon="📝")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0) 
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'CONAFE - MODELO ABCD (PLANEACION SEMANAL)', 0, 1, 'C')
        self.ln(10)

    def seccion(self, titulo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f" {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

# --- INTERFAZ ---
st.title("🛡️ PROFEEDUCA: Gestión Semanal ABCD")

with st.form("Formulario_ABCD_Semanal"):
    st.subheader("📋 Datos de Identificación")
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC (Educador Comunitario)", "AXEL REYES")
        nombre_eca = st.text_input("Nombre del ECA (Enlace de Cultura)")
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha_inicio = st.date_input("Semana del (Lunes):", datetime.date.today())

    st.divider()
    st.subheader("🍎 Planeación Post-Receso (Lunes a Viernes)")
    
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    datos_semana = {}

    for dia in dias:
        exp = st.expander(f"📅 {dia}", expanded=(dia == "Lunes"))
        col_t, col_p = exp.columns([1, 2])
        with col_t:
            tema = st.text_input(f"Temas/Materias - {dia}", key=f"t_{dia}")
        with col_p:
            plan = st.text_area(f"Actividades Post-Receso - {dia}", key=f"p_{dia}", height=100)
        datos_semana[dia] = {"tema": tema, "plan": plan}
    
    submit = st.form_submit_button("🔨 PLANEACIONES ABCD")

# --- VISUALIZACIÓN Y PDF ---
if submit:
    # 1. Visualización en pantalla
    st.success("### 👁️ Vista Previa de la Semana")
    st.write(f"**EC:** {nombre_ec} | **ECA:** {nombre_eca} | **Comunidad:** {comunidad}")
    
    for dia, contenido in datos_semana.items():
        if contenido['tema']:
            with st.container():
                st.markdown(f"**{dia}** - *{contenido['tema']}*")
                st.write(contenido['plan'])
                st.markdown("---")

    # 2. Generación de PDF
    pdf = PlaneacionPDF()
    pdf.add_page()
    
    pdf.seccion("DATOS DE IDENTIFICACION")
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, clean(f"EC: {nombre_ec}"), 0, 1)
    pdf.cell(0, 7, clean(f"ECA: {nombre_eca}"), 0, 1)
    pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | Semana del: {fecha_inicio}"), 0, 1)
    pdf.ln(5)

    for dia, contenido in datos_semana.items():
        if contenido['tema'] or contenido['plan']:
            pdf.seccion(f"JORNADA: {dia.upper()}")
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, clean(f"Materias: {contenido['tema']}"), 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, clean(contenido['plan']))
            pdf.ln(4)
    
    pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
    
    st.download_button(
        label="📥 DESCARGAR PLANEACIÓN SEMANAL (PDF)",
        data=pdf_out,
        file_name=f"Planeacion_Semanal_ABCD_{fecha_inicio}.pdf",
        mime="application/pdf"
    )
