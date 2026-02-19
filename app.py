import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Configuración obligatoria (Debe ser la primera línea de código)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Inicialización de conexiones
def cargar_servicios():
    try:
        # Supabase
        sb = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        # Gemini (Modelo estable para evitar error 404)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        modelo_ai = genai.GenerativeModel('gemini-1.5-flash')
        return sb, modelo_ai
    except Exception as e:
        st.error(f"Error de configuración: {e}")
        return None, None

supabase, model = cargar_servicios()

# 3. Interfaz de Planeación ABCD
st.title("🍎 Profe.Educa IA: Planeador ABCD")

tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej: El ciclo del agua")

if st.button("Generar Planeación"):
    if tema and model:
        with st.spinner("La IA está trabajando..."):
            try:
                prompt = f"Actúa como un tutor experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío inicial, una meta y una ruta de diálogo."
                respuesta = model.generate_content(prompt)
                st.session_state['propuesta'] = respuesta.text
            except Exception as e:
                st.error(f"La IA no pudo responder: {e}")
    else:
        st.warning("Ingresa un tema para continuar.")

# 4. Mostrar y Guardar
if 'propuesta' in st.session_state:
    resultado = st.text_area("Resultado:", value=st.session_state['propuesta'], height=300)
    
    if st.button("Guardar en mi Bitácora"):
        try:
            # Asegúrate de que la columna en Supabase se llame meta_semana
            supabase.table("planeaciones").insert({"meta_semana": resultado}).execute()
            st.success("✅ Guardado con éxito en Supabase.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
