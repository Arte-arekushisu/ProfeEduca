import streamlit as st
from PIL import Image
import base64
import io
import random

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO "HIGH-TECH" ---
st.set_page_config(page_title="Planeaciones para el Maestro ABCD | ProfeEduca", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    /* Fondo con gradiente animado y profundidad */
    .stApp { 
        background: radial-gradient(circle at top, #1a1c24 0%, #050505 100%);
        color: #e0e0e0;
    }
    
    /* Tarjetas corporativas con efecto de cristal */
    .plan-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s, border-color 0.3s;
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
    
    /* Estilo de botones */
    .stButton>button {
        border-radius: 20px;
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGICA DE BASE DE DATOS Y SESIÓN ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {
            "admin": {"pass": "master123", "name": "Admin ProfeEduca", "plan": "Magna", "pic": None}
        },
        "auth": False,
        "step": "login", # login, registro, verificacion, app
        "temp_user": {}
    }

def process_profile_pic(image_file):
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
    "Platino":  {"costo": "$450", "limite": 50, "periodo": "Mensual", "desc": "Máxima potencia"},
    "Magna":    {"costo": "$3999", "limite": "Ilimitado", "periodo": "Anual", "desc": "Excelencia docente"}
}

# --- 4. FLUJO DE PANTALLAS ---

# PANTALLA: LOGIN
if st.session_state.db["step"] == "login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Planeaciones ABCD 🍎")
        st.subheader("Bienvenido a ProfeEduca")
        with st.form("login_form"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INICIAR SESIÓN"):
                if u in st.session_state.db["usuarios"] and st.session_state.db["usuarios"][u]["pass"] == p:
                    st.session_state.db["auth"] = True
                    st.session_state.db["step"] = "app"
                    st.session_state.db["current_user"] = u
                    st.rerun()
                else: st.error("Credenciales incorrectas")
        st.button("Crear cuenta de educador", on_click=lambda: st.session_state.db.update({"step": "registro"}))

# PANTALLA: REGISTRO CON TABLA COMPARATIVA
elif st.session_state.db["step"] == "registro":
    st.title("🚀 Únete a ProfeEduca")
    st.markdown("### Selecciona el plan que impulsará tu labor docente")
    
    cols = st.columns(5)
    for i, (nombre, info) in enumerate(PLANES.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="plan-card">
                    <h3 style='color:#00d4ff'>{nombre}</h3>
                    <h2>{info['costo']}</h2>
                    <p>{info['periodo']}</p>
                    <hr style='border-color:rgba(0,212,255,0.2)'>
                    <p><b>{info['limite']}</b> Planeaciones</p>
                    <p><b>{info['limite']}</b> Escritos Diarios</p>
                    <p><b>{info['limite']}</b> Evaluaciones</p>
                    <p><small>{info['desc']}</small></p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seleccionar {nombre}"):
                st.session_state.db["temp_user"]["plan"] = nombre
                st.toast(f"Plan {nombre} marcado.")

    st.divider()
    
    with st.form("reg_form"):
        col_a, col_b = st.columns(2)
        u_user = col_a.text_input("Usuario")
        u_pass = col_b.text_input("Contraseña", type="password")
        u_real = col_a.text_input("Nombre Completo")
        u_mail = col_b.text_input("Correo Electrónico")
        u_foto = st.file_uploader("Foto de Perfil", type=['jpg', 'png'])
