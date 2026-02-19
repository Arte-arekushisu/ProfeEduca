import streamlit as st
import requests
from supabase import create_client

# 1. Configuración inicial
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión Supabase
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"Error de base de datos: {e}")
    st.stop()

# 3. Función de IA con respaldo (Fallback)
def consultar_ia(prompt_text):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Intentamos con el nombre de modelo estable oficial
    modelos_a_probar = ["gemini-1.5-flash-latest", "gemini-1.5-flash"]
    
    last_error = ""
    for m in modelos_a_probar:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                last_error = f"{res.status_code}: {res.text}"
        except Exception as e:
            last_error = str(e)
            
    raise Exception(f"No se pudo conectar con ningún modelo. Último error: {last_error}")

# 4. Interfaz ABCD
st.title("🍎 Planeador ABCD (CONAFE)")
tema = st.text_input("¿Qué tema quieres planear?", placeholder="Ej: Fotosíntesis")

if st.button("Generar Desafío"):
    if tema:
        with st.spinner("Buscando el modelo de IA más estable..."):
            try:
                p = f"Actúa como tutor CONAFE. Crea un desafío y meta ABCD para: {tema}"
                resultado = consultar_ia(p)
                st.session_state['resultado_ia'] = resultado
            except Exception as e:
                st.error(f"Error crítico: {e}")
    else:
        st.warning("Escribe un tema.")

# 5. Mostrar y Guardar
if 'resultado_ia' in st.session_state:
    texto = st.text_area("Propuesta:", value=st.session_state['resultado_ia'], height=300)
    if st.button("Guardar Planeación"):
        try:
            supabase.table("planeaciones").insert({"meta_semana": texto}).execute()
            st.success("✅ Guardado en Supabase")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
