import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILOS (De Fase 0.1 y 0.2) ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

def aplicar_estilos_saas():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
        /* Animación Manzana y Gusanito */
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
        .apple-container { font-size: 80px; text-align: center; animation: float 3s ease-in-out infinite; position: relative; }
        .worm-icon { position: absolute; font-size: 30px; left: 50%; top: -10px; }
        /* Tarjetas de Planes */
        .plan-card { background: rgba(30, 41, 59, 0.6); border: 1px solid #38bdf8; border-radius: 15px; padding: 20px; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. CLASES PDF UNIFICADAS (De Fase 0.4, 0.5 y 0.7) ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class GeneradorPDF(FPDF):
    def header_profesional(self, titulo, color_fondo=(128, 0, 0)):
        self.set_fill_color(*color_fondo)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(10)

# --- 3. LÓGICA DE CONTROL (State Management) ---
if "step" not in st.session_state:
    st.session_state.step = "login"
if "plan" not in st.session_state:
    st.session_state.plan = None

aplicar_estilos_saas()

# --- 4. NAVEGACIÓN POR FASES ---

# FASE 0.1: ACCESO
if st.session_state.step == "login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        if st.button("Entrar al Ecosistema", use_container_width=True):
            st.session_state.step = "plan"
            st.rerun()

# FASE 0.1: PLANES MENSUALES
elif st.session_state.step == "plan":
    st.subheader("Elige tu suscripción mensual")
    c1, c2, c3 = st.columns(3)
    planes = {"Básico": "$99", "Pro": "$199", "Premium": "$299"}
    for i, (nombre, precio) in enumerate(planes.items()):
        with [c1, c2, c3][i]:
            st.markdown(f"<div class='plan-card'><h3>{nombre}</h3><h2>{precio}/mes</h2></div>", unsafe_allow_html=True)
            if st.button(f"Activar {nombre}", key=nombre):
                st.session_state.plan = nombre
                st.session_state.step = "app"
                st.rerun()

# FASE 0.2 - 0.7: LA APLICACIÓN INTEGRADA
elif st.session_state.step == "app":
    # Sidebar de Navegación Profesional
    with st.sidebar:
        st.markdown(f"**Plan: {st.session_state.plan}**")
        menu = st.radio("Herramientas:", ["🏠 Inicio", "📝 Planeaciones", "👤 Escritos", "📊 Evaluaciones"])
        if st.button("Cerrar Sesión"):
            st.session_state.step = "login"
            st.rerun()

    # CONTENIDO DINÁMICO SEGÚN EL MENÚ
    if menu == "🏠 Inicio":
        col_v, col_t = st.columns([1, 2])
        with col_v:
            st.markdown('<div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>', unsafe_allow_html=True)
        with col_t:
            st.title("Panel de Control")
            st.write("Bienvenido, Maestro. Seleccione una herramienta en el menú lateral.")

    elif menu == "📝 Planeaciones":
        # Aquí vive la lógica de la FASE 0.5
        st.header("Generador de Planeación Semanal")
        with st.form("form_plan"):
            materia = st.text_input("Materia")
            activ = st.text_area("Actividades")
            if st.form_submit_button("Crear Planeación"):
                st.success("PDF Generado (Simulación de Fase 0.5)")

    elif menu == "👤 Escritos":
        # Aquí vive la lógica de la FASE 0.4
        st.header("Escritos Reflexivos")
        alumno = st.text_input("Nombre del Alumno")
        observacion = st.text_area("Observaciones de seguimiento")
        if st.button("Exportar Escrito"):
            st.info("Procesando documento...")

    elif menu == "📊 Evaluaciones":
        # Aquí vive la lógica de la FASE 0.6 y 0.7
        st.header("Evaluación Trimestral")
        uploaded_files = st.file_uploader("Subir evidencias (Fotos)", accept_multiple_files=True)
        nota = st.slider("Calificación", 5, 10)
        if st.button("Finalizar Reporte"):
            st.balloons()
