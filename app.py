import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. LLAVES SECRETAS ---
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 2. CONFIGURACIÓN ---
try:
    # Conexión a la base de datos
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    # Conexión a la Inteligencia Artificial
    genai.configure(api_key=KEY_GEMINI)
    # NOMBRE CORREGIDO: Probamos con el nombre simple
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- 3. FUNCIÓN DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"Eres un experto maestro. Haz una planeación ABCD profesional para el tema: {tema}. Usa Inicio, Desarrollo y Cierre."
    try:
        # Aquí es donde ocurre la magia
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        # Si falla el nombre anterior, intentamos con el nombre alternativo automáticamente
        try:
            modelo_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            respuesta = modelo_alt.generate_content(prompt)
            return respuesta.text
        except:
            return f"Error al conectar con la IA: {e}"

# --- 4. INTERFAZ VISUAL ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tu asistente inteligente para maestros</p>", unsafe_allow_html=True)
st.write("---")

tema_maestro = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej. El ciclo del agua")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_maestro:
        with st.spinner("⏳ Redactando tu planeación..."):
            # Llamamos a la inteligencia
            resultado = pedir_ayuda_a_gemini(tema_maestro)
            
            # Mostramos el resultado
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            # Guardamos en Supabase
            try:
                supabase.table("planeaciones").insert({"tema": tema_maestro, "contenido_ia": resultado}).execute()
                st.success("✅ Guardado en tu cuenta")
            except:
                st.info("Planeación generada. (Nota: Hubo un detalle al guardar en la base de datos, revisa tus llaves de Supabase)")
    else:
        st.warning("Por favor, escribe un tema primero.")

# Barra lateral
st.sidebar.markdown("### Estado del Sistema")
st.sidebar.success("Conectado a la Nube")
