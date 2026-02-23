import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- 2. LLAVES ---
# Verifica que no tengan espacios en blanco al principio o al final
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 3. INICIALIZACIÓN DEL SISTEMA ---
try:
    # Forzamos el uso de la versión estable de la API para evitar el error 404
    genai.configure(api_key=KEY_GEMINI)
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
except Exception as e:
    st.error(f"Error de conexión: {e}")

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🪄 Generar Planeación"):
    if tema:
        with st.spinner("⏳ Redactando tu planeación..."):
            try:
                # Generamos el contenido
                respuesta = model.generate_content(f"Crea una planeación pedagógica para: {tema}")
                texto_planeacion = respuesta.text
                
                # Mostramos el resultado
                st.markdown("### Resultado:")
                st.write(texto_planeacion)
                
                # Guardamos en Supabase
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": texto_planeacion}).execute()
                st.success("✅ ¡Éxito! Guardado en la nube.")
            except Exception as e:
                # Si hay un error, lo mostramos claramente para corregirlo
                st.error(f"Hubo un problema: {e}")
    else:
        st.warning("Escribe un tema antes de continuar.")
