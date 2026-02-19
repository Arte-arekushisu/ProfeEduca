import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página (Debe ser la primera línea)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión segura a Base de Datos
@st.cache_resource
def iniciar_db():
    # Esto elimina el KeyError: 'SUPABASE_URL'
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

db = iniciar_db()

# 3. Función de IA estable (Evita el Error 404)
def generar_planeacion(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Ruta v1 de producción: estable y gratuita
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Eres experto en Modelo ABCD CONAFE. Tema: {tema}. Crea desafío, meta y ruta."}]
        }]
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error técnico ({response.status_code}): {response.text}"

# 4. Interfaz
st.title("🍎 Planeador ABCD")
tema = st.text_input("¿Qué tema planeamos?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con Gemini 1.5 Flash..."):
            resultado = generar_planeacion(tema)
            st.session_state['resultado_ia'] = resultado
            st.markdown(resultado)

if 'resultado_ia' in st.session_state and st.button("Guardar en Bitácora"):
    db.table("planeaciones").insert({"meta_semana": st.session_state['resultado_ia']}).execute()
    st.success("✅ ¡Guardado con éxito!")
