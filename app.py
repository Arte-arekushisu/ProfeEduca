import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="PROFEEDUCA - Gestión CONAFE", layout="wide", page_icon="🛡️")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_fill_color(200, 30, 30) # Rojo institucional
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PROFEEDUCA: SISTEMA DE PLANEACION', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, 'Herramienta de Apoyo para el Educador Comunitario (CONAFE)', 0, 1, 'C')
        self.ln(15)

    def seccion(self, titulo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(3)

# --- PANEL DE CONTROL ---
st.title("🛡️ PROFEEDUCA: Centro de Gestión Pedagógica")
st.info("Modo: Plantilla de Estructuración (Listo para migración a servidor privado)")

with st.expander("📝 DATOS DE IDENTIFICACIÓN", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha de Aplicación")
    with c3:
        tema = st.text_input("Tema Central", "LAS TORTUGAS MARINAS")
        microregion = st.text_input("Microregión", "CIENCIAS")

# --- CUERPO DE LA PLANEACIÓN ---
st.subheader("🚀 Desarrollo de la Jornada")
actividades = st.text_area("Descripción de Actividades (Lo que antes hacía la IA, ahora lo estructuramos aquí):", 
                          placeholder="Escribe aquí los desafíos, actividades de inicio, desarrollo y cierre...")

objetivos = st.text_area("Objetivos de Aprendizaje:")

if st.button("📄 GENERAR DOCUMENTO OFICIAL"):
    if not actividades:
        st.warning("Por favor, describe las actividades para generar el reporte.")
    else:
        pdf = PlaneacionPDF()
        pdf.add_page()
        
        pdf.seccion("I. DATOS GENERALES")
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 7, clean(f"Nivel: {nivel} | Educador: {educador}"), 0, 1)
        pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | Fecha: {fecha}"), 0, 1)
        pdf.cell(0, 7, clean(f"Tema: {tema}"), 0, 1)
        
        pdf.ln(5)
        pdf.seccion("II. OBJETIVOS")
        pdf.multi_cell(0, 6, clean(objetivos))
        
        pdf.ln(5)
        pdf.seccion("III. DESARROLLO PEDAGÓGICO")
        pdf.multi_cell(0, 6, clean(actividades))
        
        pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
        st.success("✅ Formato generado correctamente.")
        st.download_button("📥 DESCARGAR PLANEACIÓN (PDF)", pdf_output, f"Planeacion_{tema}.pdf", "application/pdf")

# --- ESPACIO RESERVADO PARA IA ---
st.divider()
st.caption("⚙️ Módulo de IA Gemini: Deshabilitado temporalmente para migración a servidor privado.")
