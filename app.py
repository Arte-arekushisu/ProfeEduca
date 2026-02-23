import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. CONFIGURACIÓN (Siempre al principio) ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- 2. LLAVES SECRETAS ---
# Pega aquí tus datos actuales. Asegúrate de que no haya espacios extras.
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
# RECUERDA: Genera una clave NUEVA en Google AI Studio si la anterior sigue fallando
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 3. INICIALIZACIÓN ---
# Creamos las variables como 'None' para evitar errores de "not defined"
model = None
supabase = None

try:
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    genai.configure(api_key=KEY_GEMINI)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- 4. FUNCIÓN DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    if model is None:
        return "Error: El modelo de IA no está configurado. Revisa tu API Key."
    
    prompt = f"Eres un experto maestro. Crea una planeación ABCD profesional para: {tema}"
    try:
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"Error al generar con IA: {e}"

# --- 5. INTERFAZ VISUAL ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

tema_maestro = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_maestro:
        with st.spinner("⏳ Gemini está trabajando..."):
            resultado = pedir_ayuda_a_gemini(tema_maestro)
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            # Guardado en base de datos
            if supabase:
                try:
                    supabase.table("planeaciones").insert({"tema": tema_maestro, "contenido_ia": resultado}).execute()
                    st.success("✅ Guardado en la nube")
                except:
                    st.info("Planeación lista. (Nota: Detalle al guardar en Supabase)")
    else:
        st.warning("Por favor, escribe un tema primero.")

st.sidebar.success("Sistema Conectado")
