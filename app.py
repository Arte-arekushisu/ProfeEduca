import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA MASTER", layout="wide", page_icon="🎓")

# --- ESTILO DARK (FONDO OSCURO) ---
st.markdown("""
    <style>
    /* Fondo principal oscuro */
    .stApp {
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    /* Estilo para las tarjetas de información */
    .stAlert {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
    }
    /* Títulos en azul brillante */
    h1, h2, h3 {
        color: #38bdf8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO DE BIENVENIDA ---
st.title("🎓 Sistema Integral PROFEEDUCA")
st.write("---")
st.write("### ¡Hola Axel! Bienvenido a tu plataforma educativa.")
st.write("Selecciona una fase en el menú de la izquierda para comenzar a trabajar en cada módulo de forma independiente.")

st.info("👈 **TIP:** Si no ves el menú lateral, dale clic a la flechita blanca en la esquina superior izquierda.")

# Un pequeño mensaje motivador para que se vea pro
st.markdown("""
<div style="padding: 20px; border-radius: 10px; background-color: #0f172a; border-left: 5px solid #38bdf8;">
    <p style="margin: 0; color: #94a3b8;"><i>"Transformando la educación comunitaria con tecnología y corazón."</i></p>
</div>
""", unsafe_allow_html=True)
