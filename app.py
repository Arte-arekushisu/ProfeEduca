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
st.title("📊 Fase 0.6: Evaluación Trimestral")

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

# --- SECCIÓN UNIVERSAL DE ANÁLISIS (IA-READY) ---
# Esta sección es igual para todos, preparando el terreno para Gemini
st.subheader("🖋️ Análisis por Campo Formativo")
st.info("💡 Este apartado se alimentará automáticamente de tus bitácoras diarias mediante IA.")

eval_campos = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Ética, N. y S.", "De lo Humano y lo Com."]

# Título dinámico según el nivel
tipo_analisis = "Trayectoria" if nivel_edu == "Preescolar" else "Análisis"

cols_campos = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols_campos[i % 2]:
        eval_campos[campo] = st.text_area(f"{tipo_analisis} en {campo}:", 
                                        height=150, 
                                        placeholder="Esperando datos de bitácoras diarias...",
                                        key=f"ia_{campo}")

# --- INDICADORES ---
st.divider()
col_ind1, col_ind2 = st.columns(2)
indicador_lectura = col_ind1.text_input("📖 Indicador de Lectura (12A, 1B, etc.)", "12A")
indicador_escritura = col_ind2.text_input("✍️ Indicador de Escritura (6, etc.)", "6")

# --- CALIFICACIONES (PRIMARIA Y SECUNDARIA) ---
eval_detalles = []
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader(f"🔢 Calificaciones y Claves ({nivel_edu})")
    
    # Primaria usa campos formativos, Secundaria usa materias
    items_lista = campos_nombres if nivel_edu == "Primaria" else ["Español", "Matemáticas", "Ciencias", "Historia", "Geografía", "F. Cívica y Ética"]
    
    for item in items_lista:
        c1, c2 = st.columns([2, 1])
        nota = c1.number_input(f"Nota: {item}", 5, 10, 8, key=f"n_{item}")
        clave = c2.text_input(f"Clave (Máx T120)", "T", max_chars=4, key=f"c_{item}")
        eval_detalles.append({"concepto": item, "nota": nota, "clave": clave})

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GENERAR REPORTE EVALUATIVO", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Indica el nombre del alumno.")
    else:
        pdf = EvaluacionPDF()
        pdf.add_page()
        pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

        # Indicadores de Lecto-Escritura
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(95, 8, clean(f"INDICADOR LECTURA: {indicador_lectura}"), 1, 0, 'L', True)
        pdf.cell(95, 8, clean(f"INDICADOR ESCRITURA: {indicador_escritura}"), 1, 1, 'L', True)
        pdf.ln(5)

        # Sección de Análisis (Alimentada por IA)
        titulo_seccion = "TRAYECTORIAS (DESCRIPTIVO)" if nivel_edu == "Preescolar" else "ANALISIS CUALITATIVO (IA)"
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_fill_color(0, 51, 102); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, clean(f" {titulo_seccion}"), 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

        for campo, texto in eval_campos.items():
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
            pdf.set_font('Helvetica', '', 9)
            # Texto por defecto si la IA aún no ha procesado nada
            txt_mostrar = texto if texto else "Informacion en proceso de analisis desde bitacoras diarias..."
            pdf.multi_cell(0, 5, clean(txt_mostrar))
            pdf.ln(2)

        # Tabla de Notas Numéricas
        if nivel_edu != "Preescolar":
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 10); pdf.set_fill_color(200, 200, 200)
            pdf.cell(100, 10, clean(" ASIGNATURA / CAMPO"), 1, 0, 'C', True)
            pdf.cell(45, 10, clean(" CALIFICACION"), 1, 0, 'C', True)
            pdf.cell(45, 10, clean(" CLAVE"), 1, 1, 'C', True)
            pdf.set_font('Helvetica',
