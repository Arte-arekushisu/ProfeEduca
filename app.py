import streamlit as st
from PIL import Image
import base64
import io
import random
import time

# --- 1. CONFIGURACIÓN Y ESTILOS DINÁMICOS ---
st.set_page_config(page_title="Planeaciones ABCD | ProfeEduca", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1a1c24 0%, #050505 100%);
        color: #e0e0e0;
    }
    
    /* EFECTO DE MOVIMIENTO Y RESPLANDOR EN TARJETAS */
    .plan-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
    }
    
    .plan-card:hover {
        transform: scale(1.05) translateY(-15px);
        background: rgba(0, 212, 255, 0.1);
        border-color: #00d4ff;
        box-shadow: 0px 15px 30px rgba(0, 212, 255, 0.3);
    }

    .profile-pic {
        border-radius: 50%;
        width: 120px; height: 120px;
        object-fit: cover;
        border: 3px solid #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS Y SESIÓN ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "123", "name": "Admin", "plan": "Magna", "pic": None}},
        "auth": False,
        "step": "login",
        "temp_user": {}
    }

# --- 3. PLANES ---
PLANES = {
    "Gratuito": {"costo": "$0", "limite": 2, "periodo": "7 Días", "anim": "🍎"},
    "Plata":    {"costo": "$200", "limite": 12, "periodo": "Mensual", "anim": "🥈"},
    "Oro":      {"costo": "$300", "limite": 24, "periodo": "Mensual", "anim": "👑"},
    "Platino":  {"costo": "$450", "limite": 50, "periodo": "Mensual", "anim": "💎"},
    "Magna":    {"costo": "$3999", "limite": "∞", "periodo": "Anual", "anim": "🚀"}
}

# --- 4. FLUJO DE PANTALLAS ---

if st.session_state.db["step"] == "login":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("Planeaciones ABCD 🍎")
        st.subheader("Inicia sesión para innovar")
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR"):
                if u in st.session_state.db["usuarios"] and st.session_state.db["usuarios"][u]["pass"] == p:
                    st.session_state.db.update({"auth": True, "step": "app", "current_user": u})
                    st.rerun()
        if st.button("¿Nuevo aquí? Regístrate"):
            st.session_state.db["step"] = "registro"
            st.rerun()

elif st.session_state.db["step"] == "registro":
    st.title("Selecciona tu Nivel de Poder Docente")
    
    cols = st.columns(5)
    for i, (nombre, info) in enumerate(PLANES.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="plan-card">
                    <div style="font-size: 40px;">{info['anim']}</div>
                    <h3 style='color:#00d4ff'>{nombre}</h3>
                    <h2 style='margin:0;'>{info['costo']}</h2>
                    <p style='font-size: 0.8em;'>{info['periodo']}</p>
                    <hr style='opacity:0.2'>
                    <p><b>{info['limite']}</b> Archivos</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Elegir {nombre}", key=f"sel_{nombre}"):
                st.session_state.db["temp_user"]["plan"] = nombre
                st.success(f"Has elegido el Plan {nombre}")

    st.divider()
    with st.form("reg_form"):
        st.write("### Completa tu perfil corporativo")
        c1, c2 = st.columns(2)
        u_user = c1.text_input("Crea tu Usuario")
        u_mail = c2.text_input("Tu Correo Electrónico")
        u_pass
