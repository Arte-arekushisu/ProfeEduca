import streamlit as st
import google.generativeai as genai
from supabase import create_client

# Configuración de página
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# Credenciales (Verifica que tu API KEY sea la NUEVA)
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"

try:
    # transport='rest' es la clave para eliminar el error 404 v1beta
    genai.configure(api_key=GEMINI_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("Tema de la clase:")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("⏳ Conectando con la IA..."):
            try:
                # Usamos el modelo estable
                response = model.generate_content(f"Planeación para: {tema}")
                st.write(response.text)
                
                # Guardado
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": response.text}).execute()
                st.success("✅ Guardado correctamente")
            except Exception as e:
                st.error(f"Error técnico: {e}")
