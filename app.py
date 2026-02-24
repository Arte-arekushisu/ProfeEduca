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

# --- 2. ESTILOS CSS (Estilo Discord + Animación ProfeEduca) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Animación de la Manzana y Gusanito */
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        25% { transform: translate(30px, -45px) scale(1.1); opacity: 1; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
        75% { transform: translate(-30px, -45px) scale(1.1); opacity: 1; }
        90% { transform: translate(-45px, -30px) scale(1); opacity: 0; }
    }
    .apple-container { position: relative; display: inline-block; font-size: 8rem; margin-top: 20px; }
    .worm-icon { position: absolute; font-size: 3rem; animation: worm-move 5s ease-in-out infinite; }
    
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    .slogan { font-style: italic; color: #94a3b8; text-align: center; margin-bottom: 20px; }

    /* Estilo Chat Discord */
    .discord-msg {
        background: #1e293b;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .avatar-chat { border-radius: 50%; width: 40px; height: 40px; border: 2px solid #38bdf8; object-fit: cover; }
    .user-info { color: #38bdf8; font-weight: bold; font-size: 0.9rem; }
    .msg-content { color: #f1f5f9; font-size: 1rem; }
    
    /* Frases Motivacionales */
    .quote-box {
        background: rgba(56, 189, 248, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #38bdf8;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES DE IA (Gemini 2.0 Flash) ---
def generar_frase_diaria():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    prompt = "Genera una frase motivacional corta y poderosa para un maestro de CONAFE que trabaja en comunidades rurales."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Tu labor es la semilla del México del mañana."

# --- 4. INTERFAZ ---
if 'p' not in st.session_state: st.session_state.p = "inicio"

col_menu, col_visual = st.columns([1, 1.8])

with col_menu:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🚀 Menú Maestro")
    if st.button("🏠 Inicio"): st.session_state.p = "inicio"
    if st.button("💬 Chat Comunitario"): st.session_state.p = "chat"
    if st.button("📝 Planeación ABCD"): st.session_state.p = "plan"
    if st.button("📓 Escrito Reflexivo"): st.session_state.p = "reflex"
    st.caption("Ecosistema Digital ProfeEduca © 2026")

with col_visual:
    st.markdown(f"""
        <div style='text-align:center;'>
            <div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>
            <div class="brand-header">📏 ProfeEduca ✏️</div>
            <div class="slogan">"Guía de luz en las comunidades más remotas, transformando cada desafío en una oportunidad para el México del mañana."</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. LÓGICA DE SECCIONES ---
if st.session_state.p == "chat":
    st.subheader("💬 Comunidad ProfeEduca (Estilo Discord)")
    
    # Simulación de sesión (aquí conectarías con los datos de Fase 1)
    # En un caso real, jalaríamos st.session_state.nombre y st.session_state.foto
    user_actual = st.session_state.get('nombre', "Maestro Visitante")
    
    with st.container():
        with st.form("msg_form", clear_on_submit=True):
            nuevo_msg = st.text_input(f"Mensaje como {user_actual}:")
            if st.form_submit_button("Enviar"):
                if nuevo_msg:
                    # Guardar en Supabase (Asegúrate de tener la tabla 'chat')
                    data = {"nombre": user_actual, "mensaje": nuevo_msg, "created_at": str(datetime.now())}
                    supabase.table("chat").insert(data).execute()
        
        st.markdown("---")
        # Mostrar mensajes
        res = supabase.table("chat").select("*").order("created_at", desc=True).limit(10).execute()
        for m in res.data:
            st.markdown(f"""
                <div class="discord-msg">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={m['nombre']}" class="avatar-chat">
                    <div>
                        <div class="user-info">{m['nombre']}</div>
                        <div class="msg-content">{m['mensaje']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.p == "inicio":
    st.subheader("✨ Tu Inspiración Diaria")
    if st.button("Obtener Frase Motivacional"):
        with st.spinner("Conectando con la IA..."):
            frase = generar_frase_diaria()
            st.markdown(f'<div class="quote-box">"{frase}"</div>', unsafe_allow_html=True)
    
    st.info("Bienvenido. Selecciona una opción del menú para comenzar.")
