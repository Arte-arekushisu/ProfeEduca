import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Configuración
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# 2. Credenciales (Asegúrate de que la API KEY sea la NUEVA que generaste)
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# 3. Conexión Forzada a Versión Estable
try:
    # Esta línea es la que quita el error 404 de raíz
    genai.configure(api_key=GEMINI_KEY, transport='rest') 
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error de configuración: {e}")

# 4. Interfaz
st.title("🍎 ProfeEduca")
tema = st.text_input("Tema de la clase:")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con el cerebro de Google..."):
            try:
                # Intento de generación
                response = model.generate_content(f"Planeación para: {tema}")
                st.write(response.text)
                
                # Intento de guardado
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("Guardado en la nube")
            except Exception as e:
                st.error(f"Error técnico: {e}")
