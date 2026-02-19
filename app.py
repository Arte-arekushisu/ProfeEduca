import streamlit as st
import requests

st.title("Prueba de Conexión Real")

api_key = st.secrets["GEMINI_API_KEY"]

# Esta URL no genera contenido, solo LISTA qué modelos puedes usar
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

if st.button("Verificar mi API Key"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.success("¡Tu llave funciona!")
            st.write("Modelos que Google te permite usar:")
            modelos = response.json()
            for m in modelos['models']:
                st.code(m['name'])
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Fallo total: {e}")
