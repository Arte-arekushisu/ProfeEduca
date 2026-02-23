import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="PROFEEDUCA - Sistema Integral", layout="wide", page_icon="🍎")

# Inicializar estado de sesión para el login (Simulado para esta fase)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = True

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'replace').decode('latin-1')

# --- 2. CLASE PDF UNIFICADA ---
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

# --- 3. ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    div[data-testid="stExpander"] { border: 2px solid #FF4B4B !important; background-color: #1e293b; border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    /* Estilo específico para el botón de cerrar sesión */
    .stButton>button[kind="secondary"] { background-color: #ef4444; color: white; border: none; }
    .stButton>button[kind="secondary"]:hover { background-color: #b91c1c; }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE CONTROL DE ACCESO ---
if not st.session_state.autenticado:
    st.warning("Sesión cerrada. Por favor, recarga la página para ingresar de nuevo.")
    st.stop()

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
    
    st.markdown("<br>"*5, unsafe_allow_html=True) # Espaciador para empujar el botón abajo
    
    # --- BOTÓN DE CERRAR SESIÓN ---
    if st.button("🔒 CERRAR SESIÓN", use_container_width=True, type="secondary"):
        st.session_state.autenticado = False
        st.toast("Cerrando sesión de forma segura...")
        time.sleep(1.5)
        st.rerun()

# --- 5. CUERPO PRINCIPAL (NAVEGACIÓN POR TABS) ---
t1, t2, t3, t4 = st.tabs(["👤 Escrito Reflexivo", "🗓️ Planeación", "📊 Evaluación", "🧾 Facturación"])

# [El contenido de las pestañas t1, t2, t3 y t4 se mantiene igual al anterior]
# --- TAB 1: ESCRITO REFLEXIVO ---
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

# (Resto de pestañas omitidas en este bloque para brevedad, pero integradas en el flujo completo)
