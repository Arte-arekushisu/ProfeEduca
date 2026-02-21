import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import google.generativeai as genai  # Necesitas instalar: pip install google-generativeai

# --- CONFIGURACIÓN DE IA ---
# Reemplaza 'TU_API_KEY_AQUI' con tu clave de Google AI Studio
genai.configure(api_key="TU_API_KEY_AQUI")
model = genai.GenerativeModel('gemini-pro')

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION IA", layout="wide")
st.title("🛡️ Generador de Planeación con Inteligencia Artificial")

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

    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN ÚNICA CON IA")

if submit:
    with st.spinner("🤖 La IA está investigando y redactando tu planeación..."):
        # PROMPT PARA LA IA
        prompt = f"""
        Actúa como un experto pedagogo del modelo CONAFE México. 
        Genera una planeación para el nivel {nivel} sobre el tema {tema} en la comunidad {comunidad}.
        Incluye:
        1. Un marco teórico científico de 10 renglones.
        2. Un pase de lista creativo sobre el tema.
        3. Un regalo de lectura y bienvenida.
        4. Tres estaciones de trabajo (Lenguajes, Saberes, Ética) con procedimientos paso a paso.
        Responde en formato de lista clara.
        """
        
        try:
            response = model.generate_content(prompt)
            texto_ia = response.text
            
            # Generar PDF
            pdf = PlaneacionPDF()
            pdf.add_page()
            
            pdf.barra("I. DATOS GENERALES")
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Grado: {grado}"), 0, 1)
            pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | Tema: {tema}"), 0, 1)

            pdf.ln(5); pdf.barra("II. CONTENIDO GENERADO POR IA")
            pdf.set_font('Helvetica', '', 10)
            # Limpiamos el texto de la IA para que el PDF no falle con caracteres especiales
            pdf.multi_cell(0, 6, clean(texto_ia))

            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
            
            st.success("✅ ¡Planeación única creada!")
            st.download_button("📥 Descargar PDF con IA", pdf_bytes, f"Planeacion_IA_{tema}.pdf", "application/pdf")
            
        except Exception as e:
            st.error(f"Error al conectar con la IA: {e}")
