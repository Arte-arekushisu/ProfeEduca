import streamlit as st
import requests
from supabase import create_client

# 1. Configuración básica
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

st.title("🍎 Profe.Educa: Planeador ABCD")

# 2. Inicialización de servicios (Con manejo de errores para evitar pantalla blanca)
def inicializar_servicios():
    try:
        if "SUPABASE_URL" not in st.secrets:
            st.error("Faltan secretos en la configuración.")
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error de inicio: {e}")
        return None

supabase = inicializar_servicios()

if supabase:
    st.success("✅ Conexión con la base de datos establecida.")

# 3. Lógica de la IA (URL v1 para evitar Error 404)
def generar_planeacion(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Usamos la ruta estable v1 que Google prefiere para Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"Actúa como experto CONAFE. Crea una planeación ABCD para: {tema}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error de Google ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {e}"

# 4. Interfaz
tema_input = st.text_input("Escribe el tema de tu tutoría:", placeholder="Ej. El ciclo del agua")

if st.button("Generar Desafío y Meta"):
    if tema_input:
        with st.spinner("Generando contenido pedagógico..."):
            resultado = generar_planeacion(tema_input)
            st.markdown("### Resultado:")
            st.write(resultado)
    else:
        st.warning("Por favor, introduce un tema.")
