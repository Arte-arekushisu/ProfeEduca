import streamlit as st
from supabase import create_client
import google.generativeai as genai
from fpdf import FPDF
import unicodedata# Conexión a tu base de datos
URL_DE_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
LLAVE_ANON_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 

# Conexión a tu Inteligencia Artificial
LLAVE_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# Aquí activamos la conexión
supabase = create_client(URL_DE_SUPABASE, LLAVE_ANON_SUPABASE)
genai.configure(api_key=LLAVE_GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash')def pedir_ayuda_a_gemini(tema):
    prompt = f"Eres un experto maestro. Haz una planeación corta para el tema: {tema}"
    respuesta = model.generate_content(prompt)
    return respuesta.textst.title("🍎 ProfeEduca: Tu Asistente con IA")

tema_del_maestro = st.text_input("¿Qué clase quieres preparar hoy?")

if st.button("🪄 Crear Planeación con IA"):
    # 1. Le pedimos a la IA que escriba
    resultado = pedir_ayuda_a_gemini(tema_del_maestro)
    
    # 2. Lo mostramos en pantalla
    st.write(resultado)
    
    # 3. Lo guardamos en tu base de datos de Supabase automáticamente
    supabase.table("planeaciones").insert({"tema": tema_del_maestro, "contenido_ia": resultado}).execute()
    st.success("✅ Guardado en la nube")
