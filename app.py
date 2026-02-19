import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Inicialización de conexiones
def init_connections():
    try:
        # Conexión a Supabase usando los secretos configurados
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error al leer secretos o conectar a Supabase: {e}")
        return None

supabase = init_connections()

# 3. Función para generar contenido con Gemini estable
def generar_con_ia(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Ruta v1 estable para evitar el error 404 de versiones beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Actúa como tutor CONAFE. Para el tema '{tema}', genera un desafío, meta y ruta ABCD."}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error de la IA ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {e}"

# 4. Interfaz de Usuario
st.title("🍎 Planeador ABCD (Gemini Free Tier)")
st.write("Iniciando proyecto con el plan gratuito de Google Gemini.")

tema = st.text_input("¿Qué tema vamos a planear hoy?", placeholder="Ej: Las fracciones")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con la IA..."):
            resultado = generar_con_ia(tema)
            st.session_state['propuesta'] = resultado
            st.markdown(resultado)
    else:
        st.warning("Por favor, escribe un tema.")

# 5. Guardado
if 'propuesta' in st.session_state and st.button("Guardar Planeación"):
    if supabase:
        try:
            supabase.table("planeaciones").insert({"meta_semana": st.session_state['propuesta']}).execute()
            st.success("✅ ¡Guardado con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
