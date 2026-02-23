import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Configuración de Página (Siempre al inicio)
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# 2. Llaves (Asegúrate de pegar tu API KEY NUEVA de Google AI Studio)
GEMINI_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# 3. Conexión Forzada a Versión Estable
try:
    # 'transport=rest' ayuda a evitar el error 404 en algunos servidores
    genai.configure(api_key=GEMINI_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error de configuración inicial: {e}")

# 4. Interfaz Visual
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
tema = st.text_input("Tema de la clase:", placeholder="Ej. El ciclo del agua")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con Google..."):
            try:
                # Generamos contenido
                response = model.generate_content(f"Planeación ABCD para: {tema}")
                st.markdown("### Resultado:")
                st.write(response.text)
                
                # Guardamos en Supabase
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ Guardado en la nube")
            except Exception as e:
                # Este error nos dirá si es la clave o la conexión
                st.error(f"Detalle técnico: {e}")
    else:
        st.warning("Escribe un tema primero.")
