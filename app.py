import streamlit as st
import google.generativeai as genai
from supabase import create_client
import os

# Configuración de página adaptable
st.set_page_config(page_title="ProfeEduca", page_icon="🍎", layout="wide")

# --- CREDENCIALES (Variables fijas para evitar errores de ruta) ---
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

# --- CONEXIÓN MULTI-RUTA (La solución al 404) ---
@st.cache_resource
def conectar_servicios():
    # Forzamos el transporte 'rest' para que funcione en cualquier servidor de Streamlit
    genai.configure(api_key=GOOGLE_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    db = create_client(S_URL, S_KEY)
    return model, db

try:
    ia_model, supabase = conectar_servicios()
except Exception as e:
    st.error(f"Error de conexión: {e}")

# --- INTERFAZ ---
st.title("🍎 ProfeEduca: Generador Universal")

tema = st.text_input("Escribe el tema para tu planeación:")

if st.button("Generar Contenido"):
    if tema:
        with st.spinner("Conectando con la IA..."):
            try:
                # El modelo 1.5-flash es el más compatible con las rutas actuales
                res = ia_model.generate_content(f"Planeación educativa sobre: {tema}")
                st.markdown(res.text)
                
                # Guardado en base de datos
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": res.text}).execute()
                st.success("Guardado en Supabase")
            except Exception as e:
                st.error(f"Error en la ruta de acceso: {e}")
