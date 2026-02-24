import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq

# --- 1. CONFIGURACIÓN DE LLAVES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="ProfeEduca | Sistema Blindado", page_icon="🍎", layout="wide")

# --- 2. ESTILOS PROFEEDUCA (Fondo y Animación) ---
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
    .apple-container { position: relative; display: inline-block; font-size: 6rem; text-align: center; width: 100%; }
    .worm-icon { position: absolute; font-size: 2.5rem; animation: worm-move 5s ease-in-out infinite; left: 50%; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE INTELIGENCIA HÍBRIDA ---
def generar_planeacion_semanal(prompt):
    # Intento 1: Gemini (Principal)
    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_KEY}"
    try:
        res = requests.post(url_gemini, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text'], "Gemini 2.0"
    except:
        pass

    # Intento 2: Groq (Emergencia con tu llave)
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500
        )
        return completion.choices[0].message.content, "Groq (Llama 3.3)"
    except Exception as e:
        return None, None

# --- 4. FUNCIÓN PDF ---
def crear_pdf(datos, contenido):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"PLANEACIÓN SEMANAL ABCD - {datos['inst']}", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.cell(95, 8, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 8, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(190, 8, txt=f"Comunidad: {datos['comunidad']} | Período: 1 Semana", border=1, ln=True)
    pdf.ln(10)
    # Limpieza de caracteres para el PDF
    texto_pdf = contenido.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, txt=texto_pdf)
    return pdf.output(dest='S').encode('latin-1')

# --- 5. ESTRUCTURA VISUAL ---
st.sidebar.markdown("### 🚀 Navegación")
if st.sidebar.button("🏠 Inicio"): st.session_state.p = "inicio"
if st.sidebar.button("📝 Planeaciones ABCD"): st.session_state.p = "plan"

if 'p' not in st.session_state: st.session_state.p = "inicio"

# Encabezado con manzana
st.markdown('<div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-header">📏 ProfeEduca ✏️</div>', unsafe_allow_html=True)

st.divider()

if st.session_state.p == "plan":
    st.subheader("🗓️ Planeación Semanal (4 Estaciones)")
    
    with st.expander("📝 Datos Generales", expanded=True):
        c1, c2 = st.columns(2)
        ec_val = c1.text_input("E.C.")
        eca_val = c1.text_input("E.C.A.")
        comu_val = c2.text_input("Comunidad")
        inst_val = c2.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        rinc_val = st.text_input("Rincón Permanente")

    tema_val = st.text_input("Tema central para la semana:")

    if st.button("🚀 Planeaciones ABCD"):
        if tema_val and ec_val:
            with st.spinner("Generando planeación semanal..."):
                prompt_pedagogico = f"""
                Genera una planeación ABCD SEMANAL para '{tema_val}'. 
                Estructura: 4 estaciones con 3 actividades diarias cada una.
                Distribución: Lunes a Viernes.
                Campos Formativos: Lenguajes, Saberes, Ética, De lo Humano.
                Finaliza con una sugerencia de Demostración Pública para el viernes.
                """
                resultado, motor = generar_planeacion_semanal(prompt_pedagogico)
                
                if resultado:
                    st.success(f"¡Listo! Motor: {motor}")
                    st.markdown(resultado)
                    pdf_bytes = crear_pdf({"ec": ec_val, "eca": eca_val, "comunidad": comu_val, "inst": inst_val}, resultado)
                    st.download_button("📥 Descargar PDF Semanal", data=pdf_bytes, file_name=f"Semana_{tema_val}.pdf")
                else:
                    st.error("🚨 Todos los motores saturados. Intenta de nuevo en un minuto.")
else:
    st.markdown("### 👋 ¡Bienvenido al Generador Inteligente!")
    st.write("Selecciona **Planeaciones ABCD** en el menú lateral para empezar a planear tu semana sin interrupciones.")
