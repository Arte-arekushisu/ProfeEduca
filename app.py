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
    # Configuramos Google para evitar el error 404
    genai.configure(api_key=GOOGLE_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Conexión simplificada a Supabase para evitar el error 'proxy'
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.title("🍎 ProfeEduca")
st.markdown("### Generador de Planeaciones Pedagógicas")

tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🚀 Generar y Guardar Planeación"):
    if tema:
        with st.spinner("⏳ Creando planeación..."):
            try:
                # Generar con Gemini
                response = model.generate_content(f"Plan de clase detallado sobre: {tema}")
                
                if response.text:
                    st.markdown(response.text)
                    # Guardar en base de datos
                    try:
                        supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                        st.success("✅ ¡Guardado en la base de datos!")
                    except Exception as db_e:
                        st.warning(f"Se creó la planeación, pero no se guardó: {db_e}")
            except Exception as e:
                st.error(f"Error con la IA: {e}")
