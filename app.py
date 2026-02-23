import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILOS (Fases 0.1, 0.2, 0.3) ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

# Inicialización de estados para evitar que salga la ayuda de Streamlit
if "step" not in st.session_state:
    st.session_state.step = "login"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { font-size: 3rem; font-weight: 800; color: #38bdf8; text-shadow: 0 0 15px rgba(56,189,248,0.5); text-align: center; }
    .apple-container { font-size: 100px; text-align: center; position: relative; margin-top: 20px; }
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px); opacity: 0; }
        50% { transform: translate(0px, -50px); opacity: 1; }
    }
    .worm-icon { position: absolute; font-size: 40px; animation: worm-move 3s infinite ease-in-out; }
    /* Botón Rojo Cerrar Sesión */
    .stButton>button[kind="secondary"] { background-color: #ef4444 !important; color: white !important; border: none !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES PDF (Fases 0.4 - 0.7) ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ProfeEducaPDF(FPDF):
    def header_institucional(self, titulo):
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(10)

# --- 3. LÓGICA DE NAVEGACIÓN ---

if st.session_state.step == "login":
    st.markdown("<h1 style='text-align: center;'>🍎 ACCESO PROFEEDUCA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("Usuario Docente")
        password = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
            st.session_state.user_data = {"name": user}
            st.session_state.step = "dashboard"
            st.rerun()

elif st.session_state.step == "dashboard":
    # Sidebar con Botón de Cerrar Sesión
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_data.get('name', 'Docente')}")
        if st.button("📝 Planeación", use_container_width=True): st.session_state.step = "planeacion"; st.rerun()
        if st.button("📊 Evaluación", use_container_width=True): st.session_state.step = "evaluacion"; st.rerun()
        st.markdown("---")
        if st.button("🔒 CERRAR SESIÓN", type="secondary"):
            st.session_state.step = "login"
            st.rerun()

    st.markdown('<div class="brand-header">📏 ProfeEduca ✏️</div>', unsafe_allow_html=True)
    st.markdown('<div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>', unsafe_allow_html=True)
    st.write("Bienvenido al panel principal. Selecciona una opción en el menú lateral.")

# Módulos de trabajo (Fases 0.5 y 0.7)
elif st.session_state.step == "planeacion":
    st.title("📝 Planeación Semanal")
    if st.button("⬅️ Volver"): st.session_state.step = "dashboard"; st.rerun()
    # Aquí iría el formulario de la fase 0.5...
    st.info("Formulario de planeación activo.")

elif st.session_state.step == "evaluacion":
    st.title("📊 Evaluación Trimestral")
    if st.button("⬅️ Volver"): st.session_state.step = "dashboard"; st.rerun()
    # Aquí iría el formulario de la fase 0.7...
    st.info("Formulario de evaluación activo.")
