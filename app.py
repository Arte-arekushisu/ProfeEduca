import streamlit as st
import requests
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN Y CREDENCIALES ---
# Usamos Gemini 2.0 Flash para una respuesta más rápida y precisa en esta fase
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

st.set_page_config(page_title="ProfeEduca F2: Menú Maestro", page_icon="🍎", layout="wide")

# Inicializar Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. ESTILOS CSS (Corregidos para evitar el SyntaxError) ---
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
    .apple-container { position: relative; display: inline-block; font-size: 8rem; margin-top: 50px; }
    .worm-icon { position: absolute; font-size: 3rem; animation: worm-move 5s ease-in-out infinite; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-shadow: 0 0 15px rgba(56, 189, 248, 0.4); text-align: center; }
    .stButton>button { text-align: left; padding: 15px; background: transparent; color: #f8fafc; border: none; border-bottom: 1px solid rgba(56, 189, 248, 0.2); width: 100%; }
    .stButton>button:hover { background: rgba(56, 189, 248, 0.1); color: #38bdf8; border-bottom: 1px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MOTOR DE IA: GEMINI 2.0 FLASH ---
def ia_menu_maestro(rol, consulta):
    # Endpoint específico para Gemini 2.0 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Contexto: Modelo ABCD CONAFE. Rol: {rol}. Tarea: {consulta}"
            }]
        }]
    }
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "La IA está descansando. Por favor, intenta de nuevo en unos segundos."

# --- 4. DISEÑO DE INTERFAZ ---
if 'p' not in st.session_state: st.session_state.p = "inicio"

col_menu, col_visual = st.columns([1, 1.5])

with col_menu:
    st.title("🚀 Menú Maestro")
    if st.button("🏠 Inicio"): st.session_state.p = "inicio"
    if st.button("📝 Planeación ABCD"): st.session_state.p = "plan"
    if st.button("📓 Escrito Reflexivo"): st.session_state.p = "reflexivo"
    if st.button("📅 Diario del Maestro"): st.session_state.p = "diario"
    st.caption("Ecosistema Digital ProfeEduca © 2026")

with col_visual:
    st.markdown(f"""
        <div style='text-align:center;'>
            <div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>
            <div class="brand-header">📏 ProfeEduca ✏️</div>
            <p><b>INTELIGENCIA ARTIFICIAL: GEMINI 2.0 FLASH</b></p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. LÓGICA DE LAS SECCIONES ---
if st.session_state.p == "plan":
    st.subheader("📝 Generador de Planeación con Gemini 2.0")
    tema = st.text_input("Ingresa el tema pedagógico:")
    if st.button("Generar Secuencia ABCD"):
        with st.spinner("Diseñando planeación..."):
            resultado = ia_menu_maestro("Experto en Planeación", f"Diseña una secuencia de aprendizaje sobre {tema}")
            st.info(resultado)

elif st.session_state.p == "reflexivo":
    st.subheader("📓 Análisis de Escrito Reflexivo")
    reflexion = st.text_area("Comparte tu experiencia del día:")
    if st.button("Analizar con IA"):
        with st.spinner("Analizando profundidad pedagógica..."):
            resultado = ia_menu_maestro("Mentor de CONAFE", f"Analiza esta reflexión y dame 2 sugerencias: {reflexion}")
            st.success(resultado)

elif st.session_state.p == "inicio":
    st.write("Selecciona una opción del menú lateral para activar la IA.")
