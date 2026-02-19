import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página (ESTO DEBE SER LA LÍNEA 1)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

st.title("🍎 Profe.Educa: Planeador ABCD")

# 2. Verificación de Secretos
if "SUPABASE_URL" not in st.secrets or "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Faltan las llaves en los Secrets de Streamlit Cloud.")
    st.info("Ve a Settings > Secrets y asegúrate de haber pegado las llaves.")
    st.stop()

# 3. Conexión a Base de Datos
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    st.success("✅ Conexión con la base de datos establecida.")
except Exception as e:
    st.error(f"❌ Error al conectar con Supabase: {e}")

# 4. Función de IA (URL Corregida para evitar el 404)
def generar_planeacion(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": f"Eres un experto en el Modelo ABCD de CONAFE. Crea una planeación para el tema: {tema}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error de la IA ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {e}"

# 5. Interfaz de Usuario
tema = st.text_input("Escribe el tema de tu tutoría:")

if st.button("Generar Desafío y Meta"):
    if tema:
        with st.spinner("La IA está pensando..."):
            resultado = generar_planeacion(tema)
            st.session_state['resultado'] = resultado
            st.markdown("### Resultado:")
            st.write(resultado)
    else:
        st.warning("Escribe un tema primero.")
