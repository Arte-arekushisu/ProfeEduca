import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="PROFEEDUCA - Sistema Integral", layout="wide", page_icon="🍎")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'replace').decode('latin-1')

# --- 2. CLASE PDF UNIFICADA (Para todos los documentos) ---
class ProfeEducaPDF(FPDF):
    def header_institucional(self, titulo, color_rgb=(128, 0, 0)):
        self.set_fill_color(*color_rgb)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(5)

    def tabla_identificacion(self, dict_datos):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        for i, (label, valor) in enumerate(dict_datos.items()):
            self.cell(95, 8, clean(f" {label}: {valor}"), 1, (i % 2), 'L', True)
        self.ln(10)

# --- 3. ESTILOS VISUALES (Basados en Fase 0.1 y 0.2) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    div[data-testid="stExpander"] { border: 2px solid #FF4B4B !important; background-color: #1e293b; border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    </style>
""", unsafe_allow_html=True)

# --- 4. BARRA LATERAL (DATOS MAESTROS Y SOS) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🍎 PROFEEDUCA</h1>", unsafe_allow_html=True)
    nombre_ec = st.text_input("Educador Comunitario", "AXEL REYES")
    comunidad = st.text_input("Comunidad", "CRUZ")
    nivel_edu = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
    
    st.divider()
    st.markdown("### 🆘 CENTRO DE AYUDA")
    with st.expander("🚨 BOTÓN SOS", expanded=False):
        st.error("¿Algo no funciona?")
        if st.button("🤖 Ayuda IA", use_container_width=True):
            st.info("La IA requiere textos detallados en las bitácoras para generar el análisis.")
        st.link_button("📲 Soporte Directo", "https://wa.me/tu_numero", use_container_width=True)

# --- 5. CUERPO PRINCIPAL (NAVEGACIÓN POR TABS) ---
t1, t2, t3, t4 = st.tabs(["👤 Escrito Reflexivo", "🗓️ Planeación", "📊 Evaluación", "🧾 Facturación"])

# --- TAB 1: ESCRITO REFLEXIVO (Fase 0.4) ---
with t1:
    st.subheader("📝 Seguimiento Individual del Alumno")
    col1, col2 = st.columns(2)
    alumno_ref = col1.text_input("Nombre del Alumno", key="ref_n")
    trimestre_ref = col2.selectbox("Trimestre", ["1ero", "2do", "3ero"], key="ref_t")
    
    q_hizo = st.text_area("¿Qué hizo el alumno hoy?")
    c_hizo = st.text_area("¿Cómo realizó las actividades?")
    
    if st.button("💾 GENERAR ESCRITO PDF"):
        pdf = ProfeEducaPDF()
        pdf.add_page()
        pdf.header_institucional("ESCRITO REFLEXIVO")
        pdf.tabla_identificacion({"ALUMNO": alumno_ref, "TRIMESTRE": trimestre_ref, "EC": nombre_ec, "COMUNIDAD": comunidad})
        st.download_button("📥 Descargar", data=bytes(pdf.output()), file_name="Escrito.pdf")

# --- TAB 2: PLANEACIÓN (Fase 0.5) ---
with t2:
    st.subheader("🗓️ Planeación Semanal ABCD")
    fecha_p = st.date_input("Semana del:", datetime.date.today())
    dia_p = st.selectbox("Día", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
    actividades_p = st.text_area(f"Actividades para el {dia_p}")
    
    if st.button("🔨 CREAR PLANEACIÓN"):
        st.success("Módulo de planeación activado.")

# --- TAB 3: EVALUACIÓN (Fase 0.6 / 0.7) ---
with t3:
    st.subheader("📉 Reporte de Evaluación Trimestral")
    alumno_ev = st.text_input("Alumno a evaluar", key="ev_n")
    
    campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
    eval_textos = {}
    c_ev = st.columns(2)
    for i, campo in enumerate(campos):
        eval_textos[campo] = c_ev[i%2].text_area(f"Análisis {campo}")

    if st.button("🚀 GENERAR REPORTE TRIMESTRAL"):
        pdf = ProfeEducaPDF()
        pdf.add_page()
        pdf.header_institucional("REPORTE DE EVALUACION", (0, 51, 102))
        pdf.tabla_identificacion({"ALUMNO": alumno_ev, "NIVEL": nivel_edu, "EC": nombre_ec})
        st.download_button("📥 Descargar Reporte", data=bytes(pdf.output()), file_name="Evaluacion.pdf")

# --- TAB 4: FACTURACIÓN (Fase 0.7 / 0.8) ---
with t4:
    st.subheader("🧾 Gestión Administrativa")
    col_f1, col_f2 = st.columns(2)
    razon_f = col_f1.text_input("Razón Social")
    monto_f = col_f2.number_input("Monto total ($)", min_value=0.0)
    
    if st.button("📝 EMITIR COMPROBANTE"):
        if monto_f > 0:
            pdf = ProfeEducaPDF()
            pdf.add_page()
            pdf.header_institucional("COMPROBANTE DE PAGO", (33, 47, 61))
            pdf.tabla_identificacion({"RECEPTOR": razon_f, "MONTO": f"${monto_f}", "FECHA": str(datetime.date.today())})
            st.download_button("📥 Descargar Recibo", data=bytes(pdf.output()), file_name="Factura.pdf")
            st.balloons()
