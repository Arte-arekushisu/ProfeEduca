import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from groq import Groq

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Reflexión con IA", layout="wide", page_icon="🤖")

# Estilo Visual Oscuro
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1e293b 0%, #020617 100%); 
        color: #f8fafc; 
    }
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: #0f172a;
        color: #38bdf8;
        border: 1px solid #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

GROQ_KEY = "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"

def llamar_ia_reflexion(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Eres un experto pedagogo del modelo ABCD. Redacta un texto reflexivo formal y detallado para el expediente del alumno.
        ALUMNO: {datos['alumno']}
        LOGROS: {datos['logros']}
        DIFICULTADES: {datos['dificultades']}
        EMOCIONES: {datos['emociones']}
        COMPROMISO: {datos['compromiso']}
        
        Redacta en tercera persona, de forma profesional, sin usar asteriscos (*). 
        El texto debe integrar estos puntos en un relato coherente de la jornada escolar.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return "No se pudo generar el texto automático. Se usará la información manual."

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexivoPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 15, clean('REGISTRO REFLEXIVO INDIVIDUAL IA'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, alumno, comunidad, fecha, nivel):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 249, 255)
        self.cell(95, 8, clean(f" EC: {ec}"), 1, 0, 'L', True)
        self.cell(95, 8, clean(f" ALUMNO: {alumno}"), 1, 1, 'L', True)
        self.cell(63, 8, clean(f" COMUNIDAD: {comunidad}"), 1, 0, 'L', True)
        self.cell(63, 8, clean(f" FECHA: {fecha}"), 1, 0, 'L', True)
        self.cell(64, 8, clean(f" NIVEL: {nivel}"), 1, 1, 'L', True)
        self.ln(8)

# --- INTERFAZ ---
st.markdown('<h1 style="color:#38bdf8;">🤖 Generador de Reflexiones ABCD</h1>', unsafe_allow_html=True)

with st.form("Form_IA_Reflexivo"):
    col1, col2 = st.columns(2)
    with col1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno")
    with col2:
        comunidad = st.text_input("Comunidad", "PARAJES")
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])
    
    fecha = st.date_input("Fecha", datetime.date.today())
    
    st.subheader("Puntos clave del día (La IA los redactará por ti)")
    logros = st.text_area("¿Qué aprendió?")
    dificultades = st.text_area("¿Qué se le complicó?")
    emociones = st.text_area("¿Cómo se sintió?")
    compromiso = st.text_area("Compromiso")

    submit = st.form_submit_button("🚀 GENERAR REFLEXIÓN CON IA")

if submit:
    if not nombre_alumno:
        st.error("Falta el nombre del alumno.")
    else:
        with st.spinner("La IA está redactando el informe pedagógico..."):
            datos = {
                "alumno": nombre_alumno, "logros": logros, 
                "dificultades: ": dificultades, "emociones": emociones, 
                "compromiso": compromiso
            }
            texto_ia = llamar_ia_reflexion(datos)
            
            st.markdown("### Vista Previa de la Redacción:")
            st.info(texto_ia)
            
            pdf = ReflexivoPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, nombre_alumno.upper(), comunidad, str(fecha), nivel)
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, clean("ANÁLISIS PEDAGÓGICO Y SOCIAL"), 0, 1)
            pdf.ln(2)
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 6, clean(texto_ia))
            
            pdf_bytes = pdf.output(dest='S')
            st.download_button(
                label="📥 DESCARGAR PDF REFLEXIVO",
                data=bytes(pdf_bytes),
                file_name=f"Reflexion_IA_{nombre_alumno}.pdf",
                mime="application/pdf"
            )
