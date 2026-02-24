import streamlit as st
import requests
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN Y CREDENCIALES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

st.set_page_config(page_title="ProfeEduca | Fase 2", page_icon="🍎", layout="wide")

# Inicializar Chat Temporal (Memoria volátil: se borra al refrescar)
if 'chat_grupal' not in st.session_state:
    st.session_state.chat_grupal = []

# --- 2. ESTILOS CSS (CORREGIDOS) ---
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
    .slogan-text { font-style: italic; color: #94a3b8; text-align: center; font-size: 0.9rem; margin-bottom: 20px; }
    
    /* Estilo Discord Temporal */
    .msg-discord { background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; display: flex; align-items: center; gap: 15px; border-left: 4px solid #38bdf8; }
    .avatar-mini { border-radius: 50%; width: 40px; height: 40px; border: 2px solid #38bdf8; }
    .user-tag { color: #38bdf8; font-weight: bold; font-size: 0.85rem; }
    
    /* Caja Motivacional */
    .quote-box { background: rgba(56, 189, 248, 0.05); padding: 25px; border-radius: 15px; border: 1px dashed #38bdf8; text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE IA (Gemini 2.0 Flash - Automático) ---
def obtener_frase_predeterminada():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": "Dame una frase motivadora corta para un docente de CONAFE."}]}]}
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Tu labor es la luz de la comunidad."

# --- 4. INTERFAZ Y NAVEGACIÓN ---
if 'p' not in st.session_state: st.session_state.p = "inicio"

col_menu, col_visual = st.columns([1, 2])

with col_menu:
    st.markdown("### 🚀 Panel Maestro")
    if st.button("🏠 Inicio"): st.session_state.p = "inicio"
    if st.button("💬 Chat Grupal (Temporal)"): st.session_state.p = "chat"
    if st.button("📝 Planeación ABCD"): st.session_state.p = "plan"
    st.caption("ProfeEduca 2026 | Sistema Autónomo")

with col_visual:
    st.markdown(f"""
        <div style='text-align:center;'>
            <div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>
            <div class="brand-header">📏 ProfeEduca ✏️</div>
            <div class="slogan-text">"Guía de luz en las comunidades más remotas, transformando cada desafío en una oportunidad para el México del mañana."</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. SECCIONES ---
if st.session_state.p == "inicio":
    st.subheader("✨ Inspiración para hoy")
    # La frase aparece por defecto al entrar
    frase_hoy = obtener_frase_predeterminada()
    st.markdown(f'<div class="quote-box"><h3>"{frase_hoy}"</h3></div>', unsafe_allow_html=True)
    st.info("💡 Consejo: Usa el menú de la izquierda para generar planeaciones o convivir en el chat.")

elif st.session_state.p == "chat":
    st.subheader("💬 Chat Grupal Temporal")
    st.warning("⚠️ Mensajes temporales: se borrarán si reinicias la página.")
    
    # Nombre del usuario (viene de la fase 1 o genérico)
    nombre_usuario = st.session_state.get('nombre', "Maestro")
    
    with st.form("chat_form", clear_on_submit=True):
        input_msg = st.text_input(f"Mensaje como {nombre_usuario}:")
        if st.form_submit_button("Enviar"):
            if input_msg:
                # Insertar al inicio de la lista temporal
                st.session_state.chat_grupal.insert(0, {"user": nombre_usuario, "msg": input_msg})
                st.rerun()

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
