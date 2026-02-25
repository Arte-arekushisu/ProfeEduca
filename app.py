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

# --- FUNCIONES DE IA NARRATIVA ---
def llamar_ia_cuento_pedagogico(tipo, campo, alumno, nivel, contexto=""):
    try:
        client = Groq(api_key=GROQ_KEY)
        if tipo == "trayectoria":
            prompt = f"Escribe un cuento breve y emotivo sobre el progreso de {alumno} en el campo {campo}. Describe sus logros como aventuras vencidas. Nivel: {nivel}. Sin asteriscos."
        elif tipo == "resumen":
            prompt = f"Redacta una crónica narrativa de este periodo para {alumno}. Incluye metas, estrategias, qué aprendimos y recursos, usando un tono cálido y humano. Sin asteriscos."
        else:
            prompt = f"Escribe una carta de compromisos inspiradora para {alumno}. Sin asteriscos."
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7, max_tokens=1000
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return "Érase una vez un camino de aprendizaje..."

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReporteNarrativoPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 20, clean('CRONICA DE UN VIAJE DE APRENDIZAJE'), 0, 1, 'C')

# --- INTERFAZ TOTAL DARK ---
st.set_page_config(page_title="PROFEEDUCA - Reporte Narrativo", layout="wide")
st.markdown("<style>.stApp { background: #020617; color: #f8fafc; } .stTextArea textarea, .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important; } label { color: #38bdf8 !important; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🏢 Datos del Encabezado")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    nombre_ec_acompa = st.text_input("Educador de Acompañamiento")
    comunidad = st.text_input("Comunidad", "PARAJES")
    fecha_doc = st.date_input("Fecha de Creación", datetime.date.today())
    st.divider()
    nombre_alumno = st.text_input("Nombre del Alumno")
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado", ["1", "2", "3", "4", "5", "6"])

st.title("📖 Reporte de Evaluación Emotivo")

if st.button("✨ GENERAR CRÓNICA CON IA"):
    with st.spinner("Escribiendo el cuento del alumno..."):
        campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
        for c in campos:
            st.session_state[f"narr_{c}"] = llamar_ia_cuento_pedagogico("trayectoria", c, nombre_alumno, nivel_edu)
        st.session_state["resumen_ia"] = llamar_ia_cuento_pedagogico("resumen", "", nombre_alumno, nivel_edu)
        st.session_state["comp_ia"] = llamar_ia_cuento_pedagogico("compromiso", "", nombre_alumno, nivel_edu)

# --- SECCIÓN POR CAMPO FORMATIVO ---
eval_campos = {}
claves_prescolar = {}
campos_lista = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]

for c in campos_lista:
    with st.expander(f"📍 Campo Formativo: {c}", expanded=True):
        col1, col2 = st.columns([2, 1])
        eval_campos[c] = col1.text_area(f"Trayectoria (Cuento): {c}", value=st.session_state.get(f"narr_{c}", ""), height=150, key=f"t_{c}")
        if nivel_edu == "Preescolar":
            claves_prescolar[c] = col2.text_input(f"Clave {c}", value="T", key=f"cl_{c}")

st.divider()
nombre_proyecto = st.text_input("🚀 Nombre del Proyecto Comunitario", placeholder="Título de la aventura colectiva")

# --- RESUMEN DETALLADO ---
st.subheader("📝 Resumen de Aprendizajes")
resumen_final = st.text_area("Crónica del Periodo (Qué, Cómo, Metas, Estrategias, Emociones)", 
                             value=st.session_state.get("resumen_ia", ""), height=250)

compromisos_final = st.text_area("🤝 Compromisos del Alumno", value=st.session_state.get("comp_ia", ""), height=150)

# --- CALIFICACIONES (SI NO ES PREESCOLAR) ---
eval_detalles = []
if nivel_edu != "Preescolar":
    st.subheader("📊 Tabla de Notas")
    mats = ["Español", "Matemáticas", "Ciencias", "Historia"] if nivel_edu == "Primaria" else ["Español", "Matemáticas", "Inglés", "Historia"]
    for m in mats:
        c1, c2 = st.columns([3, 1])
        n = c1.number_input(f"Nota {m}", 5, 10, 8, key=f"n_{m}")
        clv = c2.text_input(f"Clave", "T", key=f"clv_{m}")
        eval_detalles.append({"m": m, "n": n, "c": clv})

# --- GENERAR PDF ---
if st.button("🚀 FINALIZAR Y DESCARGAR REPORTE"):
    pdf = ReporteNarrativoPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 10)
    
    # Encabezado
    pdf.cell(100, 7, clean(f"EDUCADOR: {nombre_ec}"), 0, 0); pdf.cell(90, 7, clean(f"ACOMPA: {nombre_ec_acompa}"), 0, 1)
    pdf.cell(100, 7, clean(f"COMUNIDAD: {comunidad}"), 0, 0); pdf.cell(90, 7, clean(f"FECHA: {fecha_doc}"), 0, 1)
    pdf.cell(0, 7, clean(f"PROYECTO: {nombre_proyecto}"), 0, 1); pdf.ln(5)

    # Campos Formativos
    for c in campos_lista:
        pdf.set_fill_color(230, 245, 255)
        txt_header = f"{c} - Clave: {claves_prescolar.get(c, '')}" if nivel_edu == "Preescolar" else c
        pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 7, clean(txt_header), 1, 1, 'L', True)
        pdf.set_font("Helvetica", "", 9); pdf.multi_cell(0, 5, clean(eval_campos[c]), 1)
        pdf.ln(2)

    # Resumen y Compromisos
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11); pdf.cell(0, 8, clean("RESUMEN DE APRENDIZAJES"), 1, 1, 'C', True)
    pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(resumen_final), 1); pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 11); pdf.cell(0, 8, clean("COMPROMISOS DEL ALUMNO"), 1, 1, 'C', True)
    pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(compromisos_final), 1); pdf.ln(5)

    # Calificaciones
    if nivel_edu != "Preescolar":
        pdf.set_font("Helvetica", "B", 10); pdf.cell(90, 7, "MATERIA", 1); pdf.cell(45, 7, "NOTA", 1); pdf.cell(45, 7, "CLAVE", 1, 1)
        for it in eval_detalles:
            pdf.set_font("Helvetica", "", 9); pdf.cell(90, 6, clean(it['m']), 1); pdf.cell(45, 6, str(it['n']), 1); pdf.cell(45, 6, clean(it['c']), 1, 1)

    # Firmas
    pdf.ln(25)
    pdf.cell(90, 10, "__________________________", 0, 0, 'C'); pdf.cell(10, 10, "", 0, 0); pdf.cell(90, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 5, clean(f"FIRMA EDUCADOR: {nombre_ec}"), 0, 0, 'C'); pdf.cell(10, 5, "", 0, 0); pdf.cell(90, 5, clean("FIRMA PADRE / MADRE / TUTOR"), 0, 1, 'C')

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 DESCARGAR REPORTE NARRATIVO", pdf_bytes, f"Cuento_{nombre_alumno}.pdf", "application/pdf")
