import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página (Indispensable al inicio)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Inicialización de Supabase
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"Error de conexión con la base de datos: {e}")
    st.stop()

# 3. Función de Conexión Directa (Evita el error 404 de v1beta)
def llamar_gemini_estable(prompt_text):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Forzamos la URL a la versión v1 estable
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# 4. Interfaz Modelo ABCD
st.title("🍎 Planeación Modelo ABCD (CONAFE)")
st.write("Generación de tutorías mediante diálogo pedagógico.")

tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej: Ciclo del agua")

if st.button("Generar Desafío ABCD"):
    if tema:
        with st.spinner("Conectando directamente con Gemini v1 estable..."):
            try:
                instruccion = (f"Actúa como tutor CONAFE. Para el tema '{tema}', "
                              f"genera un Desafío, una Meta y una Ruta de aprendizaje ABCD.")
                resultado = llamar_gemini_estable(instruccion)
                st.session_state['resultado_ia'] = resultado
            except Exception as e:
                st.error(f"La IA no pudo responder: {e}")
    else:
        st.warning("Escribe un tema primero.")

# 5. Mostrar y Guardar
if 'resultado_ia' in st.session_state:
    texto_final = st.text_area("Resultado de la IA:", value=st.session_state['resultado_ia'], height=300)
    
    if st.button("Guardar Planeación"):
        try:
            supabase.table("planeaciones").insert({"meta_semana": texto_final}).execute()
            st.success("✅ Guardado correctamente en Supabase.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
