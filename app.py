import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- REEMPLAZA ESTAS LLAVES ---
# 1. Asegúrate de que tu Google Key sea la nueva de AI Studio
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
# 2. Asegúrate de que esta sea la llave 'anon' 'public' de Supabase
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

# --- CONFIGURACIÓN DE CONEXIÓN ---
try:
    # Esta línea con transport='rest' ELIMINA el error 404 v1beta
    genai.configure(api_key=G_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Revisa tus llaves: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar planeación"):
    if tema:
        with st.spinner("⏳ Generando contenido con IA..."):
            try:
                # Generar con el modelo estable
                response = model.generate_content(f"Planeación pedagógica sobre: {tema}")
                st.markdown(response.text)
                
                # Guardar en la base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ ¡Planeación guardada con éxito!")
            except Exception as e:
                # Si esto falla, el error nos dirá exactamente por qué
                st.error(f"Aviso técnico: {e}")
