import streamlit as st
import google.generativeai as genai
from supabase import create_client

# Configuración básica
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# LLAVES (Copia y pega con cuidado, sin espacios extra)
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# Conexión al modelo estable
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué quieres planear hoy?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Generando..."):
            try:
                # Generar contenido
                response = model.generate_content(f"Haz una planeación sobre: {tema}")
                st.markdown(response.text)
                
                # Guardar en base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("¡Listo y guardado!")
            except Exception as e:
                st.error(f"Error: {e}")
