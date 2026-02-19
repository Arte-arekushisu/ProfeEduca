import streamlit as st
from supabase import create_client
import google.generativeai as genai

# CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# CONEXIÓN A MOTORES (Con manejo de errores para que la app no muera)
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de conexión: {e}")

# INTERFAZ DE PLANEACIÓN
st.title("📋 Planeación Modelo ABCD")

tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("Generar Desafío ABCD"):
    with st.spinner("La IA está trabajando..."):
        try:
            prompt = f"Actúa como un tutor de CONAFE. Crea un desafío y una meta para el tema: {tema} bajo el modelo ABCD."
            res = model.generate_content(prompt)
            st.session_state['propuesta'] = res.text
            st.success("¡Propuesta lista!")
        except Exception as e:
            st.error(f"Error al generar: {e}")

# Cuadro donde aparece el resultado
meta_final = st.text_area("Resultado:", value=st.session_state.get('propuesta', ''), height=200)

if st.button("Guardar en la Nube"):
    supabase.table("planeaciones").insert({"meta_semana": meta_final}).execute()
    st.balloons()
