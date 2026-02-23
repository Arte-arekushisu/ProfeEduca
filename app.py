import streamlit as st
import google.generativeai as genai
from supabase import create_client

# Configuración inicial
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# LLAVES: Asegúrate de que GEMINI_KEY sea la nueva que generaste hoy
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

try:
    # Esta línea configura la conexión estable para evitar el 404
    genai.configure(api_key=GEMINI_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error de inicio: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("Tema de la clase:")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con la IA..."):
            try:
                # Generación de contenido
                response = model.generate_content(f"Crea una planeación para: {tema}")
                st.write(response.text)
                # Guardado en base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ ¡Guardado!")
            except Exception as e:
                st.error(f"Error técnico: {e}")
