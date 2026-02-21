import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from google import genai

# --- CONFIGURACIÓN DE IA (SOLUCIÓN ERROR 404) ---
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# Creamos el cliente asegurando que use la API estable
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
st.title("🛡️ PROFEEDUCA: Sistema de Planeación 2026")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "Multigrado")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "Proyecto Raices")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interes", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincon", "CIENCIAS")

    st.subheader("🗓️ Actividades Post-Receso")
    mats_inputs = {}
    cols = st.columns(5)
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for i, col in enumerate(cols):
        mats_inputs[dias[i]] = col.text_area(f"{dias[i]}", "Matematicas", height=80)

    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN AHORA")

if submit:
    with st.spinner("🤖 Generando contenido pedagógico..."):
        try:
            # Forzamos el uso de gemini-1.5-flash de forma directa
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Como experto pedagogo CONAFE, genera una planeación técnica para {nivel} sobre {tema}. Incluye Marco Teórico, Rutinas de inicio y Estaciones de trabajo."
            )
            
            pdf = PlaneacionPDF()
            pdf.add_page()
            pdf.barra("I. DATOS GENERALES")
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel}"), 0, 1)
            pdf.cell(0, 7, clean(f"Tema: {tema} | Comunidad: {comunidad}"), 0, 1)

            pdf.ln(5); pdf.barra("II. DESARROLLO DE LA IA")
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, clean(response.text))

            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
            st.success("✅ ¡Felicidades! La planeación se ha creado correctamente.")
            st.download_button("📥 DESCARGAR MI PDF", pdf_bytes, f"Planeacion_{tema}.pdf", "application/pdf")
            
        except Exception as e:
            st.error("⚠️ El sistema detectó un conflicto de versión en el servidor.")
            st.info("Para solucionar esto, ve a 'Manage App' -> 'Reboot App'. Es necesario para limpiar la memoria vieja.")
            st.error(f"Detalle: {e}")
