import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. ESTO DEBE SER LA PRIMERA LÍNEA SIEMPRE
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. CONEXIÓN DIRECTA (Sin funciones complejas para evitar errores)
try:
    # Conectamos a Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conectamos a la IA (Versión estable de producción)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# 3. INTERFAZ SENCILLA Y EFECTIVA
st.title("📋 Planeación Modelo ABCD")

tema = st.text_input("¿Qué tema quieres planear?", placeholder="Ej: Ciclo del agua")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("Generando..."):
            try:
                # Prompt directo para el modelo ABCD de CONAFE
                prompt = f"Crea una planeación breve para el tema '{tema}' usando el modelo ABCD (Aprendizaje Basado en la Colaboración y el Diálogo). Incluye: Desafío, Meta y Ruta de aprendizaje."
                respuesta = model.generate_content(prompt)
                st.session_state['resultado'] = respuesta.text
            except Exception as e:
                st.error(f"Error de la IA: {e}")
    else:
        st.warning("Escribe un tema primero.")

# 4. MOSTRAR Y GUARDAR
if 'resultado' in st.session_state:
    texto_final = st.text_area("Resultado:", value=st.session_state['resultado'], height=300)
    
    if st.button("Guardar en la Base de Datos"):
        try:
            supabase.table("planeaciones").insert({"meta_semana": texto_final}).execute()
            st.success("✅ Guardado correctamente.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
