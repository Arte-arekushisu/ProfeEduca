import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from google import genai  # Usando la librería que ya se instaló exitosamente

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
client = genai.Client(api_key=API_KEY)

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PROFEEDUCA - PLANEACION CONAFE', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PROFEEDUCA IA", layout="wide")
st.title("🛡️ PROFEEDUCA: Sistema Inteligente")

# Formulario optimizado
with st.form("MainForm"):
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
    with col2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha", datetime.date.today())

    st.subheader("🗓️ Actividades de la Jornada")
    materias = st.text_area("Materias/Temas", "Matematicas, Español")
    
    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN AHORA")

if submit:
    with st.spinner("🤖 Generando contenido con Gemini 1.5 Flash..."):
        try:
            # Nueva forma de generar contenido (Librería google-genai)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Como experto pedagogo de CONAFE México, genera una planeación para {nivel} sobre {tema}. Comunidad: {comunidad}. Incluye actividades para: {materias}."
            )
            
            # Crear PDF
            pdf = PlaneacionPDF()
            pdf.add_page()
            pdf.barra("I. DATOS GENERALES")
            pdf.set_font('Helvetica', '', 11)
            pdf.cell(0, 8, clean(f"Educador: {educador} | Nivel: {nivel}"), 0, 1)
            pdf.cell(0, 8, clean(f"Tema: {tema} | Comunidad: {comunidad}"), 0, 1)
            
            pdf.ln(5)
            pdf.barra("II. DESARROLLO PEDAGÓGICO")
            # Acceso correcto al texto en la nueva librería
            texto_generado = response.text
            pdf.multi_cell(0, 6, clean(texto_generado))

            pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
            st.success("✅ ¡Planeación generada exitosamente!")
            st.download_button("📥 DESCARGAR MI PDF", pdf_output, f"Planeacion_{tema}.pdf", "application/pdf")
            
        except Exception as e:
            st.error(f"Error al conectar con la IA. Detalles: {e}")
            st.info("Asegúrate de que el archivo 'requirements.txt' contenga solo: streamlit, fpdf2, Pillow, google-genai")
