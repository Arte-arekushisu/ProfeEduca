import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Evaluación Trimestral", layout="wide", page_icon="📊")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt

class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102) # Azul Institucional para Evaluaciones
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
st.title("📊 Fase 0.6: Evaluación Trimestral")

with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno")
    comunidad = st.text_input("Comunidad", "CRUZ")
    trimestre = st.selectbox("Periodo", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
    grados_op = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel_edu == "Primaria" else ["1", "2", "3", "Multigrado"]
    grado_edu = st.selectbox("Grado", grados_op)

st.divider()

# --- LÓGICA DE CAPTURA SEGÚN NIVEL ---
eval_data = {}

if nivel_edu == "Preescolar":
    st.subheader("🎨 Evaluación de Trayectorias")
    eval_data['trayectorias'] = st.text_area("Describa las trayectorias de aprendizaje (basado en escritos diarios):", height=300)

elif nivel_edu == "Primaria":
    st.subheader("🔢 Calificación por Campos Formativos")
    c1, c2 = st.columns(2)
    with c1:
        eval_data['Lenguajes'] = st.number_input("Lenguajes", 5, 10, 8)
        eval_data['Saberes y P. Cientifico'] = st.number_input("Saberes y Pensamiento Científico", 5, 10, 8)
    with c2:
        eval_data['Etica, Nat. y Soc.'] = st.number_input("Ética, Naturaleza y Sociedades", 5, 10, 8)
        eval_data['De lo Hum. y lo Com.'] = st.number_input("De lo Humano y lo Comunitario", 5, 10, 8)

else: # Secundaria
    st.subheader("📚 Calificación por Materias")
    c1, c2, c3 = st.columns(3)
    with c1:
        eval_data['Español'] = st.number_input("Español", 5, 10, 8)
        eval_data['Matemáticas'] = st.number_input("Matemáticas", 5, 10, 8)
    with c2:
        eval_data['Ciencias'] = st.number_input("Ciencias", 5, 10, 8)
        eval_data['Historia'] = st.number_input("Historia", 5, 10, 8)
    with c3:
        eval_data['Geografía'] = st.number_input("Geografía", 5, 10, 8)
        eval_data['F. Cívica y Ética'] = st.number_input("F. Cívica y Ética", 5, 10, 8)

# --- GENERACIÓN DE DOCUMENTO ---
if st.button("📊 GENERAR EVALUACION TRIMESTRAL", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Por favor, ingresa el nombre del alumno.")
    else:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_fill_color(0, 51, 102)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, clean(f" RESULTADOS DEL {trimestre.upper()}"), 0, 1, 'L', True)
        pdf.ln(5)
        pdf.set_text_color(0, 0, 0)

        if nivel_edu == "Preescolar":
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 7, clean(eval_data['trayectorias']))
        else:
            # Tabla para Primaria y Secundaria
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(140, 10, clean(" ASIGNATURA / CAMPO"), 1, 0, 'C')
            pdf.cell(50, 10, clean(" CALIFICACION"), 1, 1, 'C')
            pdf.set_font('Helvetica', '', 10)
            
            for concepto, nota in eval_data.items():
                pdf.cell(140, 10, clean(f" {concepto}"), 1, 0, 'L')
                pdf.cell(50, 10, str(nota), 1, 1, 'C')

        # Pie de página para firmas
        pdf.ln(20)
        pdf.line(30, pdf.get_y(), 90, pdf.get_y())
        pdf.line(120, pdf.get_y(), 180, pdf.get_y())
        pdf.set_y(pdf.get_y() + 2)
        pdf.cell(95, 5, clean("Firma del Educador"), 0, 0, 'C')
        pdf.cell(95, 5, clean("Sello / Firma Monitor"), 0, 1, 'C')

        pdf_bytes = bytes(pdf.output())
        st.success(f"✅ Evaluación de {nombre_alumno} generada.")
        st.download_button("📥 DESCARGAR REPORTE", pdf_bytes, f"Evaluacion_{nombre_alumno}.pdf", "application/pdf")
