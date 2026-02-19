import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. CONFIGURACIÓN INICIAL (Debe ir primero para evitar el NameError)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. CONEXIÓN SEGURA
try:
    # Conectamos a la base de datos
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conectamos a la IA (Ajuste para evitar el error 404)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Usamos gemini-1.5-flash por ser la más compatible
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    # Ahora 'st' ya está definido por set_page_config
    st.error(f"⚠️ Error en la conexión inicial: {e}")
    st.stop()

# 3. INTERFAZ: PLANEACIÓN MODELO ABCD
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente de IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej: El ciclo del agua")
    
    if st.button("Generar Desafío ABCD"):
        if tema:
            with st.spinner("La IA está diseñando la tutoría..."):
                try:
                    prompt = f"Actúa como un experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío inicial, una meta y una ruta de diálogo."
                    res = model.generate_content(prompt)
                    st.session_state['propuesta'] = res.text
                except Exception as e:
                    st.error(f"La IA no pudo responder: {e}")
        else:
            st.warning("Por favor, escribe un tema primero.")

# 4. RESULTADO Y GUARDADO
resultado = st.text_area("Resultado de la IA:", value=st.session_state.get('propuesta', ''), height=300)

if st.button("Guardar Planeación"):
    try:
        supabase.table("planeaciones").insert({"meta_semana": resultado}).execute()
        st.success("✅ ¡Planeación guardada con éxito!")
        st.balloons()
    except Exception as e:
        st.error(f"Error al guardar: {e}")
