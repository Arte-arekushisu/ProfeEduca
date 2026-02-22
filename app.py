import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from PIL import Image
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
st.title("📊 Evaluación Trimestral Formal")

with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno")
    comunidad = st.text_input("Comunidad", "CRUZ")
    trimestre = st.selectbox("Periodo", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.text_input("Grado/Fase", "1")
    
    st.divider()
    st.header("📸 Evidencias")
    fotos = st.file_uploader("Subir hasta 2 fotos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# --- CONTENIDO DE EVALUACIÓN ---
st.subheader("🖋️ Análisis Reflexivo General")
reflexion_global = st.text_area("Texto reflexivo evaluatorio (Basado en escritos diarios):", height=150)

eval_data = {}

if nivel_edu == "Preescolar":
    st.subheader("🎨 Trayectorias por Campo Formativo")
    eval_data['Lenguajes'] = st.text_area("Lenguajes (Trayectoria):", height=100)
    eval_data['Saberes y P.C.'] = st.text_area("Saberes y Pensamiento Científico (Trayectoria):", height=100)
    eval_data['Etica, N. y S.'] = st.text_area("Ética, Naturaleza y Sociedades (Trayectoria):", height=100)
    eval_data['De lo H. y lo C.'] = st.text_area("De lo Humano y lo Comunitario (Trayectoria):", height=100)

elif nivel_edu == "Primaria":
    st.subheader("🔢 Calificación Numérica (Campos)")
    c1, c2 = st.columns(2)
    with c1:
        eval_data['Lenguajes'] = st.number_input("Lenguajes", 5, 10, 8)
        eval_data['Saberes y P.C.'] = st.number_input("Saberes y P.C.", 5, 10, 8)
    with c2:
        eval_data['Etica, N. y S.'] = st.number_input("Etica, N. y S.", 5, 10, 8)
        eval_data['De lo H. y lo C.'] = st.number_input("De lo H. y lo C.", 5, 10, 8)

else: # Secundaria
    st.subheader("📚 Calificación por Materias")
    materias = ["Español", "Matemáticas", "Ciencias", "Historia", "Geografía", "F. Cívica y Ética"]
    cols = st.columns(3)
    for i, mat in enumerate(materias):
        eval_data[mat] = cols[i % 3].number_input(mat, 5, 10, 8)

# --- GENERACIÓN PDF ---
if st.button("📊 GENERAR EVALUACION FORMAL", use_container_width=True):
    pdf = EvaluacionPDF()
    pdf.add_page()
    pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

    # 1. Reflexión Global
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, clean("ANÁLISIS REFLEXIVO EVALUATORIO"), 0, 1, 'L')
    pdf.set_font('Helvetica', 'I', 10)
    pdf.multi_cell(0, 5, clean(reflexion_global))
    pdf.ln(5)

    # 2. Detalle por Nivel
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, clean("DESEMPEÑO POR CAMPO / MATERIA"), 0, 1, 'L', True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    for campo, contenido in eval_data.items():
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
        pdf.set_font('Helvetica', '', 10)
        if nivel_edu == "Preescolar":
            pdf.multi_cell(0, 5, clean(contenido))
            pdf.ln(2)
        else:
            pdf.cell(0, 7, str(contenido), 0, 1)
            pdf.ln(1)

    # 3. Fotos
    if fotos:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, clean("EVIDENCIAS FOTOGRÁFICAS"), 0, 1, 'C')
        y_img = pdf.get_y()
        for i, foto in enumerate(fotos[:2]):
            img_data = io.BytesIO(foto.getvalue())
            pdf.image(img_data, x=(10 if i==0 else 110), y=y_img, w=90)

    # 4. Firmas
    pdf.set_y(-40)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.line(20, pdf.get_y(), 80, pdf.get_y())
    pdf.line(130, pdf.get_y(), 190, pdf.get_y())
    pdf.set_y(pdf.get_y() + 2)
    pdf.set_x(20)
    pdf.cell(60, 5, clean("Firma del EC"), 0, 0, 'C')
    pdf.set_x(130)
    pdf.cell(60, 5, clean("Firma del Padre / APEC"), 0, 1, 'C')

    st.download_button("📥 DESCARGAR EVALUACIÓN", bytes(pdf.output()), f"Eval_{nombre_alumno}.pdf", "application/pdf")
