import streamlit as st
from fpdf import FPDF
import unicodedata
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.7", layout="wide", page_icon="📊")

# --- FUNCIONES DE UTILIDAD ---
def clean(txt):
    if not txt: return ""
    # Elimina acentos y caracteres especiales para evitar errores en el PDF
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

# --- ESTILOS PERSONALIZADOS (SOS) ---
st.markdown("""
    <style>
    div[data-testid="stExpander"] {
        border: 2px solid #FF4B4B !important;
        border-radius: 10px;
        background-color: #FFF5F5;
    }
    .stButton>button {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INTERFAZ - BARRA LATERAL ---
with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Ej. Juan Perez")
    comunidad = st.text_input("Comunidad", "CRUZ")
    trimestre = st.selectbox("Trimestre", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado/Fase", ["1", "2", "3", "4", "5", "6"])
    
    st.divider()
    st.header("📸 Evidencias")
    fotos = st.file_uploader("Subir imágenes (Máx. 2)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # --- FASE 0.7: CENTRO DE AYUDA SOS ---
    st.divider()
    st.markdown("### 🆘 CENTRO DE AYUDA")
    with st.expander("🚨 BOTÓN SOS / SOPORTE", expanded=False):
        st.error("¿Tienes problemas?")
        if st.button("🤖 Ayuda con la IA", use_container_width=True):
            st.info("La IA analiza tus bitácoras. Si no aparece texto, revisa que tus escritos diarios sean detallados.")
        if st.button("⚙️ Error al descargar", use_container_width=True):
            st.warning("Evita usar acentos en el nombre del alumno. Si el error persiste, recarga la página (F5).")
        st.divider()
        st.link_button("📲 Contactar Soporte", "https://wa.me/tu_numero", use_container_width=True)

# --- INTERFAZ - CUERPO PRINCIPAL ---
st.title("📊 PROFEEDUCA: Sistema de Evaluación")

# SECCIÓN DE ANÁLISIS / TRAYECTORIAS
eval_campos = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]

if nivel_edu == "Preescolar":
    st.subheader("🖋️ Trayectorias Personalizadas (Manual)")
    st.info("Desarrolla el progreso del alumno por campo formativo.")
    ph = "Escribe la trayectoria aquí..."
else:
    st.subheader("🤖 Análisis por Campo (IA-Ready)")
    st.info("Este apartado se autocompletará con el análisis de Gemini.")
    ph = "Esperando análisis de la IA..."

cols = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols[i % 2]:
        eval_campos[campo] = st.text_area(f"{campo}:", height=150, key=f"eval_{campo}", placeholder=ph)

# INDICADORES DE LECTO-ESCRITURA
st.divider()
st.subheader("📖 Indicadores de Logro")
c1, c2 = st.columns(2)
ind_lectura = c1.text_input("Indicador Lectura", "12A")
ind_escritura = c2.text_input("Indicador Escritura", "6")

# CALIFICACIONES DINÁMICAS (Solo Primaria y Secundaria)
eval_detalles = []
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader(f"🔢 Calificaciones ({nivel_edu})")
    
    if nivel_edu == "Primaria":
        lista_materias = campos_nombres
    else: # Secundaria por Grado
        base = ["Espanol", "Matematicas", "Historia", "Geografia", "Artes", "Ed. Fisica"]
        if grado_edu == "1": lista_materias = ["Biologia"] + base
        elif grado_edu == "2": lista_materias = ["Fisica"] + base
        else: lista_materias = ["Quimica"] + base

    for mat in lista_materias:
        col1, col2 = st.columns([2, 1])
        nota = col1.number_input(f"Nota: {mat}", 5, 10, 8, key=f"n_{mat}")
        clave = col2.text_input(f"Clave", "T", max_chars=5, key=f"c_{mat}")
        eval_detalles.append({"concepto": mat, "nota": nota, "clave": clave})

# --- GENERACIÓN DEL PDF FINAL ---
st.divider()
if st.button("🚀 GENERAR Y DESCARGAR REPORTE FINAL", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Falta el nombre del alumno.")
    else:
        try:
            pdf = EvaluacionPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

            # Bloque Indicadores
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(95, 8, clean(f"IND. LECTURA: {ind_lectura}"), 1, 0, 'L')
            pdf.cell(95, 8, clean(f"IND. ESCRITURA: {ind_escritura}"), 1, 1, 'L')
            pdf.ln(5)

            # Bloque Cualitativo
            titulo_c = "TRAYECTORIAS" if nivel_edu == "Preescolar" else "ANALISIS CUALITATIVO (IA)"
            pdf.set_font('Helvetica', 'B', 12); pdf.set_fill_color(0, 51, 102); pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 10, clean(f" {titulo_c}"), 0, 1, 'L', True)
            pdf.set_text_color(0, 0, 0); pdf.ln(2)

            for campo, texto in eval_campos.items():
                pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
                pdf.set_font('Helvetica', '', 9)
                pdf.multi_cell(0, 5, clean(texto if texto else "Dato no registrado."))
                pdf.ln(2)

            # Tabla de Notas
            if nivel_edu != "Preescolar":
                pdf.ln(5); pdf.set_font('Helvetica', 'B', 10); pdf.set_fill_color(200, 200, 200)
                pdf.cell(90, 10, clean(" ASIGNATURA"), 1, 0, 'C', True)
                pdf.cell(50, 10, clean(" NOTA"), 1, 0, 'C', True)
                pdf.cell(50, 10, clean(" CLAVE"), 1, 1, 'C', True)
                pdf.set_font('Helvetica', '', 10)
                for it in eval_detalles:
                    pdf.cell(90, 10, clean(f" {it['concepto']}"), 1, 0, 'L')
                    pdf.cell(50, 10, str(it['nota']), 1, 0, 'C')
                    pdf.cell(50, 10, clean(it['clave']), 1, 1, 'C')

            # Manejo de Fotos
            if fotos:
                pdf.add_page()
                for i, f in enumerate(fotos[:2]):
                    pdf.image(io.BytesIO(f.getvalue()), x=(10 if i==0 else 110), y=30, w=90)

            # Firmas
            pdf.set_y(-30); pdf.set_font('Helvetica', 'B', 8)
            pdf.cell(95, 5, "__________________________", 0, 0, 'C')
            pdf.cell(95, 5, "__________________________", 0, 1, 'C')
            pdf.cell(95, 5, "FIRMA DEL EC", 0, 0, 'C')
            pdf.cell(95, 5, "FIRMA PADRE / APEC", 0, 1, 'C')

            st.download_button("📥 DESCARGAR REPORTE PDF", bytes(pdf.output()), f"Reporte_{nombre_alumno}.pdf", "application/pdf")
            st.success("✅ ¡Reporte generado con éxito!")
        except Exception as e:
            st.error(f"Error crítico: {e}")
