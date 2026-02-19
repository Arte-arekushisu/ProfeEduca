# Cambia esta parte en tu código:
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Probamos con este nombre de modelo que es el estándar más estable
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error(f"Error de configuración: {e}")
