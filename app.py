import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from groq import Groq

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Reflexión Extendida", layout="wide", page_icon="✍️")

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

def llamar_ia_redaccion_extensa(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        # Prompt modificado para solicitar EXPANSIÓN y DETALLE
        prompt = f"""
        Eres un asesor pedagógico experto en el Modelo ABCD y la Nueva Escuela Mexicana. 
        Tu tarea es redactar una CRÓNICA REFLEXIVA EXTENSA Y DETALLADA (mínimo 3 párrafos largos) sobre la jornada del alumno.
        
        DATOS CLAVE:
        ALUMNO: {datos['alumno']}
        LOGROS: {datos['logros']}
        RETOS: {datos['dificultades']}
        SENTIMIENTOS: {datos['emociones']}
        COMPROMISO: {datos['compromiso']}
        
        INSTRUCCIONES DE REDACCIÓN:
        1. Usa un lenguaje pedagógico elevado pero humano.
        2. Describe cómo los logros impactan en su proceso de aprendizaje.
        3. Analiza las dificultades como áreas de oportunidad.
        4. Relaciona sus emociones con su desempeño social en la comunidad.
        5. Redacta en tercera persona y NO uses asteriscos (*).
        6. Sé MUY EXTENSO en tu explicación.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000 # Aumentado para permitir más texto
        )
        return completion.choices[0].message.content.replace("*", "")
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def clean(txt):
    if not txt: return ""
    # Normalización completa para evitar errores de PDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('—', '-').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexivoPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('INFORME PEDAGOGICO REFLEXIVO - ABCD'), 0, 1, 'C')
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
st.markdown('<h1 style="color:#38bdf8;">📝 Registro de Reflexión Individual (Modo Extenso)</h1>', unsafe_allow_html=True)

with st.form("Form_Reflexivo_Extenso"):
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno")
    with c2:
        comunidad = st.text_input("Comunidad", "PARAJES")
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])
    
    fecha = st.date_input("Día del registro", datetime.date.today())

    st.divider()
    logros = st.text_area("🚀 Logros y aprendizajes (Notas breves)")
    dificultades = st.text_area("⚠️ Retos y dificultades (Notas breves)")
    emociones = st.text_area("🌈 Registro Social/Emociones")
    compromiso = st.text_area("🤝 Compromisos")

    submit = st.form_submit_button("🚀 GENERAR REDACCIÓN EXTENSA Y PDF")

if submit:
    if not nombre_alumno:
        st.error("Por favor, escribe el nombre del alumno.")
    else:
        with st.spinner("La IA está analizando y redactando un informe detallado..."):
            info = {
                "alumno": nombre_alumno, "logros": logros, 
                "dificultades": dificultades, "emociones": emociones, 
                "compromiso": compromiso
            }
            # Llamada a la IA para el texto largo
            texto_extenso = llamar_ia_redaccion_extensa(info)
            
            st.markdown("### 📄 Vista Previa del Análisis Pedagógico")
            st.write(texto_extenso)
            
            # Generación de PDF optimizada para texto largo
            pdf = ReflexivoPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, nombre_alumno.upper(), comunidad, str(fecha), nivel)
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, clean("CRONICA Y ANALISIS DEL PROCESO DE APRENDIZAJE"), 0, 1)
            pdf.ln(2)
            
            pdf.set_font('Helvetica', '', 11)
            # multi_cell permite que el texto largo salte de página automáticamente
            pdf.multi_cell(0, 7, clean(texto_extenso))
            
            pdf_bytes = pdf.output(dest='S')
            st.download_button(
                label="📥 DESCARGAR INFORME EXTENSO (PDF)",
                data=bytes(pdf_bytes),
                file_name=f"Informe_{nombre_alumno}_{fecha}.pdf",
                mime="application/pdf"
            )
