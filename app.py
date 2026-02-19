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

# 3. Función de conexión directa (Sin librerías fallidas)
def generar_planeacion_directa(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Forzamos la versión v1 estable y el modelo Pro para máxima compatibilidad
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={api_key}"
    
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
        # Si falla el Pro, intentamos el Flash como último recurso en la misma ruta
        url_flash = url.replace("gemini-1.5-pro", "gemini-1.5-flash")
        response_flash = requests.post(url_flash, json=payload, headers=headers)
        if response_flash.status_code == 200:
            return response_flash.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

# 4. Interfaz de Usuario
st.title("🍎 Planeador ABCD (Solución Definitiva)")

tema = st.text_input("Ingresa el tema para tu tutoría:")

if st.button("Generar Planeación Ahora"):
    if tema:
        with st.spinner("Conectando directamente con los servidores de Google..."):
            try:
                resultado = generar_planeacion_directa(tema)
                st.session_state['resultado_ia'] = resultado
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Escribe un tema.")

# 5. Guardado
if 'resultado_ia' in st.session_state:
    texto = st.text_area("Resultado:", value=st.session_state['resultado_ia'], height=400)
    
    if st.button("Guardar en mi Bitácora"):
        try:
            supabase.table("planeaciones").insert({"meta_semana": texto}).execute()
            st.success("✅ ¡Guardado con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
