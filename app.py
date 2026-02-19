import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Conexión Estable
try:
    # Conexión Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # FORZAR VERSIÓN ESTABLE V1
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest') # Usamos 'rest' para mayor estabilidad
    
    # Llamamos al modelo sin prefijos de beta
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# 3. Interfaz Modelo ABCD
st.title("🍎 Planeador ABCD (Versión Estable)")
st.write("Genera desafíos y rutas de aprendizaje para CONAFE.")

tema = st.text_input("¿Qué tema quieres planear hoy?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Conectando con la versión estable de Gemini..."):
            try:
                prompt = f"Actúa como tutor CONAFE. Para el tema '{tema}', genera un Desafío, una Meta y una Ruta de aprendizaje usando el Modelo ABCD."
                # Llamada directa
                response = model.generate_content(prompt)
                st.session_state['resultado'] = response.text
            except Exception as e:
                st.error(f"Error en la conexión estable: {e}")
    else:
        st.warning("Escribe un tema primero.")

# 4. Mostrar y Guardar
if 'resultado' in st.session_state:
    texto_final = st.text_area("Resultado:", value=st.session_state['resultado'], height=300)
    
    if st.button("Guardar en Bitácora"):
        try:
            supabase.table("planeaciones").insert({"meta_semana": texto_final}).execute()
            st.success("✅ ¡Guardado con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
