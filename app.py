import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from google import genai

# --- CONFIGURACIÓN DE IA (SOLUCIÓN FINAL 2026) ---
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# Forzamos al cliente a usar solo la versión estable
client = genai.Client(api_key=API_KEY)

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION PROFESIONAL PROFEEDUCA', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PROFEEDUCA IA", layout="wide")
st.title("🛡️ PROFEEDUCA: Sistema Pedagógico Inteligente")

with st.form("FormularioPrincipal"):
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
    with col2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha", datetime.date.today())

    st.subheader("🗓️ Actividades de la Jornada")
    mats = st.text_area("Materias (una por línea)", "Matematicas\nEspañol")
    
    boton = st.form_submit_button("🔨 GENERAR PLANEACIÓN AHORA")

if boton:
    with st.spinner("🤖 Google está redactando tu planeación..."):
        try:
            # Llamada directa al modelo más estable
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Genera una planeación educativa para {nivel} sobre {tema}. Comunidad: {comunidad}."
            )
            
            pdf = PlaneacionPDF()
            pdf.add_page()
            pdf.barra("I. DATOS GENERALES")
            pdf.set_font('Helvetica', '', 11)
            pdf.cell(0, 8, clean(f"Educador: {educador} | Tema: {tema}"), 0, 1)
            
            pdf.ln(5); pdf.barra("II. DESARROLLO PEDAGÓGICO")
            pdf.multi_cell(0, 6, clean(response.text))

            pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
            st.success("✅ ¡Lo logramos! Tu planeación está lista.")
            st.download_button("📥 DESCARGAR PDF", pdf_output, "Planeacion.pdf", "application/pdf")
            
        except Exception as e:
            st.error(f"Error de sincronización. Por favor, realiza un 'Reboot' en el panel derecho.")
