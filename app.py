import streamlit as st
import requests

# Tu llave confirmada
G_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

st.title("🍎 ProfeEduca: Conexión Inteligente")

# Intentaremos con el nombre técnico correcto para Gemini 3
# En la API, Gemini 3 Flash suele llamarse 'gemini-2.0-flash' o 'gemini-1.5-flash'
# dependiendo de la región y actualización del proyecto.
modelos_a_probar = ["gemini-1.5-flash", "gemini-2.0-flash"]

tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar Planeación"):
    if tema:
        exito = False
        for modelo in modelos_a_probar:
            # Probamos con la versión v1beta que es donde suelen estar los modelos nuevos
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={G_KEY}"
            
            try:
                payload = {"contents": [{"parts": [{"text": f"Crea una planeación de clase sobre: {tema}"}]}]}
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    texto = data['candidates'][0]['content']['parts'][0]['text']
                    st.success(f"✅ Conectado exitosamente usando el modelo: {modelo}")
                    st.markdown(texto)
                    exito = True
                    break # Salimos del ciclo si funciona
                else:
                    st.write(f"Refinando conexión... (Probando siguiente ruta)")
            except Exception as e:
                continue
        
        if not exito:
            st.error("No se pudo establecer la conexión automática.")
            st.info("💡 Sugerencia: Revisa en Google AI Studio si el modelo 'Gemini 1.5 Flash' aparece como disponible en tu región.")
