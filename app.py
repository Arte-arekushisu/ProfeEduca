import streamlit as st  # <--- ESTA ES LA LÍNEA QUE FALTABA
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq

# --- 1. CONFIGURACIÓN DE LLAVES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="ProfeEduca | Sistema Blindado", page_icon="🍎", layout="wide")

# --- 2. ESTILOS PROFEEDUCA ---
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
    # Intento 1: Gemini
    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_KEY}"
    try:
        res = requests.post(url_gemini, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text'], "Gemini 2.0"
    except:
        pass

    # Intento 2: Groq (Llave desbloqueada)
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content, "Groq (Llama 3.3)"
    except:
        return None, None

# --- 4. FUNCIÓN PDF ---
def crear_pdf(datos, contenido):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"PLANEACIÓN SEMANAL - {datos['inst']}", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.cell(95, 8, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 8, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(190, 8, txt=f"Comunidad: {datos['comunidad']}", border=1, ln=True)
    pdf.ln(10)
    texto_pdf = contenido.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, txt=texto_pdf)
    return pdf.output(dest='S').encode('latin-1')

# --- 5. INTERFAZ ---
st.sidebar.markdown("### 🚀 Panel de Control")
if st.sidebar.button("🏠 Inicio"): st.session_state.p = "inicio"
if st.sidebar.button("📝 Planeaciones ABCD"): st.session_state.p = "plan"

if 'p' not in st.session_state: st.session_state.p = "inicio"

st.markdown('<div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-header">📏 ProfeEduca ✏️</div>', unsafe_allow_html=True)

if st.session_state.p == "plan":
    st.subheader("🗓️ Planeación Semanal Segura")
    with st.expander("Datos Generales", expanded=True):
        c1, c2 = st.columns(2)
        ec = c1.text_input("E.C.")
        eca = c1.text_input("E.C.A.")
        comu = c2.text_input("Comunidad")
        inst = c2.selectbox("Institución", ["CONAFE", "SEP", "Otros"])

    tema = st.text_input("Tema de interés (Semana completa):")

    if st.button("🚀 Generar Planeación"):
        if tema and ec:
            with st.spinner("Buscando IA disponible..."):
                prompt = f"Genera una planeación ABCD SEMANAL para '{tema}'. 4 estaciones, 3 actividades diarias por estación. De Lunes a Viernes."
                res, motor = generar_planeacion_semanal(prompt)
                if res:
                    st.success(f"Generado con {motor}")
                    st.markdown(res)
                    pdf_bytes = crear_pdf({"ec": ec, "eca": eca, "comunidad": comu, "inst": inst}, res)
                    st.download_button("📥 Descargar PDF", data=pdf_bytes, file_name=f"Planeacion_{tema}.pdf")
                else:
                    st.error("Error: Todos los motores están saturados.")
else:
    st.info("Haz clic en 'Planeaciones ABCD' para comenzar.")
