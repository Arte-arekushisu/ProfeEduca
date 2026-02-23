import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. LLAVES SECRETAS (Pega las tuyas aquí) ---
# Encuentra estos datos en tu panel de Supabase y Google AI Studio
URL_SUPABASE = "https://pmqmqeukhufaqecbuodg.supabase.co"
KEY_SUPABASE = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4" 
KEY_GEMINI = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- 2. CONFIGURACIÓN DE CONEXIONES ---
# Aquí conectamos tu app con el mundo exterior
try:
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    genai.configure(api_key=KEY_GEMINI)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error en las llaves: Revisa que estén bien copiadas.")

# --- 3. EL CEREBRO DE LA IA ---
def pedir_ayuda_a_gemini(tema):
    # Instrucción especial para que la IA sepa qué hacer
    prompt = f"""
    Actúa como un experto maestro del modelo ABCD. 
    Crea una planeación didáctica profesional para el tema: {tema}.
    Incluye Inicio, Desarrollo y Cierre. 
    Usa un lenguaje claro y evita usar muchos asteriscos o símbolos raros.
    """
    respuesta = model.generate_content(prompt)
    return respuesta.text

# --- 4. DISEÑO DE LA PÁGINA (INTERFAZ) ---
st.set_page_config(page_title="ProfeEduca IA", page_icon="🍎")

# Estilo visual básico
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍎 ProfeEduca</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tu asistente inteligente para maestros</p>", unsafe_allow_html=True)

# Entrada de datos
tema_del_maestro = st.text_input("¿Qué tema quieres preparar hoy?", placeholder="Ej. El ciclo del agua, Las fracciones...")

if st.button("🪄 Crear Planeación Mágicamente"):
    if tema_del_maestro:
        with st.spinner("⏳ Gemini está redactando tu clase..."):
            try:
                # 1. La IA genera el contenido
                resultado = pedir_ayuda_a_gemini(tema_del_maestro)
                
                # 2. Mostramos el resultado en pantalla
                st.markdown("---")
                st.subheader("Tu Planeación Lista:")
                st.write(resultado)
                
                # 3. Guardamos en tu base de datos de Supabase
                datos = {"tema": tema_del_maestro, "contenido_ia": resultado}
                supabase.table("planeaciones").insert(datos).execute()
                
                st.success("✅ ¡Éxito! Tu planeación se generó y se guardó en la nube.")
            except Exception as e:
                st.error(f"Hubo un problema: {e}")
    else:
        st.warning("Escribe un tema primero para poder ayudarte.")

# Pie de página
st.sidebar.markdown("### Suscripción Activa")
st.sidebar.info("Plan Mensual Profesional")
