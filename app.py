import streamlit as st
from supabase import create_client
import requests

# 1. Configuración de página
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Función para leer secretos sin que la app explote
def obtener_secreto(nombre):
    if nombre in st.secrets:
        return st.secrets[nombre]
    else:
        st.error(f"❌ No encuentro la llave: **{nombre}** en los Secrets de Streamlit.")
        st.stop()

# 3. Inicialización
url = obtener_secreto("SUPABASE_URL")
key = obtener_secreto("SUPABASE_KEY")
gemini_key = obtener_secreto("GEMINI_API_KEY")

supabase = create_client(url, key)

st.title("🍎 Planeador ABCD (CONAFE)")
st.success("¡Conexión establecida correctamente!")

# El resto de tu lógica de IA aquí...
