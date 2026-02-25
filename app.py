import streamlit as st
from fpdf import FPDF
import unicodedata
import io
import datetime
from groq import Groq
from supabase import create_client, Client

# --- CONFIGURACIÓN DE CONEXIONES ---
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"
GROQ_KEY = "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"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# --- FUNCIONES DE IA ---
def llamar_ia_analisis(campo, alumno, nivel, ind_l, ind_e):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Eres un experto en el Modelo ABCD. Redacta un análisis cualitativo profesional.
        CAMPO: {campo} | ALUMNO: {alumno} | NIVEL: {nivel}
        INDICADORES: Lectura {ind_l}, Escritura {ind_e}.
        Escribe un párrafo fluido, pedagógico y sin asteriscos.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return ""

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REPORTE DE EVALUACION TRIMESTRAL'), 0, 1, 'C')

# --- INTERFAZ CON DISEÑO OSCURO ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.6 IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1e293b 0%, #020617 100%); color: #f8fafc; }
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: #0f172a !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important;
    }
    label { color: #38bdf8 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Reporte Trimestral Inteligente")

# Formulario principal
with st.sidebar:
    st.header("👤 Datos Generales")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Alumno")
    comunidad = st.text_input("Comunidad", "PARAJES")
    trimestre = st.selectbox("Periodo", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado", ["1", "2", "3", "4", "5", "6"])

st.subheader("📝 Indicadores y Trayectorias")
c1, c2 = st.columns(2)
ind_l = c1.text_input("Indicador Lectura", "12A")
ind_e = c2.text_input("Indicador Escritura", "6")

if st.button("✨ GENERAR ANÁLISIS CON IA"):
    if not nombre_alumno:
        st.error("Escribe el nombre del alumno.")
    else:
        with st.spinner("IA redactando..."):
            campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
            for c in campos:
                st.session_state[f"text_{c}"] = llamar_ia_analisis(c, nombre_alumno, nivel_edu, ind_l, ind_e)

# Áreas de texto para los campos formativos
eval_campos = {}
col_a, col_b = st.columns(2)
for i, campo in enumerate(["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]):
    target_col = col_a if i % 2 == 0 else col_b
    eval_campos[campo] = target_col.text_area(f"Trayectoria: {campo}", value=st.session_state.get(f"text_{campo}", ""), height=150)

# Calificaciones (Solo si no es Preescolar)
eval_detalles = []
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader("🔢 Calificaciones")
    mats = ["Español", "Matemáticas", "Naturaleza", "Comunidad"] if nivel_edu == "Primaria" else ["Español", "Matemáticas", "Ciencias", "Historia", "Inglés"]
    for m in mats:
        ca, cb = st.columns([3, 1])
        n = ca.number_input(f"Nota {m}", 5, 10, 8, key=f"n_{m}")
        cl = cb.text_input("Clave", "T", key=f"cl_{m}")
        eval_detalles.append({"m": m, "n": n, "cl": cl})

# Botón Final
if st.button("🚀 GUARDAR Y DESCARGAR PDF"):
    try:
        # Guardar en Supabase
        if supabase:
            supabase.table("reportes").insert({"alumno": nombre_alumno.upper(), "trimestre": trimestre, "ec": nombre_ec}).execute()
        
        # Crear PDF
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 10, clean(f"ALUMNO: {nombre_alumno} | PERIODO: {trimestre}"), 0, 1)
        
        for c, t in eval_campos.items():
            pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 8, clean(f"{c}:"), 0, 1)
            pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(t))
            pdf.ln(2)

        if nivel_edu != "Preescolar":
            pdf.ln(5)
            for item in eval_detalles:
                pdf.cell(80, 8, clean(item['m']), 1)
                pdf.cell(20, 8, str(item['n']), 1)
                pdf.cell(20, 8, clean(item['cl']), 1, 1)

        pdf_out = pdf.output(dest='S')
        pdf_bytes = pdf_out.encode('latin-1') if isinstance(pdf_out, str) else pdf_out
        st.download_button("📥 DESCARGAR REPORTE", pdf_bytes, f"Reporte_{nombre_alumno}.pdf", "application/pdf")
        st.success("¡Listo!")
    except Exception as e:
        st.error(f"Error: {e}")
