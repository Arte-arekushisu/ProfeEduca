import streamlit as st
import requests

# REEMPLAZA ESTO CON TU LLAVE NUEVA (la que acabas de crear)
G_KEY = "PEGA_AQUÍ_TU_NUEVA_LLAVE"

st.title("🍎 ProfeEduca: Gemini 3 Activado")

tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("⏳ Generando con Gemini 2.0 Flash..."):
            # Usamos la ruta v1beta y el ID gemini-2.0-flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={G_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Crea una planeación educativa sobre: {tema}"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    texto = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(texto)
                else:
                    st.error(f"Error {response.status_code}")
                    st.json(data)
            except Exception as e:
                st.error(f"Error: {e}")
