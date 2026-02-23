import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. LLAVES SECRETAS ---
# Pon tus datos reales entre las comillas
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 2. CONFIGURACIÓN ---
try:
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    genai.configure(api_key=KEY_GEMINI)
    # Nombre de modelo actualizado para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error de conexión: {e}")

# --- 3. FUNCIONES ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"Eres un experto maestro. Crea una planeación ABCD profesional para: {tema}"
    try:
        # Intentamos generar el contenido
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"La IA dice: {e}"

# --- 4. INTERFAZ ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")
st.markdown("<h1 style='text-align: center;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

tema_usuario = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_usuario:
        with st.spinner("⏳ Redactando..."):
            # Generamos
            resultado = pedir_ayuda_a_gemini(tema_usuario)
            
            # Mostramos
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            # Guardamos en Supabase
            try:
                supabase.table("planeaciones").insert({"tema": tema_usuario, "contenido_ia": resultado}).execute()
                st.success("✅ Guardado en la nube")
            except:
                st.warning("Se creó la planeación, pero hubo un detalle al guardar en la base de datos.")
    else:
        st.warning("Escribe un tema primero.")

# Barra lateral
st.sidebar.success("Conectado a ProfeEduca Cloud")
