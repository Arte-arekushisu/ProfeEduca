import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- 2. LLAVES ---
# Asegúrate de que no haya espacios extras dentro de las comillas
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 3. INICIALIZACIÓN ---
try:
    genai.configure(api_key=KEY_GEMINI)
    # NOTA: Usamos el nombre sin prefijos para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
except Exception as e:
    st.error(f"Error de conexión: {e}")

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🪄 Generar Planeación"):
    if tema:
        with st.spinner("⏳ Redactando..."):
            try:
                # Generación de contenido
                respuesta = model.generate_content(f"Crea una planeación ABCD para: {tema}")
                contenido = respuesta.text
                
                # Mostrar resultado
                st.markdown("### Resultado:")
                st.write(contenido)
                
                # Guardado en base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": contenido}).execute()
                st.success("✅ Guardado en la nube")
            except Exception as e:
                # Si vuelve a dar 404, el sistema nos dirá exactamente por qué
                st.error(f"La IA no pudo responder: {e}")
    else:
        st.warning("Escribe un tema primero.")
