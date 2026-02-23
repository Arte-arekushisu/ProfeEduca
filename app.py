import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time
from PIL import Image
import base64

# --- 1. CONFIGURACIÓN Y ESTILOS (Fase 0.1 & 0.3) ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral ABCD", page_icon="🍎", layout="wide")

# Inicialización del sistema de estados
if "step" not in st.session_state:
    st.session_state.step = "login"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

def get_base64(file_path):
    # Función auxiliar para manejo de imágenes si fuera necesario
    return ""

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Tarjetas Empresariales Fase 0.1 */
    .plan-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }
    
    /* Animación Gusanito Fase 0.2/0.3 */
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
    }
    .apple-container { font-size: 100px; text-align: center; position: relative; margin-top: 20px; }
    .worm-icon { position: absolute; font-size: 40px; animation: worm-move 3s infinite ease-in-out; }
    
    .brand-header { font-size: 3rem; font-weight: 800; color: #38bdf8; text-shadow: 0 0 15px rgba(56,189,248,0.5); }
    
    /* Botón Rojo Cerrar Sesión */
    .stButton>button[kind="secondary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE PDF INTEGRADO (Fase 0.4 - 0.7) ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ProfeEducaPDF(FPDF):
    def header_institucional(self, titulo, sub_color=(128, 0, 0)):
        self.set_fill_color(*sub_color)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(10)

    def tabla_datos(self, datos_dict):
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 9)
        for label, valor in datos_dict.items():
            self.cell(40, 7, clean(f" {label}:"), 1, 0, 'L', True)
            self.set_font('Helvetica', '', 9)
            self.cell(150, 7, clean(f" {valor}"), 1, 1, 'L')
        self.ln(5)

# --- 3. LÓGICA DE NAVEGACIÓN POR FASES ---

# --- FASE 0.1: LOGIN Y SELECCIÓN DE PLAN ---
if st.session_state.step == "login":
    st.markdown("<h1 style='text-align: center;'>🍎 BIENVENIDO A PROFEEDUCA</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            st.markdown("### Acceso Docente")
            user = st.text_input("Usuario (EC/ECA)")
            contra = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR AL SISTEMA", use_container_width=True):
                if user and contra:
                    st.session_state.user_data = {"name": user, "comunidad": "General"}
                    st
