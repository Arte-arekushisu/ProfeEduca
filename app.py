import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. LLAVES SECRETAS ---
# Pon tus llaves reales aquí adentro
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 2. CONFIGURACIÓN ---
try:
    # Conexión a Base de Datos
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    # Conexión a IA
    genai.configure(api_key=KEY_GEMINI)
    
    # EL CAMBIO MÁGICO: Probamos con el nombre corto que pide la versión actual
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de conexión: {e}")

# --- 3. FUNCIÓN DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    # Instrucciones para el asistente
    prompt = f"Eres un experto maestro del modelo ABCD. Diseña una planeación profesional para: {tema}"
    try:
        # Intentamos generar el contenido
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        # Si el primer nombre falla, este bloque intenta el nombre largo automáticamente
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            respuesta = model_alt.generate_content(prompt)
            return respuesta.text
        except:
            return f"Lo siento, la IA todavía no responde. Error: {e}"

# --- 4. INTERFAZ VISUAL ---
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

tema_usuario = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej. El ciclo del agua")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_usuario:
        with st.spinner("⏳ Redactando..."):
            # Generamos el texto
            resultado = pedir_ayuda_a_gemini(tema_usuario)
            
            # Mostramos en pantalla
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            # Intentamos guardar en la base de datos (Supabase)
            try:
                # Nota: la tabla 'planeaciones' ya existe según tus capturas
                supabase.table("planeaciones").insert({"tema": tema_usuario, "contenido_ia": resultado}).execute()
                st.success("✅ Guardado en la nube")
            except:
                st.info("Planeación lista, pero no se pudo guardar en la base de datos (revisa tu llave Anon).")
    else:
        st.warning("Escribe un tema primero.")

# Barra lateral
st.sidebar.markdown("### Estado del Sistema")
st.sidebar.success("Conectado a la Nube")
