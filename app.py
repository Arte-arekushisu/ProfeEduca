import streamlit as st
import requests
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN ---
# Usamos Gemini 1.5 Pro para mayor capacidad de redacción extensa
IA_MODEL = "gemini-1.5-pro" 
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

st.set_page_config(page_title="ProfeEduca F3: Generador", page_icon="📝", layout="wide")

# --- 2. MOTOR DE GENERACIÓN EXTENSA ---
def generar_documento_abcd(tema, nivel, contexto):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{IA_MODEL}:generateContent?key={GEMINI_KEY}"
    
    prompt = f"""
    Actúa como un Asesor Pedagógico Senior experto en el Modelo ABCD de CONAFE.
    Genera una UNIDAD DE APRENDIZAJE INTEGRAL para el tema: {tema}.
    Nivel: {nivel}.
    Contexto comunitario: {contexto}.
    
    El documento debe incluir:
    1. Propósito General.
    2. Desafío (Pregunta generadora).
    3. Trayecto de Aprendizaje (Pasos detallados).
    4. Sugerencias de evaluación formativa.
    5. Espacio para Registro de Proceso de Aprendizaje (RPA).
    
    Usa un lenguaje profesional pero cercano al contexto rural mexicano.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error: La IA ha alcanzado su límite gratuito temporal. Intenta en un momento."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='color: #38bdf8;'>📝 Generador de Unidades ABCD</h1>", unsafe_allow_html=True)
st.write("Crea documentos pedagógicos extensos y personalizados con IA avanzada.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        tema_input = st.text_input("¿Qué tema quieres enseñar? (ej. Ecosistemas, Revolución Mexicana)")
        nivel_input = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria Menor", "Primaria Mayor", "Secundaria"])
    with col2:
        contexto_input = st.text_area("Breve descripción de tu comunidad (contexto rural):")

if st.button("🚀 Generar Documento Completo"):
    if tema_input and contexto_input:
        with st.spinner("La IA está redactando tu documento... esto puede tardar unos segundos debido a la extensión."):
            documento = generar_documento_abcd(tema_input, nivel_input, contexto_input)
            st.markdown("---")
            st.markdown("### 📄 Resultado de la Planeación")
            st.write(documento)
            
            # Botón para descargar como texto
            st.download_button("📥 Descargar Planeación", documento, file_name=f"Planeacion_{tema_input}.txt")
    else:
        st.warning("Por favor, llena los campos de tema y contexto.")

st.divider()
st.caption("ProfeEduca Fase 3 | Impulsado por Gemini 1.5 Pro")
