import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS ---
st.set_page_config(page_title="PROFEEDUCA - Sistema Integral", layout="wide", page_icon="🍎")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'replace').decode('latin-1')

# --- 2. CLASES PARA GENERACIÓN DE PDF ---
class MaestroPDF(FPDF):
    def header_style(self, titulo, color_rgb=(128, 0, 0)):
        self.set_fill_color(*color_rgb)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(5)

    def tabla_identificacion(self, datos):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        for label, valor in datos.items():
            self.cell(95, 8, clean(f" {label}: {valor}"), 1, 0, 'L', True)
            if list(datos.keys()).index(label) % 2 != 0: self.ln(8)
        self.ln(5)

# --- 3. INTERFAZ Y ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    div[data-testid="stExpander"] { border: 2px solid #FF4B4B !important; background-color: #1e293b; border-radius: 10px; }
    .main-header { color: #38bdf8; font-size: 2.5rem; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 4. BARRA LATERAL (IDENTIDAD Y SOS) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🍎 PROFEEDUCA</h1>", unsafe_allow_html=True)
    nombre_ec = st.text_input("Educador Comunitario", "AXEL REYES")
    comunidad = st.text_input("Comunidad", "CRUZ")
    nivel_edu = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
    
    st.divider()
    st.markdown("### 🆘 CENTRO DE AYUDA")
    with st.expander("🚨 BOTÓN SOS", expanded=False):
        st.error("¿Necesitas asistencia?")
        st.info("Tip: Si el PDF marca error, verifica que no usaste emojis o símbolos raros en los textos.")
        st.link_button("📲 Soporte WhatsApp", "https://wa.me/tu_numero")

# --- 5. NAVEGACIÓN POR PESTAÑAS (TABS) ---
tabs = st.tabs(["📝 Escritos Reflexivos", "📅 Planeación", "📊 Evaluación", "🧾 Facturación"])

# --- TAB: ESCRITOS REFLEXIVOS ---
with tabs[0]:
    st.subheader("👤 Registro de Reflexión Individual")
    col1, col2 = st.columns(2)
    alumno_ref = col1.text_input("Nombre del Alumno", key="ref_nom")
    trimestre_ref = col2.selectbox("Trimestre", ["1ro", "2do", "3ro"], key="ref_tri")
    
    que_hizo = st.text_area("¿Qué hizo el alumno hoy?")
    como_hizo = st.text_area("¿Cómo realizó las actividades?")
    
    if st.button("💾 Generar Escrito PDF"):
        pdf = MaestroPDF()
        pdf.add_page()
        pdf.header_style("ESCRITO REFLEXIVO")
        pdf.tabla_identificacion({"ALUMNO": alumno_ref, "TRIMESTRE": trimestre_ref, "EC": nombre_ec, "COMUNIDAD": comunidad})
        pdf.set_font('Helvetica', 'B', 12); pdf.cell(0, 10, "1. ACTIVIDADES", 0, 1)
        pdf.set_font('Helvetica', '', 11); pdf.multi_cell(0, 6, clean(que_hizo))
        st.download_button("📥 Descargar Escrito", data=bytes(pdf.output()), file_name="Escrito.pdf")

# --- TAB: PLANEACIÓN SEMANAL ---
with tabs[1]:
    st.subheader("🗓️ Planeación Semanal ABCD")
    fecha_plan = st.date_input("Semana del:", datetime.date.today())
    # Estructura simplificada basada en Fase 0.5
    dia_plan = st.selectbox("Día a planear", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
    actividad_plan = st.text_area(f"Actividades para el {dia_plan}")
    
    if st.button("🔨 Crear Planeación"):
        st.success("Planeación generada (Módulo unificado)")

# --- TAB: EVALUACIÓN TRIMESTRAL ---
with tabs[2]:
    st.subheader("📉 Reporte de Evaluación")
    alumno_ev = st.text_input("Nombre del Alumno", key="ev_nom")
    
    campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
    eval_textos = {}
    cols_ev = st.columns(2)
    for i, campo in enumerate(campos):
        eval_textos[campo] = cols_ev[i%2].text_area(f"Análisis {campo}")

    if st.button("🚀 Generar Evaluación"):
        pdf = MaestroPDF()
        pdf.add_page()
        pdf.header_style("REPORTE TRIMESTRAL", (0, 51, 102))
        pdf.tabla_identificacion({"ALUMNO": alumno_ev, "NIVEL": nivel_edu, "EC": nombre_ec})
        st.download_button("📥 Descargar Evaluación", data=bytes(pdf.output()), file_name="Evaluacion.pdf")

# --- TAB: FACTURACIÓN ---
with tabs[3]:
    st.subheader("🧾 Comprobantes de Pago")
    col_f1, col_f2 = st.columns(2)
    razon = col_f1.text_input("Razón Social / Nombre")
    monto = col_f2.number_input("Monto ($)", min_value=0.0)
    
    if st.button("📝 Emitir Comprobante"):
        if monto > 0:
            pdf = MaestroPDF()
            pdf.add_page()
            pdf.header_style("COMPROBANTE DE PAGO", (33, 47, 61))
            pdf.tabla_identificacion({"RECEPTOR": razon, "MONTO": f"${monto}", "FECHA": str(datetime.date.today())})
            st.download_button("📥 Descargar Factura", data=bytes(pdf.output()), file_name="Factura.pdf")
            st.balloons()
