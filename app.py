import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca Universal", page_icon="🍎")

# --- CREDENCIALES ---
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# --- CONEXIÓN UNIVERSAL ---
try:
    # Esta configuración ignora la ruta v1beta que causa el error 404
    genai.configure(api_key=G_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.title("🍎 ProfeEduca: Generador Universal")

tema = st.text_input("Escribe el tema para tu planeación:")

if st.button("Generar Contenido"):
    if tema:
        with st.spinner("Conectando con la IA por ruta segura..."):
            try:
                # Generamos contenido usando la ruta estable
                response = model.generate_content(f"Crea una planeación educativa sobre: {tema}")
                
                if response.text:
                    st.markdown(response.text)
                    # Guardar en base de datos
                    try:
                        supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                        st.success("✅ Guardado en Supabase correctamente")
                    except Exception as db_e:
                        st.warning(f"Planeación creada, pero error al guardar: {db_e}")
            except Exception as e:
                # Si esto falla, el código nos dirá si es por la ruta o por la llave
                st.error(f"Aviso de ruta: {e}")
