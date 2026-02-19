import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión segura a Supabase
@st.cache_resource
def conectar_base_datos():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error de configuración: {e}")
        return None

supabase = conectar_base_datos()

# 3. Función de IA Estable (Versión v1)
def generar_con_gemini(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Ruta de producción estable
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Actúa como tutor CONAFE experto en el Modelo ABCD. Para el tema '{tema}', genera un desafío, una meta y una ruta de aprendizaje clara."}]
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error técnico: {response.status_code}. Revisa tu clave de Gemini."

# 4. Interfaz de Usuario
st.title("🍎 Planeador ABCD (CONAFE)")
st.write("Generación pedagógica gratuita y estable.")

tema = st.text_input("¿Qué tema vamos a planear hoy?", placeholder="Ej: Las estaciones del año")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con Gemini..."):
            resultado = generar_con_gemini(tema)
            st.session_state['propuesta_guardada'] = resultado
            st.markdown("### Propuesta Generada:")
            st.write(resultado)
    else:
        st.warning("Por favor, escribe un tema primero.")

# 5. Guardado en Supabase
if 'propuesta_guardada' in st.session_state and st.button("Guardar en mi Bitácora"):
    if supabase:
        try:
            # Asegúrate de que la columna se llame 'meta_semana' en tu tabla 'planeaciones'
            supabase.table("planeaciones").insert({"meta_semana": st.session_state['propuesta_guardada']}).execute()
            st.success("✅ ¡Guardado con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}. Verifica que la tabla 'planeaciones' exista.")
