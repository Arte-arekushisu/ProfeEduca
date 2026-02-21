import streamlit as st
from PIL import Image
import base64
import io
import random

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO "HIGH-TECH" ---
st.set_page_config(page_title="Profe Educa ABCD - V0", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    /* Fondo con gradiente animado y profundidad */
    .stApp { 
        background: radial-gradient(circle at top, #1a1c24 0%, #050505 100%);
        color: #e0e0e0;
    }
    
    /* Tarjetas corporativas */
    .plan-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s;
    }
    .plan-card:hover {
        transform: translateY(-10px);
        border-color: #00d4ff;
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Foto de perfil circular */
    .profile-pic {
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 3px solid #00d4ff;
        display: block;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }
    
    /* Animación de entrada */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .fade-in { animation: fadeIn 1.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGICA DE BASE DE DATOS Y SESIÓN ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {
            "admin": {"pass": "master123", "name": "Admin", "plan": "Magna", "pic": None}
        },
        "auth": False,
        "step": "login", # login, registro, verificacion, app
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

# --- 3. DEFINICIÓN DE PLANES CORPORATIVOS ---
PLANES = {
    "Gratuito": {"costo": "$0", "limite": 2, "periodo": "7 Días", "desc": "Prueba tecnológica"},
    "Plata":    {"costo": "$200", "limite": 12, "periodo": "Mensual", "desc": "Uso profesional"},
    "Oro":      {"costo": "$300", "limite": 24, "periodo": "Mensual", "desc": "Alto rendimiento"},
    "Platino":  {"costo": "$450", "limite": 50, "periodo": "Mensual", "desc": "Potencia ilimitada"},
    "Magna":    {"costo": "$3999", "limite": "∞", "periodo": "Anual", "desc": "Excelencia docente"}
}

# --- 4. FLUJO DE PANTALLAS ---

# PANTALLA: LOGIN
if st.session_state.db["step"] == "login":
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🍎 Profe Educa ABCD")
        st.subheader("Acceso al Ecosistema Digital")
        with st.form("login_form"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u in st.session_state.db["usuarios"] and st.session_state.db["usuarios"][u]["pass"] == p:
                    st.session_state.db["auth"] = True
                    st.session_state.db["step"] = "app"
                    st.session_state.db["current_user"] = u
                    st.rerun()
                else: st.error("Credenciales incorrectas")
        if st.button("Crear cuenta nueva"):
            st.session_state.db["step"] = "registro"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA: REGISTRO CON TABLA COMPARATIVA
elif st.session_state.db["step"] == "registro":
    st.title("🚀 Únete a la Revolución Educativa")
    
    # Tabla Comparativa Corporativa
    st.markdown("### Selecciona tu Nivel de Acceso")
    cols = st.columns(5)
    for i, (nombre, info) in enumerate(PLANES.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="plan-card">
                    <h3 style='color:#00d4ff'>{nombre}</h3>
                    <h2>{info['costo']}</h2>
                    <p>{info['periodo']}</p>
                    <hr
