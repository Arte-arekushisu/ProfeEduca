import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Configuración de la interfaz
st.set_page_config(page_title="ProfeEduca", page_icon="🍎", layout="centered")

# --- CREDENCIALES ---
# Tu llave de Google (limpiada de espacios)
GOOGLE_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM".strip()

# Tus datos de Supabase (con la llave larga que acabas de obtener)
S_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc".strip()

# --- CONEXIÓN A LOS SERVICIOS ---
try:
    # transport='rest' es fundamental para evitar el error 404 en Streamlit
    genai.configure(api_key=GOOGLE_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Conexión a la base de datos
    supabase = create_client(S_URL, S_KEY)
except Exception as e:
    st.error(f"Error crítico en la configuración de llaves: {e}")

# --- DISEÑO DE LA APLICACIÓN ---
st.title("🍎 ProfeEduca")
st.markdown("### Generador de Planeaciones Pedagógicas")
st.info("Escribe el tema de tu clase y la IA creará una propuesta educativa para ti.")

tema = st.text_input("¿Qué tema quieres planear hoy?", placeholder="Ej. Fotosíntesis, Revolución Mexicana, Fracciones...")

if st.button("🚀 Generar y Guardar Planeación"):
    if tema:
        with st.spinner("⏳ La IA está redactando tu planeación..."):
            try:
                # Paso 1: Generar con Gemini
                prompt = f"Actúa como un experto pedagogo. Crea una planeación de clase detallada para el tema: {tema}. Incluye objetivos, inicio, desarrollo, cierre y evaluación."
                response = model.generate_content(prompt)
                
                if response.text:
                    # Mostrar resultado en pantalla
                    st.success("¡Planeación generada con éxito!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    
                    # Paso 2: Guardar en Supabase
                    try:
                        registro = {"tema": tema, "contenido_ia": response.text}
                        supabase.table("planeaciones").insert(registro).execute()
                        st.info("💾 Los datos se han guardado automáticamente en tu base de datos.")
                    except Exception as db_err:
                        st.warning(f"⚠️ La planeación se creó, pero hubo un detalle al guardar en la base de datos: {db_err}")
                else:
                    st.error("La IA no devolvió contenido. Por favor, intenta de nuevo.")
                    
            except Exception as e:
                # Si aparece el error 404, este mensaje te dirá si el parche de 'rest' funcionó
                st.error(f"Hubo un error al conectar con Google Gemini: {e}")
    else:
        st.warning("⚠️ Por favor, escribe un tema antes de continuar.")

# Pie de página
st.caption("ProfeEduca - Herramienta de apoyo docente impulsada por Inteligencia Artificial.")
