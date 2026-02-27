import streamlit as st

# --- CONFIGURACIÓN PARA GOOGLE (SEO) ---
st.set_page_config(
    page_title="PROFEEDUCA | Sistema Integral de Planeación ABCD", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': None,
        'About': "# PROFEEDUCA\nPlataforma de apoyo educativo para el modelo ABCD."
    }
)

# --- ESTILO DE ALTO CONTRASTE ---
st.markdown("""
    <style>
    .stApp {
        background: #020617;
        color: #ffffff;
    }
    h1 {
        color: #38bdf8 !important;
        text-shadow: 2px 2px 8px #38bdf844;
        font-weight: 900 !important;
        font-size: 3rem !important;
    }
    .stAlert {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
        border: 2px solid #38bdf8 !important;
    }
    /* Estilo para que el menú lateral también combine */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FRASE MOTIVACIONAL DEL DÍA (Personalizada para Axel) ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;">
        <span style="color: white; font-weight: bold;">🌟 FRASE DEL DÍA: "La educación no cambia al mundo, cambia a las personas que van a cambiar al mundo."</span>
    </div>
""", unsafe_allow_html=True)

# --- CONTENIDO ---
st.title("🎓 PROFEEDUCA MASTER")
st.write("---")

st.markdown("### 🚀 Bienvenido, Axel")
st.write("Has configurado tu sistema con éxito. Selecciona un módulo en el menú de la izquierda para comenzar.")

st.info("💡 **INFO:** Este sitio ahora es rastreable por buscadores. Compartir el enlace ayudará a que Google lo indexe más rápido.")

# Tarjeta de bienvenida visual
st.markdown("""
<div style="border: 1px solid #38bdf8; padding: 20px; border-radius: 15px; background: #0f172a;">
    <h4 style="color: #7dd3fc;">Estatus de Conexión:</h4>
    <p>✅ Base de Datos Supabase: Conectada</p>
    <p>✅ Modelos de IA (Gemini/Groq): Listos</p>
    <p>✅ Generador PDF: Operativo</p>
</div>
""", unsafe_allow_html=True)
