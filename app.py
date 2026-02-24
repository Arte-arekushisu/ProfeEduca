import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- LLAVES ---
# Verifica que estas llaves no tengan espacios al final
GOOGLE_API_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# --- CONFIGURACIÓN SEGURA ---
try:
    # Esta línea es el secreto para quitar el error 404 v1beta
    genai.configure(api_key=GOOGLE_API_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error en configuración de llaves: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué quieres planear hoy?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("⏳ Creando tu planeación..."):
            try:
                # Generar contenido
                response = model.generate_content(f"Crea una planeación docente para: {tema}")
                st.markdown(response.text)
                
                # Guardar en Supabase
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ Guardado en la base de datos")
            except Exception as e:
                st.error(f"Error al generar: {e}")
