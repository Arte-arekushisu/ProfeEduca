import streamlit as st
import requests
from supabase import create_client

# Configuración básica
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")
st.title("🍎 Profe.Educa: Planeador ABCD")

# 1. Conexión a Base de Datos
def conectar_supabase():
    try:
        if "SUPABASE_URL" in st.secrets:
            return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        return None
    except:
        return None

supabase = conectar_supabase()
if supabase:
    st.success("✅ Conexión establecida.")

# 2. Función de IA (Ruta Universal)
def generar_planeacion(tema):
    if "GEMINI_API_KEY" not in st.secrets:
        return "Error: Configura tu API Key en Secrets."

    api_key = st.secrets["GEMINI_API_KEY"]
    
    # Probamos con la ruta de gemini-pro que es la más estable
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Actúa como experto en el Modelo ABCD de CONAFE. Crea una planeación para el tema: {tema}. Incluye desafío, meta y ruta."}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Google sigue reportando error {response.status_code}. Verifica que tu API Key sea válida en Google AI Studio."
    except Exception as e:
        return f"Error de conexión: {e}"

# 3. Interfaz
tema_input = st.text_input("Escribe el tema:")

if st.button("Generar"):
    if tema_input:
        with st.spinner("Generando..."):
            resultado = generar_planeacion(tema_input)
            st.write(resultado)
