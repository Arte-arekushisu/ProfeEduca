import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN DE IA CON TU LLAVE REAL ---
API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def clean(txt):
    if not txt: return ""
    # Normalización para evitar errores de caracteres especiales en el PDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION PROFEEDUCA', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, 'Generado con Inteligencia Artificial - Modelo CONAFE', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PROFEEDUCA IA", layout="wide")
st.title("🛡️ PROFEEDUCA: Generador de Planeación Profesional")

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

    st.subheader("🗓️ Distribución Post-Receso (Materias)")
    mats_inputs = {}
    cols = st.columns(5)
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for i, col in enumerate(cols):
        mats_inputs[dias[i]] = col.text_area(f"{dias[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN ÚNICA")

if submit:
    with st.spinner("🤖 La IA de Google está redactando tu planeación pedagógica..."):
        prompt = f"""
        Actúa como un experto pedagogo del modelo CONAFE México. 
        Genera una planeación educativa para el nivel {nivel} sobre el tema '{tema}' en la comunidad de '{comunidad}'.
        
        Debes incluir:
        1. MARCO TEÓRICO: Un sustento científico detallado de 10 renglones sobre {tema}.
        2. RUTINAS DE INICIO: 
           - Pase de lista dinámico (con la actividad 'Hipótesis rápida').
           - Un Regalo de lectura adecuado al nivel {nivel}.
           - Una actividad de bienvenida creativa.
        3. ESTACIONES DE TRABAJO: Actividades paso a paso para los campos formativos de:
           - Lenguajes.
           - Saberes y Pensamiento Científico.
           - Ética, Naturaleza y Sociedades.
        
        Usa un lenguaje profesional y educativo.
        """
        
        try:
            response = model.generate_content(prompt)
            texto_ia = response.text
            
            pdf = PlaneacionPDF()
            pdf.add_page()
            
            # I. DATOS
            pdf.barra("I. DATOS GENERALES")
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Grado: {grado}"), 0, 1)
            pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | ECA: {eca} | Rincon: {rincon}"), 0, 1)

            # II. CONTENIDO IA
            pdf.ln(5); pdf.barra("II. DESARROLLO PEDAGÓGICO (GENERADO POR IA)")
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, clean(texto_ia))

            # III. JORNADA POST-RECESO
            pdf.add_page(); pdf.barra("III. ACTIVIDADES POST-RECESO")
            for dia, m_text in mats_inputs.items():
                pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"JORNADA: {dia}"), 1, 1, 'C', True)
                mats = m_text.split('\n')
                for m in mats:
                    if m.strip():
                        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean(f"Materia: {m}"), "LR", 1)
                        pdf.set_font('Helvetica', '', 9)
                        pdf.multi_cell(0, 5, clean(f"Secuencia: Inicio (Saberes previos), Desarrollo (Actividad vinculada a {tema}) y Cierre."), "LBR")
                pdf.ln(3)

            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

            st.divider()
            st.success("✅ Planeación generada con éxito.")
            st.download_button(
                label="📥 DESCARGAR PLANEACION EN PDF", 
                data=pdf_bytes, 
                file_name=f"Planeacion_{tema.replace(' ', '_')}.pdf", 
                mime="application/pdf",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")
