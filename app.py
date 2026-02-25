import streamlit as st
from fpdf import FPDF
import unicodedata
import io
import datetime
from groq import Groq
from supabase import create_client, Client

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"
GROQ_KEY = "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"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# --- FUNCIONES ---
def llamar_ia_analisis(campo, alumno, nivel, ind_l, ind_e):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"Eres un experto pedagogo. Redacta un analisis profesional para el campo {campo} del alumno {alumno} de nivel {nivel}. Indicadores: Lectura {ind_l}, Escritura {ind_e}. Sin asteriscos."
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return "Analisis listo para revision manual."

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

# --- INTERFAZ OSCURA ---
st.set_page_config(page_title="PROFEEDUCA - Reporte IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1e293b 0%, #020617 100%); color: #f8fafc; }
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: #0f172a !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important;
    }
    label { color: #38bdf8 !important; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 Datos")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Alumno")
    comunidad = st.text_input("Comunidad", "PARAJES")
    trimestre = st.selectbox("Trimestre", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado", ["1", "2", "3", "4", "5", "6"])
    fotos = st.file_uploader("Evidencias", type=["jpg", "png"], accept_multiple_files=True)

st.title("📊 Reporte de Evaluación")

c1, c2 = st.columns(2)
ind_l = c1.text_input("Indicador Lectura", "12A")
ind_e = c2.text_input("Indicador Escritura", "6")

if st.button("✨ GENERAR ANALISIS CON IA"):
    if not nombre_alumno:
        st.error("Escribe el nombre del alumno.")
    else:
        with st.spinner("Redactando trayectorias..."):
            for c in ["Lenguajes", "Saberes", "Etica", "Humano"]:
                st.session_state[f"val_{c}"] = llamar_ia_analisis(c, nombre_alumno, nivel_edu, ind_l, ind_e)

eval_campos = {}
cols = st.columns(2)
campos = ["Lenguajes", "Saberes", "Etica", "Humano"]
for i, c in enumerate(campos):
    eval_campos[c] = cols[i % 2].text_area(f"Trayectoria {c}", value=st.session_state.get(f"val_{c}", ""), height=150)

# Calificaciones
eval_detalles = []
if nivel_edu != "Preescolar":
    st.subheader("🔢 Calificaciones")
    mats = ["Español", "Matematicas", "Ciencias", "Historia"]
    for m in mats:
        ca, cb = st.columns([3, 1])
        n = ca.number_input(f"Nota {m}", 5, 10, 8, key=f"n_{m}")
        cl = cb.text_input("Clave", "T", key=f"cl_{m}")
        eval_detalles.append({"m": m, "n": n, "cl": cl})

if st.button("🚀 GUARDAR Y DESCARGAR PDF"):
    try:
        # CORRECCIÓN DE TABLA: Se cambió 'reportes' por 'reflexiones' que es la que sí tienes
        if supabase:
            supabase.table("reflexiones").insert({
                "alumno": nombre_alumno.upper(), 
                "ec": nombre_ec, 
                "texto_reflexivo": eval_campos["Lenguajes"][:200] # Ejemplo de guardado
            }).execute()
        
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 10, clean(f"ALUMNO: {nombre_alumno} | EC: {nombre_ec}"), 0, 1)
        
        for c, t in eval_campos.items():
            pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 8, clean(c), 0, 1)
            pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(t))
        
        if fotos:
            pdf.add_page()
            for f in fotos[:2]:
                pdf.image(io.BytesIO(f.getvalue()), w=90)

        # CORRECCIÓN DE PDF: Se agregaron bytes y encoding
        pdf_out = pdf.output(dest='S')
        pdf_final = pdf_out.encode('latin-1') if isinstance(pdf_out, str) else pdf_out
        
        st.download_button("📥 DESCARGAR", pdf_final, f"Reporte_{nombre_alumno}.pdf", "application/pdf")
        st.success("¡Todo listo, Axel!")
    except Exception as e:
        st.error(f"Error detectado: {e}")
