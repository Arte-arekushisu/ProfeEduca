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
st.title("📊 Fase 0.6: Evaluación con Indicadores y Claves")

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
eval_campos = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Ética, N. y S.", "De lo Humano y lo Com."]

for campo in campos_nombres:
    eval_campos[campo] = st.text_area(f"Análisis de {campo}:", height=100, key=f"text_{campo}")

# --- INDICADORES DE LECTO-ESCRITURA (NUEVO) ---
st.divider()
st.subheader("📖 Indicadores de Lectura y Escritura")
col_ind1, col_ind2 = st.columns(2)
indicador_lectura = col_ind1.text_input("Indicador de Lectura (Ej: 12A, 1B, 3C, 4D)", placeholder="12A")
indicador_escritura = col_ind2.text_input("Indicador de Escritura (Ej: 6)", placeholder="6")

# --- CAPTURA DE CALIFICACIONES Y CLAVES (NUEVO) ---
eval_detalles = [] # Lista de diccionarios para guardar concepto, nota y clave

if nivel_edu != "Preescolar":
    st.divider()
    st.subheader(f"🔢 Calificaciones y Claves ({nivel_edu})")
    
    if nivel_edu == "Primaria":
        for campo in campos_nombres:
            c1, c2 = st.columns([2, 1])
            nota = c1.number_input(f"Nota: {campo}", 5, 10, 8, key=f"nota_{campo}")
            clave = c2.text_input(f"Clave (Máx T120)", "T", max_chars=4, key=f"clave_{campo}")
            eval_detalles.append({"concepto": campo, "nota": nota, "clave": clave})
    
    else: # Secundaria
        materias = ["Español", "Matemáticas", "Ciencias", "Historia", "Geografía", "F. Cívica y Ética"]
        for mat in materias:
            c1, c2 = st.columns([2, 1])
            nota = c1.number_input(f"Nota: {mat}", 5, 10, 8, key=f"nota_{mat}")
            clave = c2.text_input(f"Clave (Máx T120)", "T", max_chars=4, key=f"clave_{mat}")
            eval_detalles.append({"concepto": mat, "nota": nota, "clave": clave})

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GENERAR REPORTE DE EVALUACIÓN", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Indica el nombre del alumno.")
    else:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

        # 1. Indicadores de Lecto-Escritura
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(95, 8, clean(f"INDICADOR LECTURA: {indicador_lectura}"), 1, 0, 'L')
        pdf.cell(95, 8, clean(f"INDICADOR ESCRITURA: {indicador_escritura}"), 1, 1, 'L')
        pdf.ln(5)

        # 2. Análisis por Campos
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_fill_color(0, 51, 102); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, clean(" ANÁLISIS POR CAMPO FORMATIVO"), 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

        for campo, texto in eval_campos.items():
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
            pdf.set_font('Helvetica', 'I', 9)
            pdf.multi_cell(0, 5, clean(texto if texto else "Sin registro."))
            pdf.ln(2)

        # 3. Tabla de Calificaciones y Claves
        if nivel_edu != "Preescolar":
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(100, 10, clean(" ASIGNATURA / CAMPO"), 1, 0, 'C', True)
            pdf.cell(45, 10, clean(" CALIFICACIÓN"), 1, 0, 'C', True)
            pdf.cell(45, 10, clean(" CLAVE"), 1, 1, 'C', True)
            
            pdf.set_font('Helvetica', '', 10)
            for item in eval_detalles:
                pdf.cell(100, 10, clean(f" {item['concepto']}"), 1, 0, 'L')
                pdf.cell(45, 10, str(item['nota']), 1, 0, 'C')
                pdf.cell(45, 10, clean(item['clave']), 1, 1, 'C')

        # 4. Fotos y Firmas
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
