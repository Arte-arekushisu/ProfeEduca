import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎", layout="centered")

# --- CREDENCIALES ---
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# --- CONEXIÓN ---
try:
    # EL CAMBIO CLAVE: transport='rest' evita el error 404 v1beta
    genai.configure(api_key=GOOGLE_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Conexión a Supabase
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.title("🍎 ProfeEduca")
st.markdown("### Generador de Planeaciones Pedagógicas")

tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🚀 Generar y Guardar Planeación"):
    if tema:
        with st.spinner("⏳ La IA está trabajando..."):
            try:
                # Generar contenido
                response = model.generate_content(f"Actúa como un experto pedagogo. Crea una planeación de clase detallada para: {tema}")
                
                if response.text:
                    st.markdown(response.text)
                    
                    # Intentar guardar en base de datos
                    try:
                        supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                        st.success("✅ ¡Guardado con éxito!")
                    except Exception as db_e:
                        st.warning(f"Se generó la clase, pero no se pudo guardar: {db_e}")
                else:
                    st.error("La IA no devolvió texto. Inténtalo de nuevo.")
            except Exception as e:
                # Si esto falla, el error nos dirá exactamente por qué
                st.error(f"Error con la IA: {e}")
    else:
        st.warning("Escribe un tema primero.")
