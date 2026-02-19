import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. CONEXIÓN SEGURA A MOTORES
try:
    # Conexión Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conexión Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Usamos el nombre base del modelo para evitar el error 404 de la versión v1beta
    model = genai.GenerativeModel('gemini-1.5-flash') 
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
                # Prompt optimizado para el modelo educativo de CONAFE
                prompt = f"""Actúa como un experto en el Modelo ABCD de CONAFE. 
                Para el tema '{tema}', genera un desafío inicial, una meta y una breve ruta de diálogo."""
                
                res = model.generate_content(prompt)
                st.session_state['propuesta'] = res.text
            except Exception as e:
                # Si falla el 1.5-flash, intentamos con gemini-pro automáticamente
                try:
                    alt_model = genai.GenerativeModel('gemini-pro')
                    res = alt_model.generate_content(prompt)
                    st.session_state['propuesta'] = res.text
                except:
                    st.error(f"Error de la IA: {e}")

# 4. RESULTADO Y GUARDADO
resultado = st.text_area("Resultado de la IA:", value=st.session_state.get('propuesta', ''), height=300)

if st.button("Guardar Planeación"):
    try:
        supabase.table("planeaciones").insert({"meta_semana": resultado}).execute()
        st.success("✅ ¡Guardado con éxito en la nube!")
    except Exception as e:
        st.error(f"Error al guardar: {e}")
