import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Planeación Semanal ABCD", layout="wide", page_icon="📝")

def clean(txt):
    if not txt: return ""
    # Normalizamos el texto para evitar errores de símbolos extraños en el PDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        # Encabezado estilo CONAFE
        self.set_fill_color(128, 0, 0) 
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, clean('CONAFE - MODELO ABCD (PLANEACION SEMANAL)'), 0, 1, 'C')
        self.ln(10)

    def seccion(self, titulo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f" {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

# --- INTERFAZ DE USUARIO ---
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
    st.subheader("🍎 Planeación Post-Receso (2 Materias por Día)")
    
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    datos_semana = {}

    for dia in dias:
        with st.expander(f"📅 {dia.upper()}", expanded=(dia == "Lunes")):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Materia 1**")
                m1 = st.text_input(f"Nombre Materia 1", key=f"m1_{dia}", placeholder="Ej. Matemáticas")
                p1 = st.text_area(f"Actividades Materia 1", key=f"p1_{dia}", height=100)
            with col2:
                st.markdown("**Materia 2**")
                m2 = st.text_input(f"Nombre Materia 2", key=f"m2_{dia}", placeholder="Ej. Lenguaje")
                p2 = st.text_area(f"Actividades Materia 2", key=f"p2_{dia}", height=100)
            datos_semana[dia] = {"m1": m1, "p1": p1, "m2": m2, "p2": p2}
    
    submit = st.form_submit_button("🔨 PLANEACIONES ABCD")

# --- PROCESAMIENTO ---
if submit:
    # 1. Visualización en la Web
    st.markdown("### 👁️ Vista Previa de la Planeación Semanal")
    st.info(f"**Semana:** {fecha_inicio} | **Comunidad:** {comunidad} | **EC:** {nombre_ec}")
    
    for dia, info in datos_semana.items():
        if info['m1'] or info['m2']:
            with st.container():
                st.subheader(f"🗓️ {dia}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Materia 1:** {info['m1']}")
                    st.write(info['p1'])
                with col_b:
                    st.write(f"**Materia 2:** {info['m2']}")
                    st.write(info['p2'])
                st.markdown("---")

    # 2. Generación del PDF (Corregido)
    try:
        pdf = PlaneacionPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        pdf.seccion("DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 6, clean(f"EC: {nombre_ec} | ECA: {nombre_eca}"), 0, 1)
        pdf.cell(0, 6, clean(f"Comunidad: {comunidad} | Semana: {fecha_inicio}"), 0, 1)
        pdf.ln(5)

        for dia, info in datos_semana.items():
            if info['m1'] or info['m2']:
                pdf.seccion(f"JORNADA: {dia.upper()}")
                # Materia 1
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(0, 6, clean(f"Materia 1: {info['m1']}"), 0, 1)
                pdf.set_font('Helvetica', '', 10)
                pdf.multi_cell(0, 5, clean(info['p1']))
                pdf.ln(2)
                # Materia 2
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(0, 6, clean(f"Materia 2: {info['m2']}"), 0, 1)
                pdf.set_font('Helvetica', '', 10)
                pdf.multi_cell(0, 5, clean(info['p2']))
                pdf.ln(5)
        
        # Generar el stream del PDF de forma segura
        pdf_data = pdf.output(dest='S')
        # Si es un bytearray o similar, nos aseguramos de pasarlo a bytes
        if isinstance(pdf_data, str):
            pdf_bytes = pdf_data.encode('latin-1')
        else:
            pdf_bytes = bytes(pdf_data)

        st.download_button(
            label="📥 DESCARGAR PLANEACION ABCD (PDF)",
            data=pdf_bytes,
            file_name=f"Planeacion_Semanal_{fecha_inicio}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Hubo un error al generar el PDF: {e}")
