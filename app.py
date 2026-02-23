import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. LLAVES SECRETAS (Pega las tuyas aquí) ---
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 2. CONFIGURACIÓN DE CONEXIONES ---
# Este bloque conecta tu app con Supabase y Gemini
try:
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    genai.configure(api_key=KEY_GEMINI)
    # Usamos el nombre del modelo más estable para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Revisa tus llaves, parece que hay un error de conexión.")

# --- 3. EL CEREBRO DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"""
    Eres un experto pedagogo. Diseña una planeación ABCD profesional 
    para el tema: {tema}. 
    Estructura la respuesta con: Inicio, Desarrollo y Cierre.
    No uses símbolos extraños como muchos asteriscos.
    """
    try:
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"Error al generar con IA: {e}"

# --- 4. DISEÑO DE LA PÁGINA (INTERFAZ) ---
st.set_page_config(page_title="ProfeEduca IA", page_icon="🍎")

# Título visual
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.write("---")

# Entrada del maestro
tema_usuario = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej. El sistema solar")

if st.button("🪄 Generar Planeación Mágicamente"):
    if tema_usuario:
        with st.spinner("⏳ Gemini está redactando..."):
            # 1. Llamamos a la IA
            resultado = pedir_ayuda_a_gemini(tema_usuario)
            
            # 2. Mostramos el resultado
            st.markdown("### Resultado de tu Planeación:")
            st.write(resultado)
            
            # 3. Guardamos en la base de datos de Supabase
            try:
                datos = {"tema": tema_usuario, "contenido_ia": resultado}
                supabase.table("planeaciones").insert(datos).execute()
                st.success("✅ Guardado en tu cuenta de Supabase")
            except Exception as e:
                st.warning("Se generó la planeación, pero no se pudo guardar en la base de datos.")
    else:
        st.warning("Por favor, escribe un tema.")

# Barra lateral informativa
st.sidebar.title("Configuración")
st.sidebar.success("Conectado a ProfeEduca Cloud")
st.sidebar.info("Plan: Profesional Mensual")
