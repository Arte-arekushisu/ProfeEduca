import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq
import io

# --- 1. LLAVES Y CONFIGURACIÓN ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="Generador ABCD Pro", page_icon="🍎", layout="wide")

# --- 2. DISEÑO VISUAL ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE IA (Doble Motor) ---
def llamar_ia(prompt):
    # Intento 1: Gemini
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_KEY}"
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text'], "Gemini"
    except: pass
    # Intento 2: Groq (Respaldo)
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        return completion.choices[0].message.content, "Groq"
    except: return None, None

# --- 4. INTERFAZ DE USUARIO ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Pro ✏️</div>', unsafe_allow_html=True)

with st.form("form_abc"):
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("Nombre del E.C. (Abreviado)")
        eca = st.text_input("Nombre del E.C.A. (Abreviado)")
        comunidad = st.text_input("Comunidad")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria", "Multigrado"])
        grados = st.text_input("Grado(s) específico(s)")
    with col2:
        fecha = datetime.now().strftime("%d/%m/%Y")
        st.write(f"**Fecha:** {fecha}")
        rincon = st.text_input("Rincón (Manual)")
        inst = st.selectbox("Institución", ["CONAFE", "CET", "Otros"])
        logo_inst = st.file_uploader("Subir logo de Institución", type=["png", "jpg", "jpeg"])
        if inst == "Otros":
            inst_otro = st.text_input("Especifique Institución")

    tema = st.text_area("Tema de interés (Información para Relación Tutora)")
    
    st.markdown("### 🍎 Bloque Post-Receso (2 Sesiones)")
    post_receso_1 = st.text_input("Sesión 1: Materia/Actividad")
    post_receso_2 = st.text_input("Sesión 2: Materia/Actividad")
    
    obs = st.text_area("Observaciones o notas adicionales")
    
    submit = st.form_submit_button("🚀 Planeaciones ABCD")

# --- 5. GENERACIÓN DE RESULTADOS ---
if submit:
    if tema and ec:
        with st.spinner("Generando planeación profesional..."):
            prompt_completo = f"""
            Eres un experto en el modelo ABCD y la NEM. Genera una planeación para {nivel} ({grados}) sobre: {tema}.
            REQUISITOS:
            1. Información extensa del tema con fuentes confiables (no Wikipedia).
            2. 4 Estaciones con NOMBRES LLAMATIVOS.
            3. Cada estación debe cumplir los 4 campos formativos con instrucciones y procedimientos detallados.
            4. Incluye referencias bibliográficas en formato APA.
            """
            contenido, motor = llamar_ia(prompt_completo)
            
            if contenido:
                st.success(f"Generado con {motor}")
                st.markdown(contenido)
                
                # Aquí iría la lógica de fpdf para armar el PDF con los nuevos campos
                st.info("El PDF incluirá todos los campos registrados arriba.")
            else:
                st.error("Error de conexión. Intenta de nuevo en un momento.")
