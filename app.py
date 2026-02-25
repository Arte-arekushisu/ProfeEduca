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
def llamar_ia_pedagogica(tipo, campo, alumno, nivel):
    try:
        client = Groq(api_key=GROQ_KEY)
        if tipo == "trayectoria":
            prompt = f"Redacta una trayectoria de aprendizaje para el campo {campo} del alumno {alumno} ({nivel}). Sé profesional, pedagógico y no uses asteriscos."
        else:
            prompt = f"Redacta compromisos de aprendizaje específicos y motivadores para el alumno {alumno} ({nivel}) para el siguiente periodo. Sin asteriscos."
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6, max_tokens=600
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return ""

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReporteFinalPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 20, clean('REPORTE DE EVALUACION Y COMPROMISOS'), 0, 1, 'C')

# --- INTERFAZ STREAMLIT (TOTAL DARK) ---
st.set_page_config(page_title="PROFEEDUCA - Reporte Final", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; }
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #020617; }
    hr { border: 1px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 Generador de Reporte Formativo")

with st.sidebar:
    st.header("🏢 Encabezado")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_ec_acompa = st.text_input("Educador de Acompañamiento")
    comunidad = st.text_input("Comunidad", "PARAJES")
    fecha_doc = st.date_input("Fecha de creación", datetime.date.today())
    
    st.divider()
    nombre_alumno = st.text_input("Nombre del Alumno")
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado/Fase", ["1", "2", "3", "4", "5", "6"])

# --- CONTENIDO ---
st.subheader("🤖 Redacción Automatizada")
if st.button("✨ GENERAR TODO CON IA"):
    if not nombre_alumno: st.error("Falta nombre del alumno")
    else:
        with st.spinner("Redactando informe completo..."):
            campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
            for c in campos:
                st.session_state[f"t_{c}"] = llamar_ia_pedagogica("trayectoria", c, nombre_alumno, nivel_edu)
            st.session_state["compromiso_ia"] = llamar_ia_pedagogica("compromiso", "", nombre_alumno, nivel_edu)

col_a, col_b = st.columns(2)
eval_campos = {}
for i, c in enumerate(["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]):
    area = col_a if i < 2 else col_b
    eval_campos[c] = area.text_area(f"Trayectoria: {c}", value=st.session_state.get(f"t_{c}", ""), height=120)

st.divider()
# Campo de Clave para Preescolar
clave_preescolar = ""
if nivel_edu == "Preescolar":
    clave_preescolar = st.text_area("Clave (Exclusivo Preescolar)", value="T", help="Inicia con T seguido de números")

compromiso_txt = st.text_area("🤝 Compromisos del Alumno", value=st.session_state.get("compromiso_ia", ""), height=120)

# --- CALIFICACIONES ---
eval_detalles = []
if nivel_edu != "Preescolar":
    st.subheader("📊 Calificaciones y Materias")
    if nivel_edu == "Primaria":
        materias = ["Lenguajes", "Saberes", "Etica", "Humano"]
    else: # Secundaria
        materias = ["Español", "Matemáticas", "Inglés", "Historia", "Geografía", "Artes", "Ed. Física"]
        if grado_edu == "1": materias.insert(2, "Biología")
        elif grado_edu == "2": materias.insert(2, "Física")
        else: materias.insert(2, "Química")

    for m in materias:
        c1, c2 = st.columns([3, 1])
        n = c1.number_input(f"{m}", 5, 10, 8, key=f"n_{m}")
        clv = c2.text_input(f"Clave", "T", key=f"cl_{m}")
        eval_detalles.append({"m": m, "n": n, "c": clv})

# --- PDF Y GUARDADO ---
if st.button("🚀 FINALIZAR DOCUMENTO Y DESCARGAR"):
    try:
        # Guardar en Supabase
        if supabase:
            supabase.table("reflexiones").insert({"alumno": nombre_alumno.upper(), "ec": nombre_ec, "fecha": str(fecha_doc)}).execute()

        pdf = ReporteFinalPDF()
        pdf.add_page()
        
        # Encabezado Detallado
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(100, 8, clean(f"EDUCADOR: {nombre_ec}"), 0, 0)
        pdf.cell(90, 8, clean(f"ACOMPAÑAMIENTO: {nombre_ec_acompa}"), 0, 1)
        pdf.cell(100, 8, clean(f"COMUNIDAD: {comunidad}"), 0, 0)
        pdf.cell(90, 8, clean(f"FECHA: {fecha_doc}"), 0, 1)
        pdf.ln(5)

        # Trayectorias
        pdf.set_fill_color(230, 245, 255)
        for campo, texto in eval_campos.items():
            pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 8, clean(campo), 1, 1, 'L', True)
            pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(texto), 1)
            pdf.ln(2)

        if nivel_edu == "Preescolar":
            pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 8, clean("CLAVE:"), 0, 1)
            pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(clave_preescolar))

        # Compromisos
        pdf.ln(5); pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 8, clean("COMPROMISOS DEL ALUMNO"), 1, 1, 'C', True)
        pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 6, clean(compromiso_txt), 1)

        # Tabla de Notas
        if nivel_edu != "Preescolar":
            pdf.ln(5); pdf.set_font("Helvetica", "B", 10)
            pdf.cell(90, 8, "MATERIA", 1); pdf.cell(45, 8, "NOTA", 1); pdf.cell(45, 8, "CLAVE", 1, 1)
            pdf.set_font("Helvetica", "", 10)
            for item in eval_detalles:
                pdf.cell(90, 7, clean(item['m']), 1); pdf.cell(45, 7, str(item['n']), 1); pdf.cell(45, 7, clean(item['c']), 1, 1)

        # Firmas
        pdf.ln(20)
        pdf.cell(90, 10, "__________________________", 0, 0, 'C')
        pdf.cell(10, 10, "", 0, 0)
        pdf.cell(90, 10, "__________________________", 0, 1, 'C')
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(90, 5, clean(f"FIRMA DEL EDUCADOR: {nombre_ec}"), 0, 0, 'C')
        pdf.cell(10, 5, "", 0, 0)
        pdf.cell(90, 5, clean("FIRMA PADRE / MADRE / TUTOR"), 0, 1, 'C')

        # Salida Segura
        pdf_out = pdf.output(dest='S')
        pdf_bytes = pdf_out.encode('latin-1') if isinstance(pdf_out, str) else pdf_out
        st.download_button("📥 DESCARGAR REPORTE PDF", pdf_bytes, f"Reporte_{nombre_alumno}.pdf", "application/pdf")
        st.success("¡Documento generado exitosamente!")

    except Exception as e:
        st.error(f"Error técnico: {e}")
