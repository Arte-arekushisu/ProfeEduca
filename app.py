import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión a Base de Datos
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

# 3. Función de IA Estable (Versión v1)
def generar_planeacion(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Forzamos la ruta v1 para evitar errores de versión beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Eres un tutor experto en el Modelo ABCD de CONAFE. Diseña una planeación para el tema: {tema}. Incluye un Desafío, una Meta y una Ruta de Diálogo."}]
        }]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error de conexión con la IA: {response.status_code}"

# 4. Interfaz de Usuario
st.title("🍎 Planeador ABCD (CONAFE)")
st.info("Generación estable con Gemini 1.5 Flash.")

tema = st.text_input("¿Qué tema vamos a planear hoy?", placeholder="Ej: El ciclo del agua")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("La IA está redactando la propuesta pedagógica..."):
            resultado = generar_planeacion(tema)
            st.session_state['resultado_ia'] = resultado
            st.markdown(resultado)
    else:
        st.warning("Escribe un tema para comenzar.")

# 5. Guardado en Supabase
if 'resultado_ia' in st.session_state and st.button("Guardar en Bitácora"):
    try:
        data = {"meta_semana": st.session_state['resultado_ia']}
        supabase.table("planeaciones").insert(data).execute()
        st.success("✅ ¡Guardado con éxito en tu base de datos!")
        st.balloons()
    except Exception as e:
        st.error(f"Error al guardar: {e}")
