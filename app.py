import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from google import genai

# --- CONFIGURACIÓN DE IA ---
# Axel, asegúrate de que esta clave no tenga espacios al final
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# Usamos la configuración más simple posible
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

st.set_page_config(page_title="PROFEEDUCA IA", layout="wide")
st.title("🛡️ PROFEEDUCA: Sistema de Planeación")

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
            # CAMBIO CLAVE: Usamos gemini-1.5-flash-8b que es más ligero y estable
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=f"Como experto pedagogo de CONAFE México, genera una planeación para {nivel} sobre {tema}. Comunidad: {comunidad}."
            )
            
            if response.text:
                pdf = PlaneacionPDF()
                pdf.add_page()
                pdf.set_font('Helvetica', 'B', 12)
                pdf.cell(0, 10, clean(f"Tema: {tema}"), 1, 1, 'C')
                pdf.ln(5)
                pdf.set_font('Helvetica', '', 11)
                pdf.multi_cell(0, 6, clean(response.text))

                pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
                st.success("✅ ¡Felicidades! Planeación generada.")
                st.download_button("📥 DESCARGAR PDF", pdf_out, f"Planeacion_{tema}.pdf", "application/pdf")
            else:
                st.error("La IA no respondió. Intenta de nuevo.")

        except Exception as e:
            # Si vuelve a salir 404, limpiaremos el caché del navegador
            st.error(f"Error técnico: {e}")
            st.info("Axel, si el error 404 persiste, presiona Ctrl+F5 en tu teclado para limpiar la memoria del navegador.")
