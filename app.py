import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- TUS LLAVES ---
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM" # Asegúrate de que sea la nueva que generaste

# --- CONEXIÓN AL MODELO ---
try:
    genai.configure(api_key=KEY_GEMINI)
    # Usamos el nombre estándar para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
except Exception as e:
    st.error(f"Error de conexión inicial: {e}")

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej. El ciclo del agua")

if st.button("🪄 Generar Planeación"):
    if tema:
        with st.spinner("⏳ Gemini está redactando tu clase..."):
            try:
                # Generamos el contenido sin usar versiones beta
                respuesta = model.generate_content(f"Eres un maestro experto. Crea una planeación ABCD para: {tema}")
                texto = respuesta.text
                
                st.markdown("### Planeación Generada:")
                st.write(texto)
                
                # Guardamos en la base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": texto}).execute()
                st.success("✅ ¡Éxito! Planeación guardada en la nube.")
                
            except Exception as e:
                # Este mensaje nos dirá si Google aún tiene algún bloqueo
                st.error(f"La IA todavía tiene un detalle técnico: {e}")
    else:
        st.warning("Escribe un tema primero.")
