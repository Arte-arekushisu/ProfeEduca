import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from groq import Groq

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Registro IA Alumno", layout="wide", page_icon="✍️")

# Estilo Visual Oscuro (Tu diseño original)
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

# Clave de API de Groq
GROQ_KEY = "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"

def llamar_ia_redaccion(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Como experto en el modelo pedagógico ABCD, redacta un texto reflexivo formal y coherente para el expediente del alumno.
        ALUMNO: {datos['alumno']}
        LOGROS: {datos['logros']}
        RETOS: {datos['dificultades']}
        SENTIMIENTOS: {datos['emociones']}
        COMPROMISO: {datos['compromiso']}
        
        Redacta un solo cuerpo de texto profesional, fluido y en tercera persona. No uses asteriscos (*).
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return "Error al conectar con la IA. Se usará el texto manual."

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
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REGISTRO SOCIAL Y TEXTO REFLEXIVO INDIVIDUAL'), 0, 1, 'C')
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
st.markdown('<h1 style="color:#38bdf8;">📝 Registro de Reflexión por Alumno con IA</h1>', unsafe_allow_html=True)

with st.form("Form_Reflexivo"):
    col1, col2 = st.columns(2)
    with col1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Nombre completo del estudiante")
        comunidad = st.text_input("Comunidad", "PARAJES")
    with col2:
        fecha = st.date_input("Día del registro", datetime.date.today())
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])

    st.divider()
    
    # Entradas de datos para la IA
    logros = st.text_area("🚀 ¿Qué logró aprender hoy el alumno?", height=70)
    dificultades = st.text_area("⚠️ ¿Qué retos enfrentó y cómo los superó?", height=70)
    emociones = st.text_area("🌈 Registro Social: ¿Cómo se sintió durante la jornada?", height=70)
    compromiso = st.text_area("🤝 Compromiso del alumno para la siguiente sesión", height=70)

    submit = st.form_submit_button("🔨 GENERAR REFLEXIÓN CON IA")

if submit:
    if not nombre_alumno:
        st.error("Por favor, ingresa el nombre del alumno.")
    else:
        with st.spinner("La IA está redactando el registro pedagógico..."):
            info_ia = {
                "alumno": nombre_alumno, "logros": logros, 
                "dificultades": dificultades, "emociones": emociones, 
                "compromiso": compromiso
            }
            texto_redactado = llamar_ia_redaccion(info_ia)
            
            # Mostrar vista previa
            st.markdown("### 📄 Análisis Redactado por IA")
            st.info(texto_redactado)
            
            # Generar PDF
            pdf = ReflexivoPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, nombre_alumno.upper(), comunidad, str(fecha), nivel)
            
            # Título de sección en PDF
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 10, clean("RELATO REFLEXIVO DE LA JORNADA"), 0, 1, 'L', True)
            pdf.ln(3)
            
            # Cuerpo del texto redactado por IA
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 7, clean(texto_redactado))
            
            pdf_output = pdf.output(dest='S')
            st.success(f"✅ Registro de {nombre_alumno} generado correctamente.")
            st.download_button(
                label="📥 DESCARGAR PDF REFLEXIVO",
                data=bytes(pdf_output),
                file_name=f"Reflexion_IA_{nombre_alumno}_{fecha}.pdf",
                mime="application/pdf"
            )
