import streamlit as st
import google.generativeai as genai
from supabase import create_client
import re

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- CREDENCIALES ---
# 1. Pega tu API Key de Google AI Studio aquí
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# 2. Pega los datos de Supabase (Asegúrate de que sean los correctos)
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# --- CONFIGURACIÓN ---
try:
    # Configuración de Google (Evita el error 404)
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Configuración de Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error en las llaves: {e}")

# --- INTERFAZ ---
st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué quieres planear hoy?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("⏳ La IA está trabajando..."):
            try:
                # Generar contenido con Gemini
                response = model.generate_content(f"Haz una planeación docente sobre: {tema}")
                st.markdown(response.text)
                
                # Guardar en Supabase
                data = {"tema": tema, "contenido_ia": response.text}
                supabase.table("planeaciones").insert(data).execute()
                st.success("✅ ¡Planeación generada y guardada!")
            except Exception as e:
                st.error(f"Hubo un problema: {e}")
