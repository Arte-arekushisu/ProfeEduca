import streamlit as st
import requests
from supabase import create_client

# 1. ESTO DEBE SER LA PRIMERA LÍNEA (Indispensable para evitar NameError)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. INICIALIZACIÓN DE CONEXIONES CON SEGURIDAD
def iniciar_supabase():
    try:
        if "SUPABASE_URL" in st.secrets:
            return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        return None
    except:
        return None

supabase = iniciar_supabase()

# 3. FUNCIÓN DE IA ESTABLE (Evita error 404)
def consultar_ia(tema):
    # Forzamos la versión v1 (estable) para evitar errores de versión beta
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Eres un tutor experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un Desafío inicial, una Meta y una Ruta de Diálogo pedagógico."}]
        }]
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        # Si la API Key falla, mostramos el mensaje claro para corregirla
        error_info = response.json()
        return f"Error técnico: {error_info.get('error', {}).get('message', 'Clave API no válida')}"

# 4. INTERFAZ DE USUARIO
st.title("🍎 Planeador ABCD (CONAFE)")
st.write("Genera propuestas pedagógicas estables y gratuitas.")

if not supabase:
    st.warning("⚠️ Configura 'SUPABASE_URL' en tus Secrets para poder guardar.")

tema = st.text_input("¿Qué tema planeamos hoy?", placeholder="Ej: Las fracciones")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con la IA..."):
            resultado = consultar_ia(tema)
            st.session_state['resultado_ia'] = resultado
            st.markdown(resultado)
    else:
        st.warning("Escribe un tema primero.")

# 5. GUARDADO EN BASE DE DATOS
if 'resultado_ia' in st.session_state and st.button("Guardar en Bitácora"):
    if supabase:
        try:
            supabase.table("planeaciones").insert({"meta_semana": st.session_state['resultado_ia']}).execute()
            st.success("✅ ¡Guardado con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
    else:
        st.error("No se pudo conectar a la base de datos.")
