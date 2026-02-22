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
    nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Ej. Juan Perez")
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
    st.info("💡 En Preescolar, describe manualmente los avances en cada campo.")
    ph = "Escribe aquí la trayectoria observada..."
else:
    st.subheader("🤖 Análisis Cualitativo por Campo Formativo (IA-Ready)")
    st.info("💡 Este espacio será llenado por la IA basándose en tus bitácoras diarias.")
    ph = "La IA generará este texto automáticamente..."

cols = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols[i % 2]:
        eval_campos[campo] = st.text_area(f"Trayectoria/Análisis en {campo}:", 
                                        height=120, key=f"eval_{campo}", 
                                        placeholder=ph)

# --- INDICADORES ---
st.divider()
st.subheader("📖 Indicadores de Logro")
c_ind1, c_ind2 = st.columns(2)
ind_lectura = c_ind1.text_input("Indicador de Lectura (ej. 12A)", "12A")
ind_escritura = c_ind2.text_input("Indicador de Escritura (ej. 6)", "6")

# --- CALIFICACIONES (PRIMARIA / SECUNDARIA) ---
eval_detalles = []
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader(f"🔢 Calificaciones y Claves ({nivel_edu})")
    items = campos_nombres if nivel_edu == "Primaria" else ["Español", "Matematicas", "Ciencias", "Historia", "Geografia", "F. Civica y Etica"]
    for item in items:
        c1, c2 = st.columns([2, 1])
        nota = c1.number_input(f"Nota: {item}", 5, 10, 8, key=f"n_{item}")
        clave = c2.text_input(f"Clave (ej. T120)", "T", max_chars=5, key=f"c_{item}")
        eval_detalles.append({"concepto": item, "nota": nota, "clave": clave})

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GENERAR REPORTE DE EVALUACIÓN", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Por favor, ingresa el nombre del alumno.")
    else:
        try:
            pdf = EvaluacionPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

            # Indicadores
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(95, 8, clean(f"INDICADOR LECTURA: {ind_lectura}"), 1, 0, 'L')
            pdf.cell(95, 8, clean(f"INDICADOR ESCRITURA: {ind_escritura}"), 1, 1, 'L')
            pdf.ln(5)

            # Contenido Cualitativo
            titulo = "TRAYECTORIAS (PREESCOLAR)" if nivel_edu == "Preescolar" else "ANALISIS CUALITATIVO (IA)"
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(0, 51, 102); pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, clean(f" {titulo}"), 0, 1, 'L', True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

            for campo, texto in eval_campos.items():
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
                pdf.set_font('Helvetica', '', 9)
                pdf.multi_cell(0, 5, clean(texto if texto else "Informacion no registrada."))
                pdf.ln(2)

            # Tabla de Notas
            if nivel_edu != "Preescolar":
                pdf.ln(5)
                pdf.set_font('Helvetica', 'B', 10); pdf.set_fill_color(200, 200, 200)
                pdf.cell(90, 10, clean(" ASIGNATURA"), 1, 0, 'C', True)
                pdf.cell(50, 10, clean(" NOTA"), 1, 0, 'C', True)
                pdf.cell(50, 10, clean(" CLAVE"), 1, 1, 'C', True)
                pdf.set_font('Helvetica', '', 10)
                for it in eval_detalles:
                    pdf.cell(90, 10, clean(f" {it['concepto']}"), 1, 0, 'L')
                    pdf.cell(50, 10, str(it['nota']), 1, 0, 'C')
                    pdf.cell(50, 10, clean(it['clave']), 1, 1, 'C')

            # Fotos
            if fotos:
                pdf.add_page()
                for i, f in enumerate(fotos[:2]):
                    pdf.image(io.BytesIO(f.getvalue()), x=(10 if i==0 else 110), y=30, w=90)

            # Firmas
            pdf.set_y(-30)
            pdf.set_font('Helvetica', 'B', 8)
            pdf.cell(95, 5, clean("__________________________"), 0, 0, 'C')
            pdf.cell(95, 5, clean("__________________________"), 0, 1, 'C')
            pdf.cell(95, 5, clean("FIRMA DEL EC"), 0, 0, 'C')
            pdf.cell(95, 5, clean("FIRMA PADRE / APEC"), 0, 1, 'C')

            st.download_button("📥 DESCARGAR REPORTE", bytes(pdf.output()), f"Reporte_{nombre_alumno}.pdf", "application/pdf")
            st.success(f"✅ Reporte de {nombre_alumno} listo.")
        except Exception as e:
            st.error(f"Error al generar el PDF: {e}")
