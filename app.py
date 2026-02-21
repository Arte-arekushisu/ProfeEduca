import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN DE IA ---
# Tu clave real integrada
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
genai.configure(api_key=API_KEY)

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION PROFEEDUCA - FINAL', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PROFEEDUCA IA", layout="wide")
st.title("🛡️ PROFEEDUCA: Planeación Profesional")

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

    st.subheader("🗓️ Actividades Post-Receso (60/60 min)")
    mats_inputs = {}
    cols = st.columns(5)
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for i, col in enumerate(cols):
        mats_inputs[dias[i]] = col.text_area(f"{dias[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN ÚNICA")

if submit:
    with st.spinner("🤖 La IA está redactando contenido pedagógico..."):
        try:
            # CORRECCIÓN CLAVE: Especificar el modelo sin prefijos de versión manual
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Como experto pedagogo CONAFE, genera una planeación para {nivel} sobre {tema} en {comunidad}.
            Incluye Marco Teórico (10 renglones), Pase de lista con 'Hipótesis rápida', 
            Regalo de lectura y procedimientos detallados para Lenguajes, Saberes y Ética.
            """
            
            response = model.generate_content(prompt)
            texto_ia = response.text
            
            pdf = PlaneacionPDF()
            pdf.add_page()
            
            pdf.barra("I. DATOS GENERALES")
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Tema: {tema}"), 0, 1)

            pdf.ln(5); pdf.barra("II. DESARROLLO PEDAGÓGICO IA")
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, clean(texto_ia))

            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
            st.success("✅ ¡Planeación generada con éxito!")
            st.download_button("📥 Descargar PDF", pdf_bytes, f"Planeacion_{tema}.pdf", "application/pdf")
            
        except Exception as e:
            # Si el error 404 persiste, daremos una instrucción clara de reinicio
            st.error(f"Nota: Si ves un error 404, por favor haz clic en 'Reboot App' en el menú de Streamlit.")
            st.error(f"Detalle del error: {e}")
