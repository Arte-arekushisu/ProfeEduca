import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- LLAVES SECRETAS ---
# Pon tus llaves reales entre las comillas
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- CONEXIONES ---
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
genai.configure(api_key=KEY_GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- FUNCIONES ---
def pedir_ayuda_a_gemini(tema):
    prompt = f"Eres un experto maestro. Haz una planeación corta para el tema: {tema}"
    respuesta = model.generate_content(prompt)
    return respuesta.text

# --- INTERFAZ ---
st.title("🍎 ProfeEduca: Tu Asistente con IA")

tema = st.text_input("¿Qué clase quieres preparar hoy?")

if st.button("🪄 Crear Planeación con IA"):
    with st.spinner("Gemini está trabajando..."):
        resultado = pedir_ayuda_a_gemini(tema)
        st.write(resultado)
        
        # Guardado automático
        supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": resultado}).execute()
        st.success("✅ Guardado en la nube")
