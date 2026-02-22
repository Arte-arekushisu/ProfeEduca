import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
from PIL import Image
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Evaluación Trimestral", layout="wide", page_icon="📊")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102) # Azul formal
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
st.title("📊 Fase 0.6: Evaluación Formal")

with st.sidebar:
    st.header("📌 Datos del Alumno")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno")
    comunidad = st.text_input("Comunidad", "CRUZ")
    trimestre = st.selectbox("Trimestre", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grados_op = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel_edu == "Primaria" else ["1", "2", "3", "Multigrado"]
    grado_edu = st.selectbox("Grado", grados_op)
    
    st.divider()
    st.header("📸 Evidencias")
    img1 = st.file_uploader("Subir Imagen 1 (Opcional)", type=["jpg", "png", "jpeg"])
    img2 = st.file_uploader("Subir Imagen 2 (Opcional)", type=["jpg", "png", "jpeg"])

st.divider()

# --- CAPTURA DE EVALUACIÓN ---
eval_data = {}

# Texto Reflexivo Basado en los 4 Campos Formativos (Para todos los niveles)
st.subheader("🖋️ Texto Reflexivo Evaluatorio")
st.info("Sintetice el desempeño basado en los escritos diarios y los 4 campos formativos.")
texto_reflexivo = st.text_area("Análisis pedagógico trimestral:", height=200, 
                               placeholder="Describa el avance en Lenguajes, Saberes, Ética y lo Comunitario...")

if nivel_edu == "Preescolar":
    st.subheader("🎨 Trayectorias (Preescolar)")
    eval_data['trayectorias'] = st.text_area("Descripción manual de trayectorias:", height=150)

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

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GENERAR EVALUACION FORMAL", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Por favor ingresa el nombre del alumno.")
    else:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

        # 1. Bloque de Texto Reflexivo
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, clean(" ANALISIS REFLEXIVO Y CAMPOS FORMATIVOS"), 0, 1, 'L', True)
        pdf.ln(2)
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, clean(texto_reflexivo))
        pdf.ln(5)

        # 2. Bloque de Calificaciones / Trayectorias
        if nivel_edu == "Preescolar":
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(0, 8, clean(" TRAYECTORIAS DE APRENDIZAJE"), 1, 1, 'L', True)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, clean(eval_data.get('trayectorias', '')))
        else:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(140, 10, clean(" CONCEPTO"), 1, 0, 'C', True)
            pdf.cell(50, 10, clean(" NOTA"), 1, 1, 'C', True)
            pdf.set_font('Helvetica', '', 10)
            for k, v in eval_data.items():
                if k != 'trayectorias':
                    pdf.cell(140, 10, clean(f" {k}"), 1, 0, 'L')
                    pdf.cell(50, 10, str(v), 1, 1, 'C')

        # 3. Espacio para Fotos
        if img1 or img2:
            pdf.ln(10)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(0, 10, clean(" EVIDENCIAS DE TRABAJO"), 0, 1, 'L')
            y_fotos = pdf.get_y()
            if img1:
                pdf.image(img1, x=10, y=y_fotos, w=90)
            if img2:
                pdf.image(img2, x=110, y=y_fotos, w=90)
            pdf.ln(65) # Espacio para que no se encimen las firmas

        # 4. Apartado de Firmas
        pdf.set_y(-40) # Posicionar al final de la página
        pdf.set_font('Helvetica', 'B', 9)
        pdf.line(20, pdf.get_y(), 80, pdf.get_y()) # Línea EC
        pdf.line(130, pdf.get_y(), 190, pdf.get_y()) # Línea Padre
        
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_x(20)
        pdf.cell(60, 5, clean("Firma del EC"), 0, 0, 'C')
        pdf.set_x(130)
        pdf.cell(60, 5, clean("Firma del Padre / APEC"), 0, 1, 'C')

        # Salida
        pdf_bytes = pdf.output()
        st.success("✅ Evaluación generada con éxito.")
        st.download_button("📥 DESCARGAR REPORTE FORMAL", bytes(pdf_bytes), f"Evaluacion_{nombre_alumno}.pdf", "application/pdf")
        
