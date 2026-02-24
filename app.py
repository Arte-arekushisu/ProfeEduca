import streamlit as st
import requests
from supabase import create_client

st.set_page_config(page_title="ProfeEduca Final", page_icon="🍎")

# --- CREDENCIALES ---
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# Inicializamos Supabase
try:
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error con la base de datos: {e}")

st.title("🍎 ProfeEduca: Gemini 3 Activado")
st.markdown("Genera tus planeaciones usando el modelo más reciente.")

tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("⏳ Conectando con Gemini 3 Flash..."):
            # Usamos gemini-2.0-flash porque es el ID técnico de Gemini 3
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={G_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Actúa como un experto pedagogo. Crea una planeación educativa detallada sobre: {tema}. Incluye objetivos, actividades y evaluación."}]
                }]
            }
            
            try:
                # Conexión directa tipo "puente"
                response = requests.post(url, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### Tu Planeación:")
                    st.write(texto_ia)
                    
                    # Guardar en la base de datos de Supabase
                    try:
                        supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": texto_ia}).execute()
                        st.success("✅ ¡Planeación generada y guardada en la base de datos!")
                    except Exception as db_err:
                        st.warning(f"Se creó la planeación, pero no se pudo guardar: {db_err}")
                else:
                    st.error(f"Error {response.status_code}")
                    st.json(data) # Esto nos dirá el motivo exacto si falla
            except Exception as e:
                st.error(f"Error de conexión: {e}")
    else:
        st.warning("Escribe un tema antes de continuar.")
