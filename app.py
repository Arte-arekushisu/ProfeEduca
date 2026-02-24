import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- REEMPLAZA ESTO CON TUS LLAVES REALES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# --- CONEXIÓN BLINDADA ---
try:
    # 'transport=rest' es el truco maestro para eliminar el error 404 v1beta
    genai.configure(api_key=GEMINI_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error en llaves: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué quieres planear hoy?")

if st.button("Generar planeación"):
    if tema:
        with st.spinner("⏳ Conectando con la IA..."):
            try:
                response = model.generate_content(f"Crea una planeación educativa sobre: {tema}")
                st.markdown(response.text)
                # Guardar
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ ¡Guardado en la base de datos!")
            except Exception as e:
                st.error(f"Aviso: {e}")
