import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time
import base64

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

# Inyección de CSS para mantener el diseño original
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .nav-list { display: flex; flex-direction: column; gap: 10px; padding: 10px; }
    .brand-header { font-size: 2.5rem; font-weight: 800; color: #38bdf8; text-shadow: 0 0 15px rgba(56,189,248,0.5); }
    .apple-container { font-size: 80px; position: relative; display: inline-block; }
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) opacity: 0; }
        50% { transform: translate(0px, -50px) opacity: 1; }
    }
    .worm-icon { position: absolute; font-size: 30px; animation: worm-move 3s infinite; }
    </style>
""", unsafe_allow_html=True)

# --- 2. CLASES DE PDF (Fases 0.4 - 0.7) ---
class MasterPDF(FPDF):
    def header_styled(self, titulo, color=(128, 0, 0)):
        self.set_fill_color(*color)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(5)

# --- 3. LÓGICA DE NAVEGACIÓN (Fases 0.1 - 0.3) ---
if "step" not in st.session_state:
    st.session_state.step = "login"
if "p" not in st.session_state:
    st.session_state.p = "inicio"

# PANTALLA DE LOGIN
if st.session_state.step == "login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align:center;' class='brand-header'>📏 ProfeEduca ✏️</div>", unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("Usuario")
            pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                if user and pw:
                    st.session_state.step = "app"
                    st.rerun()

# PANEL PRINCIPAL
elif st.session_state.step == "app":
    col_nav, col_main = st.columns([1, 4])

    with col_nav:
        st.markdown("### 🍎 Menú")
        if st.button("🏠 Inicio"): st.session_state.p = "inicio"
        if st.button("📝 Planeación Semanal"): st.session_state.p = "planeacion"
        if st.button("👤 Escrito Reflexivo"): st.session_state.p = "reflexivo"
        if st.button("📊 Evaluación Trimestral"): st.session_state.p = "evaluacion"
        st.divider()
        if st.button("🚪 Salir"): 
            st.session_state.step = "login"
            st.rerun()

    with col_main:
        # --- SUB-APP: INICIO ---
        if st.session_state.p == "inicio":
            st.markdown(f"<div style='text-align:center;' class='brand-header'>Bienvenido a ProfeEduca</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;' class='apple-container'><span class='worm-icon'>🐛</span>🍎</div>", unsafe_allow_html=True)
            st.info("Selecciona una herramienta en el menú de la izquierda para comenzar.")

        # --- SUB-APP: PLANEACIÓN (Fase 0.5) ---
        elif st.session_state.p == "planeacion":
            st.header("📝 Planeación Semanal ABCD")
            with st.form("f_plan"):
                c1, c2 = st.columns(2)
                ec = c1.text_input("Nombre del EC")
                com = c2.text_input("Comunidad")
                materia = st.text_input("Materia/Tema")
                actividades = st.text_area("Descripción de actividades")
                if st.form_submit_button("Generar PDF"):
                    pdf = MasterPDF()
                    pdf.add_page()
                    pdf.header_styled("PLANEACION SEMANAL")
                    pdf.set_text_color(0)
                    pdf.set_font("Helvetica", "B", 12)
                    pdf.cell(0, 10, f"EC: {clean(ec)} - Comunidad: {clean(com)}", 0, 1)
                    pdf.ln(5)
                    pdf.multi_cell(0, 10, f"Tema: {clean(materia)}\n\nActividades:\n{clean(actividades)}")
                    st.download_button("Descargar Planeación", pdf.output(dest='S'), "planeacion.pdf")

        # --- SUB-APP: ESCRITO (Fase 0.4) ---
        elif st.session_state.p == "reflexivo":
            st.header("👤 Escrito Reflexivo")
            with st.form("f_reflex"):
                alumno = st.text_input("Nombre del Alumno")
                observacion = st.text_area("Logros y desafíos observados")
                if st.form_submit_button("Guardar Escrito"):
                    pdf = MasterPDF()
                    pdf.add_page()
                    pdf.header_styled("ESCRITO REFLEXIVO", color=(0, 102, 204))
                    pdf.set_text_color(0)
                    pdf.cell(0, 10, f"Alumno: {clean(alumno)}", 0, 1)
                    pdf.multi_cell(0, 10, clean(observacion))
                    st.download_button("Descargar Escrito", pdf.output(dest='S'), "escrito.pdf")

        # --- SUB-APP: EVALUACIÓN (Fases 0.6 - 0.7) ---
        elif st.session_state.p == "evaluacion":
            st.header("📊 Evaluación Trimestral")
            nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
            if nivel != "Preescolar":
                nota = st.slider("Calificación", 5, 10, 8)
                if st.button("Generar Reporte"):
                    pdf = MasterPDF()
                    pdf.add_page()
                    pdf.header_styled("REPORTE DE EVALUACION", color=(0, 51, 102))
                    pdf.set_text_color(0)
                    pdf.cell(0, 10, f"Nivel: {nivel} - Calificación: {nota}", 0, 1)
                    st.download_button("Descargar Reporte", pdf.output(dest='S'), "evaluacion.pdf")
            else:
                st.write("Evaluación cualitativa para Preescolar.")
