import streamlit as st
from PIL import Image
import base64
import io
import random
import time
import requests  # Nueva librería para la IA

# --- 1. CONFIGURACIÓN Y ESTILO EMPRESARIAL ---
st.set_page_config(page_title="ProfeEduca | Planeaciones ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    /* Estética Dark-Corporate */
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    .profile-pic-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .profile-pic {
        border-radius: 50%;
        width: 150px;
        height: 150px;
        border: 4px solid #38bdf8;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }
    
    .plan-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s;
    }

    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        font-weight: 700;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADOS Y FUNCIONES IA ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "profe2024", "name": "Admin", "plan": "Magna"}},
        "step": "registro_email", 
        "temp": {}
    }

# CLAVE DE API (Asegúrate de poner tu llave activa aquí)
G_KEY = "TU_API_KEY_AQUÍ"

def llamar_gemini(prompt):
    """Función modular para consultar a la IA sin afectar el resto del código"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={G_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Como experto en el modelo educativo ABCD de CONAFE: {prompt}"}]}]
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error de conexión: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def image_to_base64(image_file):
    if image_file:
        img = Image.open(image_file)
        img.thumbnail((400, 400))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- 3. FLUJO DE PANTALLAS ---

# PASO 1: CORREO ELECTRÓNICO
if st.session_state.db["step"] == "registro_email":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align:center; font-size:4rem;'>💼</div>", unsafe_allow_html=True)
        st.title("🍎 ProfeEduca")
        email = st.text_input("Correo Electrónico")
        if st.button("Enviar Código de Seguridad"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "verificacion"
                st.rerun()

# PASO 2: VERIFICACIÓN
elif st.session_state.db["step"] == "verificacion":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.title("🔒 Verificación")
        st.info(f"Código enviado a: {st.session_state.db['temp']['email']}")
        st.caption(f"(DEBUG: {st.session_state.db['temp']['code']})")
        code_in = st.text_input("Ingresa el código")
        if st.button("Confirmar Identidad"):
            if code_in == st.session_state.db["temp"]["code"]:
                st.session_state.db["step"] = "perfil"
                st.rerun()

# PASO 3: PERFIL
elif st.session_state.db["step"] == "perfil":
    st.title("👤 Expediente del Educador")
    col_img, col_data = st.columns([1, 2])
    with col_img:
        foto = st.file_uploader("Subir Foto", type=['jpg', 'png'])
        if foto:
            b64_img = image_to_base64(foto)
            st.session_state.db["temp"]["pic"] = b64_img
            st.markdown(f'<div class="profile-pic-container"><img src="data:image/png;base64,{b64_img}" class="profile-pic"></div>', unsafe_allow_html=True)
    with col_data:
        n, a = st.text_input("Nombre"), st.text_input("Apellidos")
        u, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
        if st.button("Finalizar Perfil"):
            st.session_state.db["temp"].update({"name": f"{n} {a}", "user": u, "pass": p})
            st.session_state.db["step"] = "planes"
            st.rerun()

# PASO 4: PLANES
elif st.session_state.db["step"] == "planes":
    st.markdown("<h1 style='text-align: center;'>💎 Membresías Empresariales</h1>", unsafe_allow_html=True)
    planes_info = {
        "Gratuito": {"p": "$0", "l": "2", "icon": "🌱"},
        "Plata":    {"p": "$200", "l": "12", "icon": "🥈"},
        "Oro":      {"p": "$300", "l": "24", "icon": "🏆"},
        "Platino":  {"p": "$450", "l": "50", "icon": "⚡"},
        "Magna":    {"p": "$3999", "l": "∞", "icon": "🏛️"}
    }
    cols = st.columns(5)
    for i, (nombre, info) in enumerate(planes_info.items()):
        with cols[i]:
            st.markdown(f'<div class="plan-card"><h2>{info["icon"]}</h2><h3>{nombre}</h3><h1>{info["p"]}</h1></div>', unsafe_allow_html=True)
            if st.button(f"Elegir {nombre}", key=nombre):
                tmp = st.session_state.db["temp"]
                st.session_state.db["usuarios"][tmp["user"]] = {"pass": tmp["pass"], "name": tmp["name"], "plan": nombre, "pic": tmp.get("pic")}
                st.session_state.db["step"] = "app"
                st.rerun()

# --- DASHBOARD FINAL CON INTEGRACIÓN DE IA ---
elif st.session_state.db["step"] == "app":
    st.title("🚀 Panel Principal ProfeEduca")
    
    # Barra lateral con información del usuario
    with st.sidebar:
        if st.session_state.db["temp"].get("pic"):
            st.markdown(f'<img src="data:image/png;base64,{st.session_state.db["temp"]["pic"]}" style="width:100px; border-radius:50%;">', unsafe_allow_html=True)
        st.write(f"Maestro: **{st.session_state.db['temp'].get('name', 'Admin')}**")
        st.caption(f"Plan: {st.session_state.db['usuarios'].get(st.session_state.db['temp'].get('user'), {}).get('plan', 'Magna')}")
        if st.button("Cerrar Sesión"):
            st.session_state.db["step"] = "registro_email"
            st.rerun()

    # MODULO IA (Integración Modular)
    st.divider()
    st.subheader("🤖 Asistente IA para Planeaciones ABCD")
    prompt_usuario = st.text_area("¿Sobre qué tema quieres generar una estrategia educativa hoy?", placeholder="Ej: Estrategia de lectura para niños de primer nivel...")
    
    if st.button("Generar con Gemini IA"):
        if prompt_usuario:
            with st.spinner("La IA está redactando tu propuesta..."):
                resultado = llamar_gemini(prompt_usuario)
                st.info("Sugerencia de la IA:")
                st.write(resultado)
        else:
            st.warning("Por favor, escribe un tema o duda.")
