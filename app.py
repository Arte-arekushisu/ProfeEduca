import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
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
st.title("📊 Fase 0.6: Evaluación Trimestral Formal")

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

# --- SECCIÓN DE TEXTO REFLEXIVO POR CAMPOS ---
st.subheader("🖋️ Trayectorias / Análisis por Campo Formativo")
st.info("Nota: Este contenido debe basarse en tus escritos reflexivos diarios.")

eval_campos = {}
campos_nombres = [
    "Lenguajes", 
    "Saberes y Pensamiento Científico", 
    "Ética, Naturaleza y Sociedades", 
    "De lo Humano y lo Comunitario"
]

# Generar los 4 cuadros de texto para todos los niveles (manual por ahora)
for campo in campos_nombres:
    eval_campos[campo] = st.text_area(f"Análisis de {campo}:", height=120, key=f"text_{campo}")

# --- CAPTURA DE CALIFICACIONES (PRIMARIA/SECUNDARIA) ---
eval_notas = {}
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader("🔢 Calificaciones Numéricas")
    if nivel_edu == "Primaria":
        c1, c2 = st.columns(2)
        for i, campo in enumerate(campos_nombres):
            col = c1 if i < 2 else c2
            eval_notas[campo] = col.number_input(f"Nota: {campo}", 5, 10, 8)
    else: # Secundaria
        materias = ["Español", "Matemáticas", "Ciencias", "Historia", "Geografía", "F. Cívica y Ética"]
        cols = st.columns(3)
        for i, mat in enumerate(materias):
            eval_notas[mat] = cols[i % 3].number_input(mat, 5, 10, 8)

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GENERAR REPORTE DE EVALUACIÓN", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Indica el nombre del alumno.")
    else:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

        # Imprimir Análisis por Campos
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_fill_color(0, 51, 102)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, clean(" ANÁLISIS POR CAMPO FORMATIVO"), 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

        for campo, texto in eval_campos.items():
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
            pdf.set_font('Helvetica', 'I', 10)
            pdf.multi_cell(0, 5, clean(texto if texto else "Sin registro en este periodo."))
            pdf.ln(3)

        # Imprimir Tabla Numérica si aplica
        if nivel_edu != "Preescolar":
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(140, 10, clean(" ASIGNATURA / CAMPO"), 1, 0, 'C', True)
            pdf.cell(50, 10, clean(" CALIFICACIÓN"), 1, 1, 'C', True)
            pdf.set_font('Helvetica', '', 10)
            for concepto, nota in eval_notas.items():
                pdf.cell(140, 10, clean(f" {concepto}"), 1, 0, 'L')
                pdf.cell(50, 10, str(nota), 1, 1, 'C')

        # Fotos y Firmas (igual que la versión anterior)
        if fotos:
            pdf.add_page()
            y_img = 30
            for i, foto in enumerate(fotos[:2]):
                pdf.image(io.BytesIO(foto.getvalue()), x=(10 if i==0 else 110), y=y_img, w=90)

        pdf.set_y(-40)
        pdf.line(20, pdf.get_y(), 80, pdf.get_y())
        pdf.line(130, pdf.get_y(), 190, pdf.get_y())
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_x(20); pdf.cell(60, 5, clean("Firma del EC"), 0, 0, 'C')
        pdf.set_x(130); pdf.cell(60, 5, clean("Firma del Padre / APEC"), 0, 1, 'C')

        st.download_button("📥 DESCARGAR REPORTE", bytes(pdf.output()), f"Eval_{nombre_alumno}.pdf", "application/pdf")
