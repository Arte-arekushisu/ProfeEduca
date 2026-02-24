import streamlit as st
import requests
from supabase import create_client

st.set_page_config(page_title="ProfeEduca Fix", page_icon="🍎")

# --- CREDENCIALES ---
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# Conexión a Supabase
try:
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error en Supabase: {e}")

st.title("🍎 ProfeEduca: Modo Diagnóstico")

tema = st.text_input("¿Qué tema quieres probar?")

if st.button("Generar Planeación"):
    if tema:
        # 1. Definimos la URL (Endpoint estable de Google)
        # Usamos la versión 'v1' en lugar de 'v1beta' para mayor estabilidad
        api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={G_KEY}"
        
        # Mostramos la URL para verificarla (como te sugirieron)
        st.write(f"DEBUG: Conectando a... {api_url.split('?')[0]}") 

        payload = {
            "contents": [{
                "parts": [{"text": f"Crea una planeación educativa corta sobre: {tema}"}]
            }]
        }

        with st.spinner("Llamando a la API..."):
            try:
                response = requests.post(api_url, json=payload)
                
                # Verificamos si la respuesta fue exitosa (Código 200)
                if response.status_code == 200:
                    data = response.json()
                    texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(texto_ia)
                    
                    # Guardar en Supabase
                    supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": texto_ia}).execute()
                    st.success("✅ ¡Funcionó y se guardó!")
                else:
                    # Si da error 404 u otro, mostramos el mensaje real de Google
                    st.error(f"Error {response.status_code}: La API dice que la ruta no es válida.")
                    st.write("Detalle del error:", response.text)
                    
            except Exception as e:
                st.error(f"Error inesperado: {e}")
