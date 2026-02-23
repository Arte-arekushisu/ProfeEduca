import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time
from PIL import Image
import base64

# --- 1. CONFIGURACIÓN E IDENTIDAD VISUAL (Fase 0.1 y 0.2) ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

def get_base64(file_path):
    # Función para manejar imágenes en el CSS
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
        .plan-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.15);
            border-radius: 20px; padding: 25px; text-align: center;
            transition: all 0.3s ease;
        }
        .apple-container {
            font-size: 100px; position: relative; display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes worm-move {
            0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
            50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
        }
        .worm-icon { position: absolute; font-size: 40px; animation: worm-move 4s infinite; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE UTILIDADES Y PDF (Fase 0.4, 0.5, 0.7) ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class MasterPDF(FPDF):
    def header_custom(self, title, color=(128, 0, 0)):
        self.set_fill_color(*color)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(title), 0, 1, 'C')
        self.ln(5)

# --- 3. GESTIÓN DE ESTADO (Logica de Negocio Mensual) ---
if "db" not in st.session_state:
    st.session_state.db = {"step": "login", "user": None, "plan": None}

apply_styles()

# --- 4. FLUJO DE NAVEGACIÓN ---

# A. LOGIN Y REGISTRO (Fase 0.1)
if st.session_state.db["step"] == "login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
        with st.container():
            u = st.text_input("Correo Electrónico")
            p = st.text_input("Contraseña", type="password")
            if st.button("Iniciar Sesión / Registrarse", use_container_width=True):
                st.session_state.db["step"] = "plan"
                st.rerun()

# B. SELECCIÓN DE PLAN MENSUAL (Fase 0.1)
elif st.session_state.db["step"] == "plan":
    st.markdown("<h2 style='text-align:center;'>Selecciona tu suscripción mensual</h2>", unsafe_allow_html=True)
    cols = st.columns(3)
    planes = {
        "Básico": {"p": "$99/mes", "desc": "Ideal para 1 grupo"},
        "Pro": {"p": "$199/mes", "desc": "Multigrado y Reportes"},
        "Premium": {"p": "$299/mes", "desc": "Todo ilimitado + IA"}
    }
    for i, (nombre, info) in enumerate(planes.items()):
        with cols[i]:
            st.markdown(f"<div class='plan-card'><h3>{nombre}</h3><h1>{info['p']}</h1><p>{info['desc']}</p></div>", unsafe_allow_html=True)
            if st.button(f"Elegir {nombre}", key=nombre):
                st.session_state.db["plan"] = nombre
                st.session_state.db["step"] = "app"
                st.rerun()

# C. APP PRINCIPAL (Fase 0.2 a 0.7)
elif st.session_state.db["step"] == "app":
    # Sidebar Profesional
    with st.sidebar:
        st.markdown("### 🍎 Panel Maestro")
        opcion = st.radio("Herramientas:", ["🏠 Inicio", "📝 Planeación", "👤 Escritos", "📊 Evaluación"])
        if st.button("Cerrar Sesión"):
            st.session_state.db["step"] = "login"
            st.rerun()

    # Contenedor Dinámico
    if opcion == "🏠 Inicio":
        col_t, col_v = st.columns([2,1])
        with col_v:
            st.markdown('<div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>', unsafe_allow_html=True)
        with col_t:
            st.title("Bienvenido a ProfeEduca")
            st.info(f"Suscripción activa: Plan {st.session_state.db['plan']}")

    elif opcion == "📝 Planeación":
        # Aquí se integra fase0.5.py íntegro
        st.header("Planeación Semanal ABCD")
        with st.form("f_plan"):
            nombre_ec = st.text_input("Nombre del EC")
            fecha = st.date_input("Semana del:")
            if st.form_submit_button("Generar PDF"):
                st.success("Generando planeación...")

    elif opcion == "👤 Escritos":
        # Aquí se integra fase0.4.py íntegro
        st.header("Escritos Reflexivos")
        alumno = st.text_input("Nombre del Alumno")
        # ... resto de campos ...

    elif opcion == "📊 Evaluación":
        # Aquí se integra fase0.6 y 0.7 íntegro
        st.header("Evaluación Trimestral")
        # Lógica de fotos y notas
