import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Iniciamos la configuración de la página
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión a servicios con manejo de errores limpio
try:
    # Conectamos Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conectamos Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# 3. Interfaz de Planeación Modelo ABCD
st.title("🍎 Planeador ABCD (CONAFE)")
st.write("Crea desafíos y rutas de aprendizaje basadas en el diálogo.")

tema = st.text_input("¿Qué tema vamos a planear hoy?", placeholder="Ej: Las estaciones del año")

if st.button("Generar Propuesta"):
    if tema:
        with st.spinner("La IA está analizando el tema..."):
            try:
                prompt = f"Actúa como tutor CONAFE. Para el tema '{tema}', genera un Desafío, una Meta y una Ruta de aprendizaje usando el Modelo ABCD."
                respuesta = model.generate_content(prompt)
                st.session_state['resultado'] = respuesta.text
            except Exception as e:
                st.error(f"La IA no pudo procesar la solicitud: {e}")
    else:
        st.warning("Por favor, ingresa un tema.")

# 4. Mostrar y Guardar
if 'resultado' in st.session_state:
    texto_final = st.text_area("Propuesta Pedagógica:", value=st.session_state['resultado'], height=300)
    
    if st.button("Guardar en Supabase"):
        try:
            # Insertamos en la tabla 'planeaciones'
            supabase.table("planeaciones").insert({"meta_semana": texto_final}).execute()
            st.success("✅ ¡Guardado con éxito en tu bitácora!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
