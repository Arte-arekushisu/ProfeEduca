import streamlit as st
import google.generativeai as genai
from supabase import create_client

st.set_page_config(page_title="ProfeEduca", page_icon="🍎")

# --- LLAVES CORREGIDAS ---
# Tu llave de Google parece correcta, pero asegúrate de que no tenga espacios.
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"

# IMPORTANTE: Aquí debes pegar la llave que empieza con "eyJ..." 
# La que tenías anteriormente (sb_publishable) no funcionará aquí.
S_KEY = "PEGA_AQUÍ_LA_LLAVE_QUE_EMPIEZA_CON_eyJ" 

try:
    # transport='rest' es vital para evitar el error 404
    genai.configure(api_key=GOOGLE_KEY.strip(), transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Inicializamos Supabase
    supabase = create_client(S_URL, S_KEY.strip())
except Exception as e:
    st.error(f"Error en configuración inicial: {e}")

st.title("🍎 ProfeEduca")
tema = st.text_input("¿Qué tema planeamos hoy?")

if st.button("Generar planeación"):
    if tema:
        with st.spinner("⏳ Conectando con la IA..."):
            try:
                # 1. Generar contenido con Gemini
                response = model.generate_content(f"Crea una planeación educativa detallada sobre: {tema}")
                
                if response.text:
                    st.markdown(response.text)
                    
                    # 2. Intentar guardar en Supabase
                    try:
                        data = {"tema": tema, "contenido_ia": response.text}
                        supabase.table("planeaciones").insert(data).execute()
                        st.success("✅ ¡Planeación generada y guardada en la base de datos!")
                    except Exception as db_error:
                        st.warning(f"La planeación se creó, pero no se pudo guardar en la base de datos: {db_error}")
                else:
                    st.error("La IA no devolvió contenido. Intenta con otro tema.")
                    
            except Exception as e:
                st.error(f"Error al conectar con la IA de Google: {e}")
    else:
        st.warning("Por favor, escribe un tema antes de generar.")
