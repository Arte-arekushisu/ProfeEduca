import streamlit as st
import requests

# 1. PEGA TU LLAVE NUEVA AQUÍ (Asegúrate de que no tenga espacios)
G_KEY = "TU_NUEVA_LLAVE_AQUÍ"

st.title("🍎 ProfeEduca: Intento Definitivo")

tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("🚀 Generar Planeación"):
    if tema:
        with st.spinner("⏳ Conectando con la IA..."):
            # Usamos la ruta estable v1beta y el modelo flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={G_KEY}"
            
            # Estructura JSON simplificada al mínimo
            payload = {
                "contents": [
                    {
                        "parts": [{"text": f"Genera una planeación de clase para: {tema}"}]
                    }
                ]
            }
            
            try:
                # Enviamos la petición
                response = requests.post(url, json=payload)
                
                # Si es 200, todo salió bien
                if response.status_code == 200:
                    data = response.json()
                    # Extraemos el texto con cuidado
                    if 'candidates' in data:
                        texto = data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(texto)
                    else:
                        st.error("Google respondió pero no envió texto.")
                else:
                    # Si sale 400 u otro, mostramos el por qué exacto
                    st.error(f"Error {response.status_code}")
                    st.json(response.json()) # Esto nos dirá qué palabra exacta no le gustó
                    
            except Exception as e:
                st.error(f"Fallo de conexión: {e}")
    else:
        st.warning("Por favor escribe un tema.")
