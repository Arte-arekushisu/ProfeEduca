import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTADO DE SESIÓN ---
st.set_page_config(page_title="PROFEEDUCA - Sistema Integral", layout="wide", page_icon="🍎")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = True

# --- 2. FUNCIONES DE UTILIDAD Y CLASE PDF ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'replace').decode('latin-1')

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

# --- 3. ESTILOS VISUALES PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    div[data-testid="stExpander"] { border: 2px solid #FF4B4B !important; background-color: #1e293b; border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    .stButton>button[kind="secondary"] { background-color: #ef4444; color: white; border: none; }
    .stButton>button[kind="secondary"]:hover { background-color: #b91c1c; }
    </style>
""", unsafe_allow_html=True)

# Lógica de seguridad
if not st.session_state.autenticado:
    st.warning("⚠️ Sesión cerrada. Por favor, recarga la página para ingresar.")
    st.stop()

# --- 4. BARRA LATERAL (DATOS MAESTROS, SOS Y LOGOUT) ---
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
            st.info("La IA requiere textos detallados para generar mejores análisis.")
        st.link_button("📲 Soporte Directo", "https://wa.me/tu_numero", use_container_width=True)
    
    st.markdown("<br>"*3, unsafe_allow_html=True)
    if st.button("🔒 CERRAR SESIÓN", use_container_width=True, type="secondary"):
        st.session_state.autenticado = False
        st.toast("Cerrando sesión...")
        time.sleep(1.2)
        st.rerun()

# --- 5. CUERPO PRINCIPAL: TABS DE TRABAJO ---
t1, t2, t3, t4 = st.tabs(["👤 Escrito Reflexivo", "🗓️ Planeación", "📊 Evaluación", "🧾 Facturación"])

# --- TAB 1: ESCRITO REFLEXIVO ---
with t1:
    st.subheader("📝 Seguimiento Individual del Alumno")
    c1, c2 = st.columns(2)
    alumno_ref = c1.text_input("Nombre del Alumno", key="ref_n")
    trimestre_ref = c2.selectbox("Trimestre", ["1ero", "2do", "3ero"], key="ref_t")
    q_hizo = st.text_area("¿Qué hizo el alumno hoy?")
    c_hizo = st.text_area("¿Cómo realizó las actividades?")
    
    if st.button("💾 GENERAR ESCRITO PDF"):
        if alumno_ref and q_hizo:
            pdf = ProfeEducaPDF()
            pdf.add_page()
            pdf.header_institucional("ESCRITO REFLEXIVO")
            pdf.tabla_identificacion({"ALUMNO": alumno_ref, "TRIMESTRE": trimestre_ref, "EC": nombre_ec, "COMUNIDAD": comunidad})
            
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, clean("1. ACTIVIDADES REALIZADAS"), 0, 1)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, clean(q_hizo))
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, clean("2. DESEMPEÑO Y PROCESO"), 0, 1)
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 6, clean(c_hizo))
            
            st.download_button("📥 Descargar Escrito", data=bytes(pdf.output()), file_name=f"Escrito_{alumno_ref}.pdf")
        else:
            st.error("Completa el nombre y la descripción.")

# --- TAB 2: PLANEACIÓN ---
with t2:
    st.subheader("🗓️ Planeación Semanal ABCD")
    fecha_p = st.date_input("Semana del:", datetime.date.today())
    dia_p = st.selectbox("Día", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
    act_p = st.text_area(f"Actividades planeadas para el {dia_p}")
    if st.button("🔨 CREAR PLANEACIÓN"):
        st.success(f"Planeación para el {dia_p} registrada correctamente.")

# --- TAB 3: EVALUACIÓN ---
with t3:
    st.subheader("📉 Reporte Trimestral")
    alumno_ev = st.text_input("Alumno a evaluar", key="ev_n")
    campos = ["Lenguajes", "Saberes y P.C.", "Ética, N. y S.", "De lo Humano y lo Com."]
    c_ev = st.columns(2)
    for i, campo in enumerate(campos):
        c_ev[i%2].text_area(f"Análisis: {campo}", key=f"eval_{i}")
    
    if st.button("🚀 GENERAR REPORTE"):
        pdf = ProfeEducaPDF()
        pdf.add_page()
        pdf.header_institucional("REPORTE DE EVALUACIÓN", (0, 51, 102))
        pdf.tabla_identificacion({"ALUMNO": alumno_ev, "NIVEL": nivel_edu, "EC": nombre_ec})
        st.download_button("📥 Descargar Reporte", data=bytes(pdf.output()), file_name="Evaluacion.pdf")

# --- TAB 4: FACTURACIÓN ---
with t4:
    st.subheader("🧾 Gestión de Comprobantes")
    cf1, cf2 = st.columns(2)
    razon = cf1.text_input("Razón Social")
    monto = cf2.number_input("Monto ($)", min_value=0.0)
    if st.button("📝 EMITIR COMPROBANTE"):
        if monto > 0:
            pdf = ProfeEducaPDF()
            pdf.add_page()
            pdf.header_institucional("COMPROBANTE DE PAGO", (33, 47, 61))
            pdf.tabla_identificacion({"RECEPTOR": razon, "MONTO": f"${monto}", "FECHA": str(datetime.date.today())})
            st.download_button("📥 Descargar Recibo", data=bytes(pdf.output()), file_name="Factura.pdf")
            st.balloons()
