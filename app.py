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
    
    /* Foto de perfil circular empresarial con efecto neón */
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
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(12px);
    }
    .plan-card:hover {
        transform: translateY(-15px);
        border-color: #38bdf8;
        background: rgba(30, 41, 59, 0.9);
        box-shadow: 0 15px 35px rgba(56, 189, 248, 0.2);
    }

    /* Iconos llamativos */
    .plan-icon {
        font-size: 3.5rem;
        margin-bottom: 15px;
        display: block;
    }

    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.6);
        transform: scale(1.02);
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

# PASO 1: CORREO ELECTRÓNICO (SEGURIDAD INICIAL)
if st.session_state.db["step"] == "registro_email":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align:center; font-size:4rem;'>💼</div>", unsafe_allow_html=True)
        st.title("🍎 ProfeEduca")
        st.subheader("Planeaciones para el Maestro ABCD")
        st.write("Inicia tu registro empresarial ingresando tu correo.")
        email = st.text_input("Correo Electrónico")
        if st.button("Enviar Código de Seguridad"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "verificacion"
                st.rerun()
            else:
                st.error("Por favor, ingresa un correo corporativo válido.")

# PASO 2: VERIFICACIÓN
elif st.session_state.db["step"] == "verificacion":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.title("🔒 Verificación")
        st.info(f"Código enviado a: {st.session_state.db['temp']['email']}")
        st.caption(f"(DEBUG: El código es {st.session_state.db['temp']['code']})")
        code_in = st.text_input("Ingresa el código de 6 dígitos")
        if st.button("Confirmar Identidad"):
            if code_in == st.session_state.db["temp"]["code"]:
                st.session_state.db["step"] = "perfil"
                st.rerun()
            else:
                st.error("Código inválido.")

# PASO 3: PERFIL (FOTO CIRCULAR Y DATOS)
elif st.session_state.db["step"] == "perfil":
    st.title("👤 Expediente del Educador")
    st.write("Configura tu identidad profesional para los maestros de CONAFE.")
    
    col_img, col_data = st.columns([1, 2])
    with col_img:
        foto = st.file_uploader("Fotografía Profesional", type=['jpg', 'png'])
        if foto:
            b64_img = image_to_base64(foto)
            st.session_state.db["temp"]["pic"] = b64_img
            st.markdown(f'<div class="profile-pic-container"><img src="data:image/png;base64,{b64_img}" class="profile-pic"></div>', unsafe_allow_html=True)

    with col_data:
        n = st.text_input("Nombre(s)")
        a = st.text_input("Apellidos")
        u = st.text_input("Usuario Único")
        p = st.text_input("Contraseña", type="password")
        if st.button("Finalizar Perfil"):
            if n and a and u and p:
                st.session_state.db["temp"].update({"name": f"{n} {a}", "user": u, "pass": p})
                st.session_state.db["step"] = "planes"
                st.rerun()
            else:
                st.warning("Completa todos los campos para continuar.")

# PASO 4: PLANES CON DIBUJOS LLAMATIVOS
elif st.session_state.db["step"] == "planes":
    st.markdown("<h1 style='text-align: center;'>💎 Membresías Empresariales</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Selecciona tu nivel de impacto en el modelo ABCD</p>", unsafe_allow_html=True)
    
    planes_info = {
        "Gratuito": {"p": "$0", "l": "2", "t": "7 Días", "icon": "🌱", "desc": "Inicio Educativo"},
        "Plata":    {"p": "$200", "l": "12", "t": "Mensual", "icon": "🥈", "desc": "Docente Activo"},
        "Oro":      {"p": "$300", "l": "24", "t": "Mensual", "icon": "🏆", "desc": "Alto Rendimiento"},
        "Platino":  {"p": "$450", "l": "50", "t": "Mensual", "icon": "⚡", "color": "#38bdf8", "desc": "Potencia Total"},
        "Magna":    {"p": "$3999", "l": "∞", "t": "Anual", "icon": "🏛️", "desc": "Elite ProfeEduca"}
    }
    
    cols = st.columns(5)
    for i, (nombre, info) in enumerate(planes_info.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="plan-card">
                    <span class="plan-icon">{info['icon']}</span>
                    <h3 style='color:#38bdf8; margin-bottom:5px;'>{nombre}</h3>
                    <p style='font-size:0.8rem; margin-bottom:15px; opacity:0.7;'>{info['desc']}</p>
                    <h2 style='margin:0;'>{info['p']}</h2>
                    <p><small>{info['t']}</small></p>
                    <hr style='opacity:0.2'>
                    <div style='text-align: left; font-size: 0.85rem;'>
                        <p>✅ {info['l']} Planeaciones</p>
                        <p>✅ {info['l']} Escritos</p>
                        <p>✅ {info['l']} Evaluaciones</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seleccionar {nombre}", key=f"sel_{nombre}"):
                st.balloons()
                st.snow()
                tmp = st.session_state.db["temp"]
                st.session_state.db["usuarios"][tmp["user"]] = {
                    "pass": tmp["pass"], "name": tmp["name"], "plan": nombre, "pic": tmp.get("pic")
                }
                st.success(f"¡Bienvenido al sistema, Maestro {tmp['name']}!")
                time.sleep(2)
                st.session_state.db["step"] = "app"
                st.rerun()

# DASHBOARD FINAL (ESTRUCTURA DE TRABAJO)
elif st.session_state.db["step"] == "app":
    st.title("🚀 Panel Principal ProfeEduca")
    st.write("Bienvenido al centro de mando para tus planeaciones ABCD.")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["step"] = "registro_email"
        st.rerun()
