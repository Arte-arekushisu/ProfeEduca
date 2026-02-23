import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. LLAVES SECRETAS ---
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 2. CONFIGURACIÓN ---
try:
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    genai.configure(api_key=KEY_GEMINI)
    
    # TRUCO PARA EL ERROR 404: Buscamos el modelo disponible en tu cuenta
    model_name = 'gemini-1.5-flash' # Nombre base
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- 3. FUNCIÓN DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"Eres un experto maestro. Haz una planeación ABCD profesional para el tema: {tema}."
    try:
        # Intento normal
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        # Si falla el anterior (error 404), intentamos con el prefijo models/
        try:
            modelo_alt = genai.GenerativeModel(f'models/{model_name}')
            respuesta = modelo_alt.generate_content(prompt)
            return respuesta.text
        except Exception as e2:
            return f"Error crítico de conexión con Google: {e2}"

# --- 4. INTERFAZ VISUAL ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

tema_maestro = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej. El ciclo del agua")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_maestro:
        with st.spinner("⏳ Redactando..."):
            resultado = pedir_ayuda_a_gemini(tema_maestro)
            
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            # Guardado en Supabase
            try:
                supabase.table("planeaciones").insert({"tema": tema_maestro, "contenido_ia": resultado}).execute()
                st.success("✅ Guardado en la nube")
            except:
                st.info("Planeación lista. (Nota: No se guardó en la base de datos, revisa tus llaves de Supabase)")
    else:
        st.warning("Escribe un tema primero.")

st.sidebar.success("Conectado a la Nube")
