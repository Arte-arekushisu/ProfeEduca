import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE PÁGINA (Siempre va primero) ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- 2. LLAVES SECRETAS ---
# RECUERDA: Pega aquí tu NUEVA API KEY de Gemini
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 3. CONEXIONES Y MODELO ---
try:
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    genai.configure(api_key=KEY_GEMINI)
    # Definimos el modelo ANTES de usarlo en la función
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- 4. FUNCIÓN DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"Eres un experto maestro. Crea una planeación ABCD profesional para: {tema}"
    try:
        # Intentamos generar el contenido usando el modelo ya definido
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"Error al conectar con la IA: {e}"

# --- 5. INTERFAZ VISUAL ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

tema_maestro = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_maestro:
        with st.spinner("⏳ Redactando tu planeación..."):
            resultado = pedir_ayuda_a_gemini(tema_maestro)
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            try:
                supabase.table("planeaciones").insert({"tema": tema_maestro, "contenido_ia": resultado}).execute()
                st.success("✅ Guardado en la nube")
            except:
                st.info("Planeación lista. (Nota: Revisa tu llave de Supabase para guardar)")
    else:
        st.warning("Escribe un tema primero.")

st.sidebar.success("Conectado a la Nube")
