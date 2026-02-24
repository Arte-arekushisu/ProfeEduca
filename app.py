import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- LLAVES ---
# Asegúrate de que no tengan espacios al principio ni al final
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# --- CONFIGURACIÓN ESTABLE ---
try:
    # transport='rest' obliga a usar la ruta correcta y quita el error 404
    genai.configure(api_key=GOOGLE_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Revisa tus llaves: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar planeación"):
    if tema:
        with st.spinner("⏳ La IA está trabajando..."):
            try:
                # Generar contenido
                response = model.generate_content(f"Haz una planeación docente sobre: {tema}")
                st.markdown(response.text)
                
                # Guardar en Supabase
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ ¡Guardado con éxito!")
            except Exception as e:
                st.error(f"Aviso: {e}")
