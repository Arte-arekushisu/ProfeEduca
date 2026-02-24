import streamlit as st
import requests

# Tu llave confirmada
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# AJUSTE BASADO EN TUS LÍMITES:
# Cambiamos v1beta por v1 y gemini-1.5 por gemini-3-flash
api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3-flash:generateContent?key={G_KEY}"

st.title("🍎 ProfeEduca: Conexión Gemini 3")

# Mostramos los límites para que estés al tanto
st.sidebar.write("📊 **Límites de tu nivel gratuito:**")
st.sidebar.write("- 5 peticiones por minuto")
st.sidebar.write("- 20 peticiones por día")

tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar Planeación"):
    if tema:
        payload = {
            "contents": [{
                "parts": [{"text": f"Crea una planeación de clase sobre: {tema}"}]
            }]
        }
        with st.spinner("Llamando a Gemini 3 Flash..."):
            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    texto = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(texto)
                else:
                    st.error(f"Error {response.status_code}")
                    st.write("Respuesta de Google:", response.text)
            except Exception as e:
                st.error(f"Error de red: {e}")
