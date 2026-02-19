import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de la página
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

st.title("🍎 Profe.Educa: Planeador ABCD")

# 2. Inicialización de servicios con manejo de errores
def conectar_supabase():
    try:
        if "SUPABASE_URL" in st.secrets:
            return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        return None
    except Exception as e:
        st.error(f"Error en base de datos: {e}")
        return None

supabase = conectar_supabase()
if supabase:
    st.success("✅ Conexión con la base de datos establecida.")

# 3. Función de IA - VERSIÓN ESTABLE v1
def generar_planeacion(tema):
    if "GEMINI_API_KEY" not in st.secrets:
        return "Error: No se encontró la GEMINI_API_KEY en Secrets."

    api_key = st.secrets["GEMINI_API_KEY"]
    
    # URL CAMBIADA A v1 (La versión estable que pide el error 404)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Actúa como tutor CONAFE experto en el Modelo ABCD. Crea una planeación para el tema: {tema}. Incluye desafío, meta y ruta de aprendizaje."}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error de Google ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {e}"

# 4. Interfaz de usuario
tema_input = st.text_input("Escribe el tema de tu tutoría:", placeholder="Ej. El ciclo del agua")

if st.button("Generar Desafío y Meta"):
    if tema_input:
        with st.spinner("Generando contenido pedagógico..."):
            resultado = generar_planeacion(tema_input)
            st.markdown("### Resultado:")
            st.write(resultado)
    else:
        st.warning("Por favor, introduce un tema.")
