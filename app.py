import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- LLAVES (PÉGALAS AQUÍ) ---
# 1. Tu API Key de Google AI Studio
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
# 2. La URL de tu proyecto Supabase
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
# 3. La llave 'anon' 'public' de Supabase (empieza con eyJ...)
S_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# --- CONFIGURACIÓN DE IA ---
try:
    # transport='rest' es la medicina para el error 404 v1beta
    genai.configure(api_key=GOOGLE_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error en configuración: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar planeación"):
    if tema:
        with st.spinner("⏳ Conectando con la IA..."):
            try:
                response = model.generate_content(f"Crea una planeación educativa sobre: {tema}")
                st.markdown(response.text)
                # Guardado en base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ ¡Planeación guardada con éxito!")
            except Exception as e:
                st.error(f"Aviso: {e}")
