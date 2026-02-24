import streamlit as st
from PIL import Image
import base64
import io
import random
import requests
from supabase import create_client, Client

# --- 1. CREDENCIALES (FASE 1) ---
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# Inicializar conexión autónoma a Supabase
supabase: Client = create_client(S_URL, S_KEY)

# --- 2. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="Fase 1: Onboarding ProfeEduca", page_icon="🍎", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .profile-pic { border-radius: 50%; width: 150px; height: 150px; border: 4px solid #38bdf8; box-shadow: 0 0 20px #38bdf866; }
    .stButton>button { border-radius: 10px; background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%); color: white; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE IA (Gemini 1.5 Flash) ---
def ia_asistente_perfil(nombre, contexto):
    """La IA ayuda al maestro a redactar su perfil profesional ABCD"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={G_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Eres un asistente de ProfeEduca. El maestro {nombre} trabaja en {contexto}. Crea una frase de bienvenida inspiradora corta basada en el modelo ABCD de CONAFE."}]}]
    }
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Bienvenido al ecosistema ProfeEduca, transformando la educación comunitaria."

# --- 4. LÓGICA DE LA FASE 1 ---
if 'f1_step' not in st.session_state:
    st.session_state.f1_step = "registro"

st.title("🛡️ Fase 1: Registro e Identidad")

if st.session_state.f1_step == "registro":
    with st.container():
        email = st.text_input("Correo Electrónico para el Expediente")
        nombre = st.text_input("Nombre Completo del Educador")
        contexto = st.selectbox("Nivel de Intervención", ["Preescolar", "Primaria", "Secundaria"])
        
        if st.button("Siguiente: Personalizar Perfil"):
            if email and nombre:
                st.session_state.user_data = {"email": email, "nombre": nombre, "nivel": contexto}
                st.session_state.f1_step = "perfil"
                st.rerun()

elif st.session_state.f1_step == "perfil":
    st.subheader(f"¡Hola, {st.session_state.user_data['nombre']}!")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        foto = st.file_uploader("Sube tu foto profesional", type=['jpg', 'png'])
        if foto:
            st.image(foto, width=150)
            
    with col2:
        st.write("**Asistente IA ProfeEduca:**")
        with st.spinner("Generando mensaje personalizado..."):
            mensaje_ia = ia_asistente_perfil(st.session_state.user_data['nombre'], st.session_state.user_data['nivel'])
            st.info(mensaje_ia)

    if st.button("Finalizar y Guardar en Supabase"):
        # Registro en la base de datos
        try:
            data = {
                "email": st.session_state.user_data['email'],
                "nombre": st.session_state.user_data['nombre'],
                "nivel": st.session_state.user_data['nivel'],
                "mensaje_ia": mensaje_ia
            }
            supabase.table("usuarios_profe_educa").insert(data).execute()
            st.success("¡Fase 1 completada! Datos sincronizados en la nube.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al conectar con Supabase: {e}")
            st.info("Asegúrate de tener creada la tabla 'usuarios_profe_educa' en tu panel de Supabase.")
