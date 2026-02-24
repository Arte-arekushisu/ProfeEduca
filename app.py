import streamlit as st
from PIL import Image
import base64
import io
import random
import time
import requests
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN Y CONEXIONES ---
st.set_page_config(page_title="ProfeEduca | Planeaciones ABCD", page_icon="🍎", layout="wide")

# Credenciales integradas
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# Inicializar Supabase
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# --- 2. ESTILO EMPRESARIAL ---
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    .profile-pic {
        border-radius: 50%;
        width: 150px;
        height: 150px;
        object-fit: cover;
        border: 4px solid #38bdf8;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }
    .plan-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: 0.4s;
    }
    .plan-card:hover {
        transform: translateY(-10px);
        border-color: #38bdf8;
        background: rgba(30, 41, 59, 0.8);
    }
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        font-weight: 700;
        color: white;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES DE APOYO ---
def llamar_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Como experto en el modelo educativo ABCD de CONAFE, genera una propuesta pedagógica para: {prompt}"}]}]
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Error de IA: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def image_to_base64(image_file):
    if image_file:
        img = Image.open(image_file)
        img.thumbnail((300, 300))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- 4. LÓGICA DE NAVEGACIÓN ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "profe2024", "name": "Admin", "plan": "Magna"}},
        "step": "registro_email", 
        "temp": {}
    }

# PASO 1: REGISTRO DE EMAIL
if st.session_state.db["step"] == "registro_email":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
        st.subheader("Bienvenido, Maestro ABCD")
        email = st.text_input("Ingresa tu correo institucional:")
        if st.button("Enviar Código de Seguridad"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "verificacion"
                st.rerun()
            else:
                st.error("Correo no válido.")

# PASO 2: VERIFICACIÓN
elif st.session_state.db["step"] == "verificacion":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.title("🔒 Verificación")
        st.info(f"Código enviado a: {st.session_state.db['temp']['email']}")
        st.caption(f"(Simulación: El código es {st.session_state.db['temp']['code']})")
        code_in = st.text_input("Introduce el código de 6 dígitos")
        if st.button("Validar Identidad"):
            if code_in == st.session_state.db["temp"]["code"]:
                st.session_state.db["step"] = "perfil"
                st.rerun()
            else:
                st.error("Código incorrecto.")

# PASO 3: PERFIL
elif st.session_state.db["step"] == "perfil":
    st.title("👤 Perfil del Educador")
    col_img, col_data = st.columns([1, 2])
    with col_img:
        foto = st.file_uploader("Sube tu foto profesional", type=['jpg', 'png'])
        if foto:
            b64 = image_to_base64(foto)
            st.session_state.db["temp"]["pic"] = b64
            st.markdown(f'<img src="data:image/png;base64,{b64}" class="profile-pic">', unsafe_allow_html=True)
    with col_data:
        n = st.text_input("Nombre Completo")
        u = st.text_input("Nombre de Usuario")
        p = st.text_input("Crea una Contraseña", type="password")
        if st.button("Configurar Membresía"):
            if n and u and p:
                st.session_state.db["temp"].update({"name": n, "user": u, "pass": p})
                st.session_state.db["step"] = "planes"
                st.rerun()

# PASO 4: SELECCIÓN DE PLANES
elif st.session_state.db["step"] == "planes":
    st.markdown("<h2 style='text-align: center;'>💎 Selecciona tu Plan</h2>", unsafe_allow_html=True)
    planes = {
        "Gratuito": "🌱", "Plata": "🥈", "Oro": "🏆", "Platino": "⚡", "Magna": "🏛️"
    }
    cols = st.columns(5)
    for i, (nombre, icono) in enumerate(planes.items()):
        with cols[i]:
            st.markdown(f'<div class="plan-card"><h1>{icono}</h1><h3>{nombre}</h3></div>', unsafe_allow_html=True)
            if st.button(f"Activar {nombre}", key=nombre):
                tmp = st.session_state.db["temp"]
                st.session_state.db["usuarios"][tmp["user"]] = {
                    "pass": tmp["pass"], "name": tmp["name"], "plan": nombre, "pic": tmp.get("pic")
                }
                st.session_state.db["step"] = "app"
                st.rerun()

# PASO 5: DASHBOARD CON IA
elif st.session_state.db["step"] == "app":
    # Sidebar
    with st.sidebar:
        st.title("🍎 Menú")
        if st.session_state.db["temp"].get("pic"):
            st.markdown(f'<img src="data:image/png;base64,{st.session_state.db["temp"]["pic"]}" style="width:100px; border-radius:50%;">', unsafe_allow_html=True)
        st.write(f"Maestro: **{st.session_state.db['temp'].get('name')}**")
        if st.button("Cerrar Sesión"):
            st.session_state.db["step"] = "registro_email"
            st.rerun()

    st.title("🚀 Centro de Planeación ABCD")
    st.markdown("---")
    
    st.subheader("🤖 Asistente Pedagógico Gemini")
    prompt = st.text_area("¿Qué estrategia o planeación necesitas desarrollar hoy?", height=150)
    
    if st.button("Generar Planeación con IA"):
        if prompt:
            with st.spinner("Analizando con el modelo ABCD..."):
                respuesta = llamar_gemini(prompt)
                st.markdown("### 📝 Propuesta Generada:")
                st.info(respuesta)
        else:
            st.warning("Escribe un tema para comenzar.")
