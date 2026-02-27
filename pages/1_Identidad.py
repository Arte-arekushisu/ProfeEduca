import streamlit as st
import requests
import re
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN Y CREDENCIALES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

st.set_page_config(page_title="ProfeEduca | Menú Maestro", page_icon="🍎", layout="wide")

# Inicializar Chat Temporal (Memoria volátil)
if 'chat_grupal' not in st.session_state:
    st.session_state.chat_grupal = []

# --- 2. FILTRO DE SEGURIDAD (Reglas del Chat) ---
def filtro_seguridad(texto):
    # Detectar números de cuenta/celular (patrones de 8-16 dígitos)
    if re.search(r'\d{8,}', texto):
        return False, "⚠️ Bloqueado: No compartas números de teléfono o cuentas bancarias."
    # Detectar posibles correos/usuarios
    if "@" in texto or "http" in texto:
        return False, "⚠️ Bloqueado: No compartas enlaces o correos electrónicos."
    return True, texto

# --- 3. ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        25% { transform: translate(30px, -45px) scale(1.1); opacity: 1; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
        75% { transform: translate(-30px, -45px) scale(1.1); opacity: 1; }
        90% { transform: translate(-45px, -30px) scale(1); opacity: 0; }
    }
    .apple-container { position: relative; display: inline-block; font-size: 8rem; margin-top: 10px; }
    .worm-icon { position: absolute; font-size: 3rem; animation: worm-move 5s ease-in-out infinite; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    
    /* Estilo Discord Temporal */
    .msg-discord { background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; display: flex; align-items: center; gap: 15px; border-left: 4px solid #38bdf8; }
    .avatar-mini { border-radius: 50%; width: 40px; height: 40px; border: 2px solid #38bdf8; }
    .user-tag { color: #38bdf8; font-weight: bold; font-size: 0.85rem; }
    
    /* Caja Motivacional Predeterminada */
    .quote-box { background: rgba(56, 189, 248, 0.05); padding: 25px; border-radius: 15px; border: 1px dashed #38bdf8; text-align: center; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 4. MOTOR DE IA: GEMINI 2.0 FLASH ---
def ia_frase_diaria():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": "Dame una frase de 10 palabras que motive a un maestro de educación rural hoy."}]}]}
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Tu labor es la luz de la comunidad hoy."

# --- 5. INTERFAZ Y NAVEGACIÓN ---
if 'p' not in st.session_state: st.session_state.p = "inicio"

col_menu, col_visual = st.columns([1, 2])

with col_menu:
    st.markdown("### 🚀 Panel Maestro")
    if st.button("🏠 Inicio"): st.session_state.p = "inicio"
    if st.button("💬 Chat Comunitario"): st.session_state.p = "chat"
    if st.button("📝 Planeación ABCD"): st.session_state.p = "plan"
    st.caption("Ecosistema Digital ProfeEduca © 2026")

with col_visual:
    st.markdown(f"""
        <div style='text-align:center;'>
            <div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>
            <div class="brand-header">📏 ProfeEduca ✏️</div>
            <div style="color: #94a3b8; font-style: italic; font-size: 0.9rem;">"Transformando desafíos en oportunidades en cada comunidad."</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 6. SECCIONES ---
if st.session_state.p == "inicio":
    st.subheader("✨ Tu Frase Motivacional")
    # Aparece automáticamente al cargar
    frase = ia_frase_diaria()
    st.markdown(f'<div class="quote-box"><h3>"{frase}"</h3></div>', unsafe_allow_html=True)
    st.info("Utiliza el menú lateral para navegar por las herramientas.")

elif st.session_state.p == "chat":
    st.subheader("💬 Chat Grupal (Seguro y Temporal)")
    st.markdown("🚫 **Reglas:** No números de teléfono, cuentas bancarias, usuarios o contraseñas.")
    
    # Nombre del usuario (de la Fase 1 o por defecto)
    nombre_user = st.session_state.get('nombre', "Maestro")
    
    # Formulario de Chat
    with st.form("chat_input", clear_on_submit=True):
        mensaje_texto = st.text_input(f"Mensaje como {nombre_user}:")
        enviar = st.form_submit_button("Enviar")
        
        if enviar and mensaje_texto:
            es_seguro, resultado = filtro_seguridad(mensaje_texto)
            if es_seguro:
                st.session_state.chat_grupal.insert(0, {"user": nombre_user, "msg": resultado})
            else:
                st.error(resultado)

    # Mostrar mensajes temporales
    for m in st.session_state.chat_grupal:
        st.markdown(f"""
            <div class="msg-discord">
                <img src="https://api.dicebear.com/7.x/identicon/svg?seed={m['user']}" class="avatar-mini">
                <div>
                    <div class="user-tag">{m['user']}</div>
                    <div style="color:white;">{m['msg']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.p == "plan":
    st.subheader("📝 Generador de Planeación con IA")
    tema = st.text_input("Tema de la clase:")
    if st.button("Generar"):
        st.write(f"Procesando planeación para: {tema}...")
