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
st.title("📊 Fase 0.6: Evaluación y Trayectorias")

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

# --- SECCIÓN DINÁMICA DE ANÁLISIS ---
eval_campos = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Ética, N. y S.", "De lo Humano y lo Com."]

if nivel_edu == "Preescolar":
    st.subheader("🖋️ Trayectorias Personalizadas (Manual)")
    st.info("Escribe detalladamente el progreso del alumno para cada campo.")
    for campo in campos_nombres:
        eval_campos[campo] = st.text_area(f"Trayectoria en {campo}:", height=120, key=f"pre_{campo}")
else:
    st.subheader("🤖 Análisis por Campo Formativo (IA-Ready)")
    st.warning("Este apartado será autocompletado por la IA basándose en tus bitácoras diarias.")
    for campo in campos_nombres:
        eval_campos[campo] = st.text_area(f"Vista previa del Análisis en {campo}:", height=100, key=f"ia_{campo}")

# --- INDICADORES Y CALIFICACIONES ---
st.divider()
st.subheader("📖 Indicadores de Lectura y Escritura")
col_ind1, col_ind2 = st.columns(2)
indicador_lectura = col_ind1.text_input("Indicador de Lectura (12A, 1B, etc.)", "12A")
indicador_escritura = col_ind2.text_input("Indicador de Escritura (6, etc.)", "6")

eval_detalles = []
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader(f"🔢 Calificaciones y Claves ({nivel_edu})")
    
    items_lista = campos_nombres if nivel_edu == "Primaria" else ["Español", "Matemáticas", "Ciencias", "Historia", "Geografía", "F. Cívica y Ética"]
    
    for item in items_lista:
        c1, c2 = st.columns([2, 1])
        nota = c1.number_input(f"Nota: {item}", 5, 10, 8, key=f"n_{item}")
        clave = c2.text_input(f"Clave (Máx T120)", "T", max_chars=4, key=f"c_{item}")
        eval_detalles.append({"concepto": item, "nota": nota, "clave": clave})

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GENERAR REPORTE FINAL", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Indica el nombre del alumno.")
    else:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

        # Indicadores
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(95, 8, clean(f"INDICADOR LECTURA: {indicador_lectura}"), 1, 0, 'L')
        pdf.cell(95, 8, clean(f"INDICADOR ESCRITURA: {indicador_escritura}"), 1, 1, 'L')
        pdf.ln(5)

        # Trayectorias / Análisis
        titulo_seccion = "TRAYECTORIAS PERSONALIZADAS" if nivel_edu == "Preescolar" else "ANÁLISIS POR CAMPO FORMATIVO"
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_fill_color(0, 51, 102); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, clean(f" {titulo_seccion}"), 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

        for campo, texto in eval_campos.items():
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
            pdf.set_font('Helvetica', 'I', 9)
            pdf.multi_cell(0, 5, clean(texto if texto else "Pendiente de registro."))
            pdf.ln(2)

        # Calificaciones
        if nivel_edu != "Preescolar":
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 10); pdf.set_fill_color(200, 200, 200)
            pdf.cell(100, 10, clean(" ASIGNATURA / CAMPO"), 1, 0, 'C', True)
            pdf.cell(45, 10, clean(" CALIFICACIÓN"), 1, 0, 'C', True)
            pdf.cell(45, 10, clean(" CLAVE"), 1, 1, 'C', True)
            pdf.set_font('Helvetica', '', 10)
            for it in eval_detalles:
                pdf.cell(100, 10, clean(f" {it['concepto']}"), 1, 0, 'L')
                pdf.cell(45, 10, str(it['nota']), 1, 0, 'C')
                pdf.cell(45, 10, clean(it['clave']), 1, 1, 'C')

        # Fotos
        if fotos:
            pdf.add_page()
            y_img = 30
            for i, foto in enumerate(fotos[:2]):
                pdf.image(io.BytesIO(foto.getvalue()), x=(10 if i==0 else 110), y=y_img, w=90)

        # Firmas
        pdf.set_y(-40)
        pdf.line(20, pdf.get_y(), 80, pdf.get_y())
        pdf.line(130, pdf.get_y(), 190, pdf.get_y())
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_x(20); pdf.cell(60, 5, clean("Firma del EC"), 0, 0, 'C')
        pdf.set_x(130); pdf.cell(60, 5, clean("Firma del Padre / APEC"), 0, 1, 'C')

        st.download_button("📥 DESCARGAR REPORTE", bytes(pdf.output()), f"Eval_{nombre_alumno}.pdf", "application/pdf")
