import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. ESTO DEBE SER LA PRIMERA LÍNEA DE CÓDIGO EJECUTABLE
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. CONFIGURACIÓN DE CONEXIONES
try:
    # Conexión a Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conexión a Gemini (Ajuste para evitar error 404)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Usamos 'gemini-1.5-flash' sin prefijos de versión para mayor estabilidad
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    # Ahora 'st' ya está definido, por lo que este error no fallará
    st.error(f"⚠️ Error de configuración: {e}")
    st.stop()

# 3. INTERFAZ: PLANEACIÓN MODELO ABCD
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente de IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?")
    if st.button("Generar Desafío ABCD"):
        with st.spinner("La IA está diseñando la tutoría..."):
            try:
                # Prompt diseñado para la metodología de CONAFE
                prompt = f"""Actúa como un experto en el Modelo ABCD de CONAFE. 
                Para el tema '{tema}', genera un desafío inicial, una meta y una ruta de diálogo."""
                
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
