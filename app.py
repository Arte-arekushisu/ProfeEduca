import streamlit as st
import requests
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión a Base de Datos
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# 3. Función para llamar a ChatGPT
def generar_planeacion_chatgpt(tema):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Eres un tutor experto en el Modelo ABCD de CONAFE."},
            {"role": "user", "content": f"Diseña un desafío, meta y ruta de diálogo para: {tema}"}
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}. Verifica tu saldo en OpenAI."

# 4. Interfaz
st.title("🍎 Planeador ABCD (OpenAI)")
tema = st.text_input("Tema de la clase:")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con ChatGPT..."):
            resultado = generar_planeacion_chatgpt(tema)
            st.session_state['resultado_ia'] = resultado
            st.markdown(resultado)

if 'resultado_ia' in st.session_state and st.button("Guardar en Bitácora"):
    supabase.table("planeaciones").insert({"meta_semana": st.session_state['resultado_ia']}).execute()
    st.success("✅ Guardado correctamente")
