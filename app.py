import streamlit as st
import random

# 1. Configuración y Estilos (Mantener igual que V0.3)
st.set_page_config(page_title="ProfeEduca V0.4", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .apple-stage { position: relative; font-size: 7rem; text-align: center; margin: 15px 0; }
    @keyframes worm-peek {
        0%, 100% { transform: translate(40px, 0px) scale(0); opacity: 0; }
        50% { transform: translate(0px, -45px) rotate(15deg) scale(1.2); opacity: 1; }
    }
    .worm-move { position: absolute; font-size: 2.5rem; animation: worm-peek 5s infinite; left: 47%; top: 15%; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de Variables de Estado
if 'seccion' not in st.session_state:
    st.session_state.seccion = "inicio"

# 3. CREACIÓN DE COLUMNAS (Primero definimos, luego usamos)
col_menu, col_main = st.columns([1, 2])

# --- LADO IZQUIERDO: MENÚ ---
with col_menu:
    st.title("🚀 Menú")
    if st.button("🏠 Inicio / Comunidad", use_container_width=True):
        st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True):
        st.session_state.seccion = "plan"
    
    st.markdown("<br><br>### 📏 ProfeEduca ✏️", unsafe_allow_html=True)

# --- LADO DERECHO: CONTENIDO DINÁMICO ---
with col_main:
    if st.session_state.seccion == "inicio":
        st.markdown("### 🍎 Bienvenido a la Comunidad")
        st.markdown('<div class="apple-stage"><span class="worm-move">🐛</span>🍎</div>', unsafe_allow_html=True)
        st.info("👋 ¡Hola! Saluda a tus colegas en el chat de abajo.")

    elif st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        
        # Uso de pestañas para organizar el trabajo
        tab1, tab2, tab3 = st.tabs(["🎯 Datos", "🧠 El Desafío", "🤝 Comunidad"])
        
        with tab1:
            st.selectbox("Campo Formativo", ["Lenguajes", "Saberes", "Ética", "Humano"])
            st.text_input("Nombre de la Unidad")
            st.text_area("PDA (Proceso de Desarrollo)", height=100)

        with tab2:
            st.subheader("El Motor del Aprendizaje")
            # CORRECCIÓN DE ERROR DE COMILLAS:
            desafio = st.text_area(
                label="Plantea el Desafío:",
                placeholder="Ej. ¿Cómo explicar la lluvia sin lagos cerca?",
                help="Pregunta para investigar."
            )

        with tab3:
            st.subheader("Saberes Locales")
            st.text_area("Vínculo con la comunidad:")
            if st.button("🚀 GENERAR PLANEACIÓN", use_container_width=True):
                st.balloons()
                st.success("¡Datos listos para procesar con IA!")
