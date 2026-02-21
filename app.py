import streamlit as st
from PIL import Image
import base64
import io
import random
import time

# --- 1. CONFIGURACIÓN Y ESTILO EMPRESARIAL ---
st.set_page_config(page_title="ProfeEduca | Planeaciones ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    /* Estética Dark-Corporate */
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Foto de perfil circular empresarial */
    .profile-pic-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .profile-pic {
        border-radius: 50%;
        width: 150px;
        height: 150px;
        object-fit: cover;
        border: 4px solid #38bdf8;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }
    
    /* Tarjetas de Plan con Arte Empresarial */
    .plan-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    .plan-card:hover {
        transform: translateY(-15px);
        border-color: #38bdf8;
        background: rgba(30, 41, 59, 0.9);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Iconos dinámicos */
    .icon-box {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }

    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADOS ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "profe2024", "name": "Admin", "plan": "Magna"}},
        "step": "registro_email",
        "temp": {}
    }

def image_to_base64(image_file):
    if image_file:
        img = Image.open(image_file)
        img.thumbnail((400, 400))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- 3. FLUJO DE PANTALLAS ---

# PASO 1: REGISTRO INICIAL
if st.session_state.db["step"] == "registro_email":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align:center'><span style='font-size:5rem'>📡</span></div>", unsafe_allow_html=True)
        st.title("🍎 ProfeEduca")
        st.subheader("Conectando el saber ABCD")
        email = st.text_input("Correo Institucional")
        if st.button("Enlazar Cuenta"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "verificacion"
                st.rerun()
            else: st.error("Ingresa un correo corporativo válido.")

# PASO 2: VERIFICACIÓN
elif st.session_state.db["step"] == "verificacion":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.title("🔑 Seguridad")
        st.info(f"Enviado a: {st.session_state.db['temp']['email']}")
        st.caption(f"Código: {st.session_state.db['temp']['code']}")
        code_in = st.text_input("Código de Acceso")
        if st.button("Confirmar"):
            if code_in == st.session_state.db["temp"]["code"]:
                st.session_state.db["step"] = "perfil"
                st.rerun()

# PASO 3: PERFIL (FOTO Y DATOS)
elif st.session_state.db["step"] == "perfil":
    st.title("👤 Identidad del Maestro")
    c1, c2 = st.columns([1, 2])
    with c1:
        foto = st.file_uploader("Identificación Visual", type=['jpg', 'png'])
        if foto:
            b64 = image_to_base64(foto)
            st.session_state.db["temp"]["pic"] = b64
            st.markdown(f'<div class="profile-pic-container"><img src="data:image/png;base64,{b64}" class="profile-pic"></div>', unsafe_allow_html=True)
    with c2:
        n = st.text_input("Nombre(s)")
        a = st.text_input("Apellidos")
        u = st.text_input("ID de Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Registrar Perfil"):
            st.session_state.db["temp"].update({"name": f"{n} {a}", "user": u, "pass": p})
            st.session_state.db["step"] = "planes"
            st.rerun()

# PASO 4: PLANES CON DIBUJOS EMPRESARIALES
elif st.session_state.db["step"] == "planes":
    st.markdown("<h1 style='text-align: center;'>💎 Ecosistema de Suscripción</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>Potencia tu impacto en la comunidad CONAFE</p>", unsafe_allow_html=True)
    
    # Definimos los planes con sus dibujos (Emojis representativos)
    planes = {
        "Gratuito": {"p": "$0", "l": "2", "t": "7 Días", "icon": "🌱", "color": "#94a3b8"},
        "Plata":    {"p": "$200", "l": "12", "t": "Mensual", "icon": "🥈", "color": "#e2e8f0"},
        "Oro":      {"p": "$300", "l": "24", "t": "Mensual", "icon": "🏆", "color": "#fbbf24"},
        "Platino":  {"p": "$450", "l": "50", "t": "Mensual", "icon": "⚡", "color": "#38bdf8"},
        "Magna":    {"p": "$3999", "l": "∞", "t": "Anual", "icon": "🏛️", "color": "#f472b6"}
    }
    
    cols = st.columns(5)
    for i, (nombre, info) in
