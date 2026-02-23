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
    # Usamos solo el nombre del modelo, sin el prefijo 'models/'
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- 3. FUNCIÓN DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"Actúa como experto pedagogo. Crea una planeación para: {tema}"
    try:
        # Intento de generación directa
        respuesta = model.generate_content(tema)
        return respuesta.text
    except Exception as e:
        return f"La IA aún no responde: {e}"

# --- 4. INTERFAZ ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")
st.markdown("<h1 style='text-align: center;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)

tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("🪄 Generar Planeación"):
    if tema:
        with st.spinner("⏳ Gemini está escribiendo..."):
            resultado = pedir_ayuda_a_gemini(tema)
            st.markdown("### Planeación Generada:")
            st.write(resultado)
            
            # Guardado
            try:
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": resultado}).execute()
                st.success("✅ Guardado en Supabase")
            except:
                st.info("Nota: La planeación está lista, pero no se guardó en la base de datos.")
    else:
        st.warning("Escribe un tema.")
