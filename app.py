import streamlit as st
import requests
from supabase import create_client

# Configuración inicial
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# Conexión a Base de Datos
@st.cache_resource
def conectar_db():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = conectar_db()

# Función de IA (Versión Estable v1)
def generar_planeacion(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Esta URL evita el error 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Eres un experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío, meta y ruta de aprendizaje."}]
        }]
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error técnico: {response.status_code}"

# Interfaz
st.title("🍎 Planeador ABCD")
tema = st.text_input("¿Qué tema planeamos?")

if st.button("Generar"):
    if tema:
        with st.spinner("Generando..."):
            resultado = generar_planeacion(tema)
            st.session_state['resultado'] = resultado
            st.write(resultado)

if 'resultado' in st.session_state and st.button("Guardar"):
    supabase.table("planeaciones").insert({"meta_semana": st.session_state['resultado']}).execute()
    st.success("✅ ¡Guardado!")
