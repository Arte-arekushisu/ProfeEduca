import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. CONEXIÓN A LOS MOTORES
# Usamos un bloque try/except para evitar que la app se bloquee si falta algo
try:
    # Conexión Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conexión Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Cambiamos a 'gemini-pro' para mayor estabilidad y evitar el error 404
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error(f"⚠️ Error de configuración: {e}")
    st.stop()

# 3. INTERFAZ: PLANEACIÓN MODELO ABCD
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente de IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?")
    if st.button("Generar Desafío ABCD"):
        with st.spinner("La IA está diseñando la tutoría..."):
            try:
                prompt = f"Actúa como un experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío inicial, una meta y una ruta de diálogo."
                res = model.generate_content(prompt)
                st.session_state['propuesta'] = res.text
            except Exception as e:
                st.error(f"Error de la IA: {e}")

# 4. RESULTADO Y GUARDADO
resultado = st.text_area("Resultado de la IA:", value=st.session_state.get('propuesta', ''), height=300)

if st.button("Guardar Planeación"):
    try:
        supabase.table("planeaciones").insert({"meta_semana": resultado}).execute()
        st.success("✅ ¡Guardado con éxito en la nube!")
    except Exception as e:
        st.error(f"Error al guardar: {e}")
