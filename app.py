import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. ESTO DEBE SER SIEMPRE LA PRIMERA LÍNEA (Evita NameError)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. CONFIGURACIÓN DE CONEXIONES CON MANEJO DE ERRORES
def init_app():
    try:
        # Conexión Supabase
        supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        
        # Conexión Gemini (Forzamos modelo estable para evitar error 404)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        return supabase, model
    except Exception as e:
        st.error(f"⚠️ Error de configuración: {e}")
        st.stop()

supabase, model = init_app()

# 3. INTERFAZ: MODELO ABCD
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente de IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?")
    
    if st.button("Generar Desafío ABCD"):
        if tema:
            with st.spinner("La IA está diseñando la tutoría..."):
                try:
                    # Prompt especializado en la metodología pedagógica
                    prompt = f"Actúa como experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío inicial, una meta y una ruta de diálogo."
                    res = model.generate_content(prompt)
                    st.session_state['propuesta'] = res.text
                except Exception as e:
                    st.error(f"La IA tuvo un problema técnico: {e}")
        else:
            st.warning("Escribe un tema para comenzar.")

# 4. ÁREA DE RESULTADO Y GUARDADO
resultado = st.text_area("Resultado / Meta:", value=st.session_state.get('propuesta', ''), height=300)

if st.button("Guardar Planeación"):
    if resultado:
        try:
            supabase.table("planeaciones").insert({"meta_semana": resultado}).execute()
            st.success("✅ ¡Planeación guardada con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar en base de datos: {e}")
    else:
        st.error("No hay contenido para guardar.")
