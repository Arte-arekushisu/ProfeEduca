import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. CONFIGURACIÓN INICIAL (Debe ser la primera línea para evitar NameError)
st.set_page_config(page_title="Profe.Educa IA", page_icon="🍎")

# 2. INICIALIZACIÓN DE CONEXIONES CON MANEJO DE ERRORES SEGURO
def inicializar_conexiones():
    try:
        # Conexión a Supabase
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase = create_client(url, key)
        
        # Conexión a Gemini (Usamos nombre de modelo estándar para evitar 404)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        return supabase, model
    except Exception as e:
        # Aquí 'st' ya existe, por lo que este error se mostrará correctamente
        st.error(f"⚠️ Error de configuración: {e}")
        st.stop()

supabase, model = inicializar_conexiones()

# 3. INTERFAZ DE USUARIO (Enfoque en Modelo ABCD de CONAFE)
st.title("📋 Planeación Modelo ABCD")

with st.expander("🤖 Asistente de IA (Tutoría CONAFE)", expanded=True):
    tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej: El ciclo del agua")
    
    if st.button("Generar Desafío ABCD"):
        if tema:
            with st.spinner("La IA está diseñando la tutoría..."):
                try:
                    # Prompt optimizado para la metodología pedagógica
                    prompt = f"Actúa como experto en el Modelo ABCD de CONAFE. Para el tema '{tema}', genera un desafío inicial, una meta y una breve ruta de diálogo pedagógico."
                    res = model.generate_content(prompt)
                    st.session_state['propuesta'] = res.text
                except Exception as e:
                    st.error(f"La IA tuvo un problema: {e}")
        else:
            st.warning("Por favor, ingresa un tema primero.")

# 4. RESULTADO Y GUARDADO EN LA NUBE
resultado = st.text_area("Resultado / Meta:", value=st.session_state.get('propuesta', ''), height=300)

if st.button("Guardar Planeación"):
    if resultado:
        try:
            # Guardamos el texto en tu tabla de Supabase
            data = {"meta_semana": resultado}
            supabase.table("planeaciones").insert(data).execute()
            st.success("✅ ¡Planeación guardada con éxito en Supabase!")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar en la base de datos: {e}")
    else:
        st.error("No hay contenido generado para guardar.")
