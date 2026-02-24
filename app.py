import streamlit as st
import requests
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN Y CREDENCIALES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

st.set_page_config(page_title="ProfeEduca | Fase 2", page_icon="🍎", layout="wide")

# Inicializar Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. ESTILOS CSS ---
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
    .apple-container { position: relative; display: inline-block; font-size: 8rem; margin-top: 20px; }
    .worm-icon { position: absolute; font-size: 3rem; animation: worm-move 5s ease-in-out infinite; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-shadow: 0 0 15px rgba(56, 189, 248, 0.4); text-align: center; }
    .slogan { font-style: italic; color: #94a3b8; text-align: center; max-width: 600px; margin: auto; }
    .chat-box { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #38bdf8; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES DE IA ---
def consultar_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Sigue adelante, maestro. ¡Tu labor es valiosa!"

# --- 4. INTERFAZ Y MENÚ ---
if 'p' not in st.session_state: st.session_state.p = "inicio"

col_menu, col_visual = st.columns([1, 1.5])

with col_menu:
    st.title("🚀 Menú Maestro")
    if st.button("🏠 Inicio"): st.session_state.p = "inicio"
    if st.button("💬 Chat Comunitario"): st.session_state.p = "chat"
    if st.button("✨ Frases Motivacionales"): st.session_state.p = "frases"
    if st.button("📝 Planeación ABCD"): st.session_state.p = "plan"
    st.caption("Ecosistema Digital ProfeEduca © 2026")

with col_visual:
    st.markdown("""<div style='text-align:center;'>
        <div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>
        <div class="brand-header">📏 ProfeEduca ✏️</div>
        <div class="slogan">"Guía de luz en las comunidades más remotas, transformando cada desafío en una oportunidad para el México del mañana."</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# --- 5. LÓGICA DE SECCIONES ---
if st.session_state.p == "chat":
    st.subheader("💬 Convivencia: Chat de Maestros")
    with st.form("form_chat", clear_on_submit=True):
        msg = st.text_input("Comparte un mensaje con la comunidad:")
        if st.form_submit_button("Enviar Mensaje"):
            supabase.table("chat_comunitario").insert({"mensaje": msg}).execute()
            st.success("Mensaje compartido!")
    
    st.markdown("### Mensajes Recientes:")
    mensajes = supabase.table("chat_comunitario").select("*").order("created_at", desc=True).limit(10).execute()
    for m in mensajes.data:
        st.markdown(f"<div class='chat-box'><b>Maestro:</b> {m['mensaje']}</div>", unsafe_allow_html=True)

elif st.session_state.p == "frases":
    st.subheader("✨ Motivación Diaria")
    if st.button("Generar Frase Inspiradora"):
        with st.spinner("La IA está creando algo para ti..."):
            frase = consultar_gemini("Genera una frase corta y poderosa de motivación para un maestro rural en México.")
            st.info(frase)

elif st.session_state.p == "plan":
    st.subheader("📝 Planeación con IA")
    tema = st.text_input("Tema a planear:")
    if st.button("Generar"):
        res = consultar_gemini(f"Crea una planeación ABCD para el tema: {tema}")
        st.write(res)

elif st.session_state.p == "inicio":
    st.write("Bienvenido al corazón de ProfeEduca. Selecciona una opción para comenzar.")
