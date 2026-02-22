import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Planeación Semanal", layout="wide", page_icon="📝")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        # Encabezado institucional
        self.set_fill_color(128, 0, 0) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('PLANEACION SEMANAL'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, eca, comunidad, fecha):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        
        # Anchos de columna
        w = 95
        h = 8
        
        # Fila 1
        self.cell(w, h, clean(f" NOMBRE EC: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" NOMBRE ECA: {eca}"), 1, 1, 'L', True)
        
        # Fila 2
        self.cell(w, h, clean(f" COMUNIDAD: {comunidad}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" FECHA/SEMANA: {fecha}"), 1, 1, 'L', True)
        self.ln(5)

    def seccion_dia(self, titulo):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(128, 0, 0)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f" {clean(titulo)}", 0, 1, 'L', True)
        self.ln(2)

# --- INTERFAZ ---
st.title("🛡️ PROFEEDUCA: Planeación Semanal")

with st.form("Formulario_Final"):
    st.subheader("📋 Información General")
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha_semana = st.date_input("Semana del:", datetime.date.today())

    st.divider()
    st.subheader("🍎 Jornada Post-Receso")
    
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    datos_semana = {}

    for dia in dias:
        with st.expander(f"📅 {dia.upper()}", expanded=(dia == "Lunes")):
            col1, col2 = st.columns(2)
            with col1:
                m1 = st.text_input(f"Materia 1 - {dia}", key=f"m1_{dia}")
                p1 = st.text_area(f"Actividades Materia 1", key=f"p1_{dia}", height=80)
            with col2:
                m2 = st.text_input(f"Materia 2 - {dia}", key=f"m2_{dia}")
                p2 = st.text_area(f"Actividades Materia 2", key=f"p2_{dia}", height=80)
            datos_semana[dia] = {"m1": m1, "p1": p1, "m2": m2, "p2": p2}
    
    submit = st.form_submit_button("🔨 PLANEACIONES ABCD")

if submit:
    # --- VISUALIZACIÓN ---
    st.markdown("### 👁️ Vista Previa del Documento")
    
    # --- GENERACIÓN PDF ---
    pdf = PlaneacionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Tabla de datos estructurada
    pdf.tabla_datos(nombre_ec, nombre_eca, comunidad, str(fecha_semana))

    for dia, info in datos_semana.items():
        if info['m1'] or info['m2']:
            pdf.seccion_dia(dia.upper())
            
            # Materia 1
            pdf.set_text_color(0,0,0)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 6, clean(f"Materia: {info['m1']}"), 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 5, clean(info['p1']))
            pdf.ln(2)
            
            # Materia 2
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 6, clean(f"Materia: {info['m2']}"), 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 5, clean(info['p2']))
            pdf.ln(5)
    
    pdf_output = pdf.output(dest='S')
    pdf_bytes = bytes(pdf_output) if not isinstance(pdf_output, str) else pdf_output.encode('latin-1')

    st.success("✅ Estructura generada correctamente.")
    st.download_button(
        label="📥 DESCARGAR PLANEACIÓN SEMANAL (PDF)",
        data=pdf_bytes,
        file_name=f"Planeacion_Semanal_{comunidad}.pdf",
        mime="application/pdf"
    )    
