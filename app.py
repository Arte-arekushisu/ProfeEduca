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
    
    /* Inputs y Botones Estilizados */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 10px;
        font-weight: 600;
    }
    
    /* Tarjetas de Plan */
    .plan-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s ease;
    }
    .plan-card:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADOS ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "profe2024", "name": "Admin", "plan": "Magna"}},
        "step": "registro_email", # registro_email, verificacion, perfil, planes, app
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

# --- 3. FLUJO DE REGISTRO VERSIÓN 0.1 ---

# PASO 1: CORREO ELECTRÓNICO
if st.session_state.db["step"] == "registro_email":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🍎 ProfeEduca")
        st.subheader("Planeaciones para el Maestro ABCD")
        st.write("Para comenzar, ingresa tu correo institucional o personal.")
        email = st.text_input("Correo Electrónico")
        if st.button("Enviar Código de Confirmación"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "verificacion"
                st.rerun()
            else:
                st.error("Por favor, ingresa un correo válido.")

# PASO 2: CÓDIGO DE CONFIRMACIÓN
elif st.session_state.db["step"] == "verificacion":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🔒 Verificación")
        st.write(f"Hemos enviado un código a **{st.session_state.db['temp']['email']}**")
        st.caption(f"(Simulación IA: El código es {st.session_state.db['temp']['code']})")
        code_in = st.text_input("Ingresa el código de 6 dígitos")
        if st.button("Validar Identidad"):
            if code_in == st.session_state.db["temp"]["code"]:
                st.success("Correo verificado correctamente.")
                time.sleep(1)
                st.session_state.db["step"] = "perfil"
                st.rerun()
            else:
                st.error("Código incorrecto.")

# PASO 3: DATOS PERSONALES Y FOTO (EL CORAZÓN DE LA VERSIÓN 0.1)
elif st.session_state.db["step"] == "perfil":
    st.title("👤 Perfil del Educador")
    st.write("Configura tu identidad profesional en ProfeEduca.")
    
    with st.container():
        col_img, col_data = st.columns([1, 2])
        
        with col_img:
            foto = st.file_uploader("Sube tu foto de perfil", type=['jpg', 'png', 'jpeg'])
            if foto:
                b64_img = image_to_base64(foto)
                st.session_state.db["temp"]["pic"] = b64_img
                st.markdown(f'<div class="profile-pic-container"><img src="data:image/png;base64,{b64_img}" class="profile-pic"></div>', unsafe_allow_html=True)
            else:
                st.info("La foto se mostrará en formato circular empresarial.")

        with col_data:
            nombre = st.text_input("Nombre(s)")
            apellido = st.text_input("Apellidos")
            usuario = st.text_input("Nombre de Usuario (ID Único)")
            password = st.text_input("Contraseña", type="password")
            
            if st.button("Finalizar Registro de Perfil"):
                if nombre and apellido and usuario and password:
                    st.session_state.db["temp"].update({
                        "name": f"{nombre} {apellido}",
                        "user": usuario,
                        "pass": password
                    })
                    st.session_state.db["step"] = "planes"
                    st.rerun()
                else:
                    st.warning("Por favor, completa todos los campos.")

# PASO 4: SUSCRIPCIONES (TABLA CORPORATIVA)
elif st.session_state.db["step"] == "planes":
    st.title("💎 Membresías ProfeEduca")
    st.write("Selecciona el nivel de potencia para tus planeaciones ABCD.")
    
    planes_data = {
        "Gratuito": {"p": "$0", "l": "2", "t": "7 Días"},
        "Plata": {"p": "$200", "l": "12", "t": "Mensual"},
        "Oro": {"p": "$300", "l": "24", "t": "Mensual"},
        "Platino": {"p": "$450", "l": "50", "t": "Mensual"},
        "Magna": {"p": "$3999", "l": "∞", "t": "Anual"}
    }
    
    cols = st.columns(5)
    for i, (nombre, info) in enumerate(planes_data.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="plan-card">
                    <h3 style='color:#38bdf8'>{nombre}</h3>
                    <h2 style='margin:0'>{info['p']}</h2>
                    <p><small>{info['t']}</small></p>
                    <hr style='opacity:0.2'>
                    <p><b>{info['l']}</b> Planeaciones</p>
                    <p><b>{info['l']}</b> Escritos</p>
                    <p><b>{info['l']}</b> Evaluación</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Elegir {nombre}"):
                st.balloons()
                # Guardar usuario final
                u = st.session_state.db["temp"]
                st.session_state.db["usuarios"][u["user"]] = {
                    "pass": u["pass"], "name": u["name"], "plan": nombre, "pic": u.get("pic")
                }
                st.success(f"¡Bienvenido, Maestro {u['name']}!")
                time.sleep(2)
                st.session_state.db["step"] = "app"
                st.rerun()
