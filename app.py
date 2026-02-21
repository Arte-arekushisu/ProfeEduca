import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN DE IA ---
# REEMPLAZA ESTO CON TU LLAVE REAL DE GOOGLE AI STUDIO
API_KEY = "TU_API_KEY_AQUI" 

if API_KEY != "TU_API_KEY_AQUI":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

def clean(txt):
    if not txt: return ""
    # Normalización para evitar errores de caracteres en el PDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, 'Contenido Pedagogico Extenso y Detallado', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION PRO IA", layout="wide")
st.title("🛡️ Generador de Planeación Profesional (Fase 4 - IA)")

if API_KEY == "TU_API_KEY_AQUI":
    st.warning("⚠️ Falta configurar la API KEY de Google. Por favor, añádela en el código fuente.")

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

    st.subheader("🗓️ Materias Post-Receso (60 min / 60 min)")
    mats_inputs = {}
    cols = st.columns(5)
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for i, col in enumerate(cols):
        mats_inputs[dias[i]] = col.text_area(f"{dias[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN ÚNICA CON IA")

if submit:
    if API_KEY == "TU_API_KEY_AQUI":
        st.error("No se puede generar la planeación sin una API KEY válida.")
    else:
        with st.spinner("🤖 La IA está investigando y redactando..."):
            prompt = f"""
            Como experto pedagogo CONAFE, genera una planeación extensa para {nivel} sobre {tema} en {comunidad}.
            Estructura obligatoria:
            1. MARCO TEÓRICO: 10 renglones científicos y educativos sobre {tema}.
            2. RUTINAS: Un pase de lista con 'Hipótesis rápida', un regalo de lectura y una bienvenida 'Debate express'.
            3. ESTACIONES DE TRABAJO: Procedimientos detallados paso a paso para Lenguajes, Saberes y Ética.
            Responde de forma profesional.
            """
            
            try:
                response = model.generate_content(prompt)
                texto_ia = response.text
                
                pdf = PlaneacionPDF()
                pdf.add_page()
                
                pdf.barra("I. DATOS DE IDENTIFICACION")
                pdf.set_font('Helvetica', '', 10)
                pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel/Grado: {nivel}/{grado}"), 0, 1)
                pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | Tema: {tema} | Rincon: {rincon}"), 0, 1)

                pdf.ln(5); pdf.barra("II. DESARROLLO PEDAGÓGICO CON IA")
                pdf.set_font('Helvetica', '', 10)
                pdf.multi_cell(0, 6, clean(texto_ia))

                pdf.add_page(); pdf.barra("III. BLOQUE POST-RECESO (DIVISION 60 MIN / 60 MIN)")
                for dia, m_text in mats_inputs.items():
                    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"DIA: {dia}"), 1, 1, 'C', True)
                    mats = m_text.split('\n')
                    for idx, m in enumerate(mats):
                        if m.strip():
                            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean(f"HORA {idx+1}: {m}"), "LR", 1)
                            pdf.set_font('Helvetica', '', 9)
                            pdf.multi_cell(0, 5, clean("Actividad tecnica: Inicio, Desarrollo y Cierre vinculados al tema."), "LBR")
                    pdf.ln(3)

                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
                st.success("✅ ¡Planeación consolidada con éxito!")
                st.download_button("📥 Descargar Planeación Final", pdf_bytes, f"Planeacion_{tema}.pdf", "application/pdf")
                
            except Exception as e:
                st.error(f"Error al conectar con la IA: {e}")
