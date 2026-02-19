import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. Inicialización de servicios
try:
    # Conexión Supabase
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    
    # Conexión Gemini (Usando el modelo más estable)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al conectar servicios: {e}")
    st.stop()

# 3. Interfaz de Usuario
st.title("🍎 Profe.Educa IA: Planeador ABCD")
st.write("Genera desafíos pedagógicos basados en el modelo de CONAFE.")

tema = st.text_input("¿Qué tema o unidad de aprendizaje quieres preparar?")

if st.button("Generar Planeación"):
    if tema:
        with st.spinner("La IA está creando tu desafío..."):
            try:
                prompt = (
                    f"Actúa como un tutor experto en el Modelo ABCD de CONAFE. "
                    f"Para el tema '{tema}', genera: 1. Un Desafío interesante, "
                    f"2. Una Meta de aprendizaje clara y 3. Una breve Ruta de Diálogo."
                )
                response = model.generate_content(prompt)
                st.session_state['resultado_ia'] = response.text
                st.success("¡Planeación generada!")
            except Exception as e:
                st.error(f"Error con la IA: {e}")
    else:
        st.warning("Por favor, escribe un tema primero.")

# 4. Mostrar resultado y opción de guardado
if 'resultado_ia' in st.session_state:
    texto_final = st.text_area("Resultado:", value=st.session_state['resultado_ia'], height=300)
    
    if st.button("Guardar en mi Bitácora"):
        try:
            # Insertar en la tabla 'planeaciones'
            supabase.table("planeaciones").insert({"meta_semana": texto_final}).execute()
            st.success("✅ Guardado en la base de datos de Supabase.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
