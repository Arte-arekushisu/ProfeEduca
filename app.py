import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. CONFIGURACIÓN INICIAL (Obligatorio como primera línea para evitar NameError)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. INICIALIZACIÓN DE CONEXIONES
@st.cache_resource
def init_connections():
    try:
        # Conexión a Supabase
        supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        
        # Conexión a Gemini (Forzamos nombre de modelo estable)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        return supabase, model
    except Exception as e:
        st.error(f"⚠️ Error crítico de configuración: {e}")
        st.stop()

supabase, model = init_connections()

# 3. INTERFAZ DE USUARIO (Modelo ABCD)
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente de IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej: El ciclo del agua")
    
    if st.button("Generar Desafío ABCD"):
        if tema:
            with st.spinner("La IA está diseñando la tutoría..."):
                try:
                    # Prompt optimizado para la metodología de CONAFE
                    prompt = f"Actúa como experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío inicial, una meta y una ruta de diálogo pedagógica."
                    res = model.generate_content(prompt)
                    st.session_state['propuesta'] = res.text
                except Exception as e:
                    st.error(f"La IA tuvo un problema: {e}")
        else:
            st.warning("Por favor, ingresa un tema primero.")

# 4. ÁREA DE RESULTADOS Y PERSISTENCIA
resultado = st.text_area("Resultado / Meta:", value=st.session_state.get('propuesta', ''), height=300)

if st.button("Guardar Planeación"):
    if resultado:
        try:
            # Guardamos el texto generado en tu base de datos Supabase
            data = {"meta_semana": resultado}
            supabase.table("planeaciones").insert(data).execute()
            st.success("✅ ¡Planeación guardada con éxito en la nube!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar en la base de datos: {e}")
    else:
        st.error("No hay contenido para guardar.")
