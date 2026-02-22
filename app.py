import streamlit as st
from fpdf import FPDF
import unicodedata
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.6", layout="wide", page_icon="📊")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt

class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REPORTE DE EVALUACION TRIMESTRAL'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, com, alumno, niv, gra, periodo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        w, h = 95, 8
        self.cell(w, h, clean(f" EDUCADOR: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {com}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" ALUMNO: {alumno}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" TRIMESTRE: {periodo}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" NIVEL: {niv}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO: {gra}"), 1, 1, 'L', True)
        self.ln(10)

# --- INTERFAZ ---
st.title("📊 Fase 0.6: Evaluación con Integración IA")

with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno")
    comunidad = st.text_input("Comunidad", "CRUZ")
    trimestre = st.selectbox("Trimestre", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.text_input("Grado/Fase", "1")
    
    st.divider()
    st.header("📸 Evidencias")
    fotos = st.file_uploader("Subir imágenes (Máx. 2)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

st.divider()

# --- SECCIÓN DE ANÁLISIS / TRAYECTORIAS ---
eval_campos = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]

if nivel_edu == "Preescolar":
    st.subheader("🖋️ Trayectorias Personalizadas (Llenado Manual)")
    st.info("💡 Como es Preescolar, registra manualmente los avances observados en cada campo.")
    placeholder_text = "Escribe aquí la trayectoria observada..."
else:
    st.subheader("🤖 Análisis Cualitativo por Campo Formativo (IA-Ready)")
    st.info("💡 Este espacio está diseñado para ser completado por la IA a partir de las bitácoras diarias.")
    placeholder_text = "La IA generará este texto basado en tus registros diarios..."

cols = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols[i % 2]:
        eval_campos[campo] = st.text_area(f"{'Trayectoria' if nivel_edu == 'Preescolar' else 'Análisis'} de {campo}:", 
                                        height=120, key=f"eval_{campo}", 
                                        placeholder=placeholder_text)

# --- INDICADORES ---
st.divider()
st.subheader("📖 Indicadores de Logro")
col_ind1, col_ind2 = st.columns(2)
indicador_lectura = col_ind1.text_input("Indicador de Lectura (ej. 12A)", "12A")
indicador_escritura = col_ind2.text_input("Indicador de Escritura (ej. 6)", "6")

# --- CALIFICACIONES Y CLAVES (SOLO PRIMARIA / SECUNDARIA) ---
eval_detalles = []
if nivel_edu != "Pre
