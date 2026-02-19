import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página (Obligatorio al inicio)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión a Base de Datos
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"Error en base de datos: {e}")

# 3. Función de Conexión Directa Estable (Sin errores 404)
def generar_con_gemini_estable(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Usamos la ruta v1 que es la versión de producción estable
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Actúa como tutor CONAFE experto. Para el tema '{tema}', genera un desafío, meta y ruta de aprendizaje ABCD."}]
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error {response.status_code}: {response.text}"

# 4. Interfaz de Usuario
st.title("🍎 Planeador ABCD (Gemini Free Tier)")
st.info("Iniciando proyecto con el plan gratuito de Google Gemini.")

tema = st.text_input("¿Qué tema vamos a planear hoy?", placeholder="Ej: Las fracciones")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con Gemini 1.5 Flash (Versión Estable)..."):
            try:
                resultado = generar_con_gemini_estable(tema)
                st.session_state['resultado_ia'] = resultado
                st.markdown(resultado)
            except Exception as e:
                st.error(f"Hubo un detalle: {e}")
    else:
        st.warning("Escribe un tema para comenzar.")

# 5. Guardado en Supabase
if 'resultado_ia' in st.session_state and st.button("Guardar Planeación"):
    try:
        supabase.table("planeaciones").insert({"meta_semana": st.session_state['resultado_ia']}).execute()
        st.success("✅ ¡Guardado con éxito en tu bitácora!")
        st.balloons()
    except Exception as e:
        st.error(f"No se pudo guardar: {e}")
