import streamlit as st
from supabase import create_client
import google.generativeai as genai

# 1. CONFIGURACIÓN (Debe ser lo primero)
st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# 2. LLAVES (Pega la NUEVA aquí)
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
# ¡IMPORTANTE!: Pega la llave que acabas de generar en AI Studio
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# 3. CONEXIÓN SEGURA
model = None
try:
    genai.configure(api_key=KEY_GEMINI)
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
except Exception as e:
    st.error(f"Error de conexión: {e}")

# 4. INTERFAZ
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
tema = st.text_input("¿Qué tema quieres planear?")

if st.button("🪄 Generar Planeación"):
    if not KEY_GEMINI or "PEGA_AQUI" in KEY_GEMINI:
        st.error("❌ No has puesto tu nueva API Key.")
    elif tema:
        with st.spinner("⏳ Redactando..."):
            try:
                # Llamada a la IA
                res = model.generate_content(f"Planeación ABCD para: {tema}")
                st.write(res.text)
                # Guardado
                supabase.table("planeaciones").insert({"tema": tema, "contenido_ia": res.text}).execute()
                st.success("✅ Guardado con éxito")
            except Exception as e:
                st.error(f"La IA no pudo responder: {e}")
