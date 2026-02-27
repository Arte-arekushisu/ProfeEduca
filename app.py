import streamlit as st
from fpdf import FPDF
import unicodedata
import io
import datetime
from groq import Groq

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.8 IA", layout="wide", page_icon="🤖")

# --- LLAVE DE IA (GROQ) ---
GROQ_KEY = "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"

# --- FUNCIONES DE IA NARRATIVA ---
def llamar_ia_pedagogica(tipo, campo, alumno, nivel):
    try:
        client = Groq(api_key=GROQ_KEY)
        if tipo == "trayectoria":
            # Prompt de cuento/diario reflexivo
            prompt = (f"Como educador, redacta un texto reflexivo breve (estilo cuento pedagógico) "
                      f"sobre el campo {campo} para el alumno {alumno} ({nivel}). "
                      f"Habla de sus retos y logros con calidez humana. Máximo 50 palabras. Sin asteriscos.")
        elif tipo == "resumen":
            prompt = f"Redacta un resumen narrativo y emotivo de aprendizajes para {alumno}. Incluye que vimos y metas. Sin asteriscos."
        else:
            prompt = f"Redacta compromisos motivadores para {alumno}. Sin asteriscos."
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7, max_tokens=600
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return "Érase una vez un gran esfuerzo que dio frutos..."

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REPORTE DE EVALUACION Y APRENDIZAJES'), 0, 1, 'C')
        self.ln(5)

# --- ESTILOS SOS ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    div[data-testid="stExpander"] { border: 2px solid #38bdf8 !important; border-radius: 10px; background-color: #0f172a; }
    .stTextArea textarea { background-color: #1e293b !important; color: #38bdf8 !important; }
    </style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Alumno", placeholder="Ej. Juan Perez")
    comunidad = st.text_input("Comunidad", "PARAJES")
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado/Fase", ["1", "2", "3", "4", "5", "6"])
    
    st.divider()
    st.header("🆘 CENTRO DE AYUDA")
    with st.expander("🚨 BOTÓN SOS", expanded=False):
        if st.button("🤖 Ayuda con la IA"):
            st.info("Asegúrate de haber ingresado el nombre del alumno antes de pedirle a la IA que escriba.")
        if st.button("⚙️ Error de PDF"):
            st.warning("Si sale error de 'encoding', evita usar el signo '¿' o '¡' en los textos manuales.")

# --- CUERPO PRINCIPAL ---
st.title("📊 PROFEEDUCA: Sistema de Evaluación IA")

if st.button("✨ GENERAR TODO EL REPORTE CON IA", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ ¡Falta el nombre del alumno!")
    else:
        with st.spinner("La IA está redactando la historia de aprendizaje..."):
            campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
            for c in campos:
                st.session_state[f"t_{c}"] = llamar_ia_pedagogica("trayectoria", c, nombre_alumno, nivel_edu)
            st.session_state["resumen_ia"] = llamar_ia_pedagogica("resumen", "", nombre_alumno, nivel_edu)
            st.session_state["comp_ia"] = llamar_ia_pedagogica("compromiso", "", nombre_alumno, nivel_edu)

# Campos Formativos
eval_campos = {}
claves_prescolar = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]

cols = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols[i % 2]:
        eval_campos[campo] = st.text_area(f"Reflexión: {campo}", value=st.session_state.get(f"t_{campo}", ""), height=120)
        if nivel_edu == "Preescolar":
            claves_prescolar[campo] = st.text_input(f"Clave {campo}", "T", key=f"cl_{campo}")

st.divider()
resumen_txt = st.text_area("📝 Resumen de Aprendizajes", value=st.session_state.get("resumen_ia", ""), height=150)
compromiso_txt = st.text_area("🤝 Compromisos", value=st.session_state.get("comp_ia", ""), height=100)

# Calificaciones Primaria/Secundaria
eval_detalles = []
if nivel_edu != "Preescolar":
    st.subheader(f"🔢 Calificaciones ({nivel_edu})")
    materias = campos_nombres if nivel_edu == "Primaria" else ["Espanol", "Matematicas", "Ingles", "Ciencias"]
    for mat in materias:
        c1, c2 = st.columns([3, 1])
        nota = c1.number_input(f"Nota: {mat}", 5, 10, 8, key=f"n_{mat}")
        clv = c2.text_input(f"Clave", "T", key=f"c_{mat}")
        eval_detalles.append({"m": mat, "n": nota, "c": clv})

# --- GENERACIÓN PDF ---
if st.button("🚀 FINALIZAR Y DESCARGAR PDF", use_container_width=True):
    try:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(100, 7, clean(f"EDUCADOR: {nombre_ec}"), 0, 0); pdf.cell(90, 7, clean(f"ALUMNO: {nombre_alumno}"), 0, 1)
        pdf.ln(5)

        for campo in campos_nombres:
            pdf.set_fill_color(230, 245, 255)
            h_txt = f"{campo} | CLAVE: {claves_prescolar.get(campo, '')}" if nivel_edu == "Preescolar" else campo
            pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 7, clean(h_txt), 1, 1, 'L', True)
            pdf.set_font("Helvetica", "", 9); pdf.multi_cell(0, 5, clean(eval_campos[campo]), 1)
            pdf.ln(2)

        pdf.ln(5); pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 7, clean("RESUMEN"), 1, 1, 'C', True)
        pdf.set_font("Helvetica", "", 9); pdf.multi_cell(0, 5, clean(resumen_txt), 1)

        if nivel_edu != "Preescolar":
            pdf.ln(5); pdf.set_font("Helvetica", "B", 10)
            for item in eval_detalles:
                pdf.cell(90, 6, clean(item['m']), 1); pdf.cell(45, 6, str(item['n']), 1); pdf.cell(45, 6, clean(item['c']), 1, 1)

        pdf.ln(20)
        pdf.cell(90, 5, "____________________", 0, 0, 'C'); pdf.cell(90, 5, "____________________", 0, 1, 'C')
        pdf.cell(90, 5, "FIRMA EC", 0, 0, 'C'); pdf.cell(90, 5, "FIRMA PADRE", 0, 1, 'C')

        st.download_button("📥 DESCARGAR REPORTE", pdf.output(), f"Reporte_{nombre_alumno}.pdf", "application/pdf")
        st.success("¡Perrón! Reporte generado.")
    except Exception as e:
        st.error(f"Error crítico: {e}")
