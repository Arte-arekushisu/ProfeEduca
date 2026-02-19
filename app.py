import streamlit as st
import requests
from supabase import create_client

# Configuración inicial básica
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# Conexión a Base de Datos
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def generar_con_ia(tema_clase):
    # Usamos Gemini 1.5 Pro que es más estable actualmente
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={st.secrets['GEMINI_API_KEY']}"
    
    # Estructura de mensaje simplificada
    payload = {
        "contents": [{
            "parts": [{"text": f"Como experto en CONAFE, crea un desafío, meta y ruta ABCD para: {tema_clase}"}]
        }]
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error técnico: {response.status_code}"

# Interfaz
st.title("🍎 Planeador ABCD (Estable)")
tema = st.text_input("¿Qué tema planeamos?")

if st.button("Generar"):
    if tema:
        with st.spinner("Conectando..."):
            resultado = generar_con_ia(tema)
            st.session_state['resultado'] = resultado
            st.write(resultado)

if 'resultado' in st.session_state and st.button("Guardar"):
    supabase.table("planeaciones").insert({"meta_semana": st.session_state['resultado']}).execute()
    st.success("✅ ¡Guardado!")
