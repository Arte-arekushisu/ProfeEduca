import streamlit as st
import requests
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import datetime

# 1. DISEÑO DINÁMICO Y ESTILO "PROFE EDUCA"
st.set_page_config(page_title="Profe Educa", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp {
        background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505);
        background-size: 400% 400%;
        animation: move 12s ease infinite;
        color: white;
    }
    .glass-card { background: rgba(255, 255, 255, 0.07); border-radius: 20px; padding: 25px; border: 1px solid #00d4ff; box-shadow: 0 0 20px rgba(0,212,255,0.3); }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0 0 15px #00d4ff; }
    .slogan { text-align: center; font-style: italic; color: #e0e0e0; font-size: 20px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGICA DE SUSCRIPCIONES Y LIMITES (MODELO ABCD)
if 'session' not in st.session_state:
    st.session_state.session = {"auth": False, "plan": None, "user": "", "regs_planeacion": 0, "regs_reflexion": 0, "reflexiones": {}}

# 3. GENERADOR DE PDF PROFESIONAL (PDF INALTERABLE)
class PDF(FPDF):
    def header_oficial(self, titulo, d, logos):
        if logos[0]: self.image(logos[0], 10, 8, 22)
        if logos[1]: self.image(logos[1], 178, 8, 22)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, titulo, 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, f"Comunidad: {d['comunidad']} | EC: {d['nombre']} | Modelo ABCD CONAFE", 0, 1, 'C')
        self.ln(10)

# 4. INTERFAZ DE REGISTRO Y PAGOS
if not st.session_state.session["auth"]:
    st.markdown("<h1>PROFE EDUCA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='slogan'>\"Inspirando el saber, transformando la comunidad: El eco de tu enseñanza es el futuro de todos.\"</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            email = st.text_input("Correo Electrónico")
            plan = st.selectbox("Selecciona tu Suscripción", ["Prueba 3 días (Gratis)", "Mensual ($649)", "Anual ($6,499)"])
            st.write("---")
            st.write("💳 **Registro de Pago Directo**")
            st.text_input("Número de Tarjeta")
            st.text_input("CLABE (Para depósitos directos)", type="password")
        with c2:
            st.info("🎯 Tu suscripción incluye acceso total a planeación semanal, diario reflexivo y evaluaciones trimestrales automatizadas.")
            if st.button("ACTIVAR MI CUENTA"):
                st.session_state.session.update({"auth": True, "plan": plan, "user": email})
                st.balloons()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- PANEL DE CONTROL EDUCADOR ---
    with st.sidebar:
        st.title("PROFE EDUCA")
        menu = st.radio("MENÚ", ["🏠 Inicio", "📅 Planeación ABCD", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 Asistencia IA"])
        st.divider()
        if st.button("Cerrar Sesión"): st.session_state.session["auth"] = False; st.rerun()

    # --- PLANEACIÓN SEMANAL ---
    if menu == "📅 Planeación ABCD":
        st.header("Planeación Semanal Estructurada")
        tema = st.text_input("Tema de Interés")
        estacion = st.text_input("Estación Permanente")
        m1 = st.text_input("Materia Post-Receso (Hora 1)")
        m2 = st.text_input("Materia Post-Receso (Hora 2)")
