import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE IA (CONEXIÓN ESTABLE 2026) ---
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# Forzamos la configuración a la versión estable 'v1'
genai.configure(api_key=API_KEY, transport='rest')

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

st.set_page_config(page_title="PROFEEDUCA IA", layout="wide")
st.title("🛡️ PROFEEDUCA: Sistema de Planeación")

# Tu formulario que ya funciona perfectamente
with st.form("MainForm"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha", datetime.date.today())
        materias = st.text_area("Materias/Temas", "Matematicas, Español")
    
    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN AHORA")

if submit:
    with st.spinner("🤖 Generando contenido pedagógico..."):
        try:
            # Seleccionamos el modelo flash en su ruta estable
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generamos el contenido
            response = model.generate_content(
                f"Genera una planeación pedagógica para {nivel} sobre {tema}. Comunidad: {comunidad}."
            )
            
            if response:
                pdf = PlaneacionPDF()
                pdf.add_page()
                pdf.set_font('Helvetica', 'B', 12)
                pdf.cell(0, 10, clean(f"TEMA: {tema}"), 1, 1, 'C')
                pdf.ln(5)
                pdf.set_font('Helvetica', '', 11)
                pdf.multi_cell(0, 6, clean(response.text))

                pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
                st.success("✅ ¡Éxito! Tu planeación ha sido creada.")
                st.download_button("📥 DESCARGAR MI PDF", pdf_out, f"Planeacion_{tema}.pdf", "application/pdf")

        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Axel, intenta recargar la página (F5) si el error persiste.")
