import streamlit as st
from PIL import Image
import base64
import io
import random
import time

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO "HIGH-TECH" ---
st.set_page_config(page_title="Planeaciones ABCD | ProfeEduca", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1a1c24 0%, #050505 100%);
        color: #e0e0e0;
    }
    
    /* Efecto de levitación y resplandor en planes */
    .plan-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s ease;
    }
    .plan-card:hover {
        transform: translateY(-15px);
        border-color: #00d4ff;
        box-shadow: 0px 10px 30px rgba(0, 212, 255, 0.4);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Perfil circular con sombra de neón */
    .profile-pic {
        border-radius: 50%;
        width: 130px; height: 130px;
        object-fit: cover;
        border: 3px solid #00d4ff;
        display: block;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGICA DE DATOS ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "master123", "name": "Admin", "plan": "Magna", "pic": None}},
        "auth": False,
        "step": "login",
        "temp_user": {}
    }

def img_to_b64(image_file):
    if image_file:
        img = Image.open(image_file)
        img.thumbnail((300, 300))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

PLANES = {
    "Gratuito": {"costo": "$0", "limite": 2, "periodo": "7 Días", "desc": "Prueba tecnológica"},
    "Plata":    {"costo": "$200", "limite": 12, "periodo": "Mensual", "desc": "Uso profesional"},
    "Oro":      {"costo": "$300", "limite": 24, "periodo": "Mensual", "desc": "Alto rendimiento"},
    "Platino":  {"costo": "$450", "limite": 50, "periodo": "Mensual", "desc": "Potencia ilimitada"},
    "Magna":    {"costo": "$3999", "limite": "∞", "periodo": "Anual", "desc": "Excelencia docente"}
}

# --- 3. FLUJO DE PANTALLAS ---

# A. PANTALLA DE LOGIN
if st.session_state.db["step"] == "login":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🍎 ProfeEduca ABCD")
        st.subheader("Acceso al Futuro Docente")
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u in st.session_state.db["usuarios"] and st.session_state.db["usuarios"][u]["pass"] == p:
                    st.session_state.db.update({"auth": True, "step": "app", "current_user": u})
                    st.rerun()
                else: st.error("Acceso denegado.")
        st.button("¿No tienes cuenta? Regístrate aquí", on_click=lambda: st.session_state.db.update({"step": "registro"}))

# B. PASO 1: REGISTRO DE DATOS Y FOTO
elif
