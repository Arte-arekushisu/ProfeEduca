import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# --- CONEXIÓN A MOTORES ---
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Configuración incompleta: {e}")

# --- INTERFAZ ---
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?")
    if st.button("Generar Desafío ABCD"):
        with st.spinner("La IA está diseñando la tutoría..."):
            # Instrucción específica para el modelo CONAFE
            prompt = f"""Actúa como un experto en el Modelo ABCD de CONAFE. 
            Para el tema '{tema}', genera:
            1. Un DESAFÍO inicial que despierte interés.
            2. Una breve RUTA DE DIÁLOGO para la tutoría.
            3. Una sugerencia para la DEMOSTRACIÓN PÚBLICA."""
            
            res = model.generate_content(prompt)
            st.session_state['propuesta'] = res.text
            st.success("¡Propuesta generada!")

# --- FORMULARIO DE GUARDADO ---
with st.form("f_planeacion"):
    meta = st.text_area("Resultado de la IA / Meta de la semana", 
                        value=st.session_state.get('propuesta', ''), 
                        height=300)
    
    if st.form_submit_button("Guardar Planeación"):
        try:
            supabase.table("planeaciones").insert({"meta_semana": meta}).execute()
            st.success("✅ Planeación guardada con éxito en la nube.")
        except Exception as e:
            st.error(f"Error al guardar: {e}")
