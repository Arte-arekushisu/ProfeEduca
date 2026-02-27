import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA MASTER", layout="wide", page_icon="🎓")

# --- ESTILO DE ALTO CONTRASTE (DARK MODE) ---
st.markdown("""
    <style>
    /* Fondo negro profundo para máximo contraste */
    .stApp {
        background: #020617;
        color: #ffffff;
    }
    /* Títulos en azul neón brillante */
    h1 {
        color: #38bdf8 !important;
        text-shadow: 2px 2px 4px #000000;
        font-weight: 900 !important;
    }
    h3 {
        color: #7dd3fc !important;
    }
    /* Recuadro de información con borde resaltado */
    .stAlert {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 15px;
    }
    /* Línea divisora brillante */
    hr {
        border: 1px solid #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---
st.title("🎓 Sistema Integral PROFEEDUCA")
st.write("---")

st.markdown("### 🚀 ¡Bienvenido al Centro de Control, Axel!")
st.write("Tu plataforma está lista. Cada módulo a la izquierda es independiente para evitar errores.")

st.info("💡 **DATO PRO:** Usa el menú de la izquierda para navegar entre las fases de registro, planeación y reportes de IA.")

# Decoración visual para rellenar el espacio con estilo
st.markdown("""
<div style="margin-top: 50px; padding: 30px; border-radius: 20px; background: linear-gradient(145deg, #0f172a, #1e293b); border: 1px solid #38bdf8;">
    <h2 style="color: #38bdf8; margin-top: 0;">🛠️ Estado del Sistema</h2>
    <ul style="color: #f8fafc; list-style-type: '✅ ';">
        <li>Fase 1: Identidad Digital - <b>Activa</b></li>
        <li>Fase 2: Planeación ABCD - <b>Activa</b></li>
        <li>Fase 3: Reportes IA - <b>Activa</b></li>
        <li>Fase 4: Evaluación Trimestral - <b>Activa</b></li>
    </ul>
</div>
""", unsafe_allow_html=True)
