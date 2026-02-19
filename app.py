import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. ESTO DEBE SER LA PRIMERA LÍNEA (Indispensable para que funcione 'st')
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. INICIALIZACIÓN DE SERVICIOS
try:
    # Conexión Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conexión Gemini (Forzamos modelo de producción estable)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Usamos solo 'gemini-1.5-flash' para evitar errores de API v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración inicial: {e}")
    st.stop()

# 3. INTERFAZ DE USUARIO (Modelo ABCD)
st.title("🍎 Planeador ABCD (CONAFE)")
st.write("Crea desafíos y rutas de aprendizaje basadas en el diálogo pedagógico.")

tema = st.text_input("¿Qué tema vamos a planear hoy?", placeholder="Ej: El ciclo del agua")

if st.button("Generar Propuesta"):
    if tema:
        with st.spinner("La IA está analizando el tema..."):
            try:
                # Instrucción específica para la metodología de CONAFE
                prompt = (f"Como tutor experto en el Modelo ABCD de CONAFE, "
                         f"crea para el tema '{tema}': un Desafío inicial, "
                         f"una Meta clara y una breve Ruta de Diálogo.")
                
                # Llamada directa al modelo
                respuesta = model.generate_content(prompt)
                st.session_state['resultado_ia'] = respuesta.text
            except Exception as e:
                # Si falla, mostramos el error detallado para saber qué pasó
                st.error(f"La IA tuvo un inconveniente técnico: {e}")
    else:
        st.warning("Por favor, escribe un tema primero.")

# 4. MOSTRAR RESULTADO Y GUARDADO
if 'resultado_ia' in st.session_state:
    texto_final = st.text_area("Propuesta Pedagógica:", value=st.session_state['resultado_ia'], height=300)
    
    if st.button("Guardar en mi Bitácora"):
        try:
            # Insertar en la tabla de Supabase
            supabase.table("planeaciones").insert({"meta_semana": texto_final}).execute()
            st.success("✅ ¡Guardado con éxito en Supabase!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar en la base de datos: {e}")
