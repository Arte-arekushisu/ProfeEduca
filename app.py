import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- LLAVES (Cópialas de tus paneles sin espacios) ---
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" # La que empieza con eyJ...

try:
    # transport='rest' soluciona el error 404 v1beta
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
                # Guardar en base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ ¡Guardado con éxito!")
            except Exception as e:
                st.error(f"Aviso técnico: {e}")
