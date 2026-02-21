import streamlit as st
import random

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V0.4", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS (BOTONES TRANSPARENTES Y SUAVES) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* BOTONES TIPO CRISTAL (Glassmorphism) */
    .stButton>button {
        background: rgba(255, 255, 255, 0.03); /* Casi invisible */
        color: rgba(248, 250, 252, 0.7); /* Blanco opaco muy suave */
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        text-align: left;
        padding: 12px;
    }

    /* EFECTO HOVER: Solo brilla al acercar el mouse */
    .stButton>button:hover {
        background: rgba(56, 189, 248, 0.1);
        border-color: #38bdf8;
        color: #38bdf8;
        transform: translateX(5px);
    }

    /* Animación Gusanito (Más lenta para no distraer) */
    @keyframes worm-peek {
        0%, 100% { transform: translate(40px, 0px) scale(0); opacity: 0; }
        50% { transform: translate(0px, -45px) rotate(15deg) scale(1.1); opacity: 1; }
    }
    .apple-stage { position: relative; font-size: 7rem; text-align: center; margin: 15px 0; }
    .worm-move { position: absolute; font-size: 2.5rem; animation: worm-peek 6s infinite; left: 47%; top: 15%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN ---
if 'seccion' not in st.session_state:
    st.session_state.seccion = "inicio"
if 'messages' not in st.session_state:
    st.session_state.messages = [{"user": "Profe_Michi", "text": "¡Hola colegas! ¿Listos para el desafío?"}]

# --- 4. ESTRUCTURA DE COLUMNAS (CORRIGE NameError) ---
col_menu, col_main = st.columns([1, 2])

# LADO IZQUIERDO: MENÚ
with col_menu:
    st.markdown("### 🚀 Panel de Control")
    if st.button("🏠 Inicio / Comunidad", use_container_width=True):
        st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True):
        st.session_state.seccion = "plan"
    
    st.markdown("<br><br>### 📏 ProfeEduca ✏️", unsafe_allow_html=True)

# LADO DERECHO: CONTENIDO
with col_main:
    if st.session_state.seccion == "inicio":
        st.markdown("### 🍎 El Café del Maestro")
        st.markdown('<div class="apple-stage"><span class="worm-move">🐛</span>🍎</div>', unsafe_allow_html=True)
        
        # Chat de Amistad
        st.subheader("💬 Chat Global")
        for m in st.session_state.messages[-3:]: # Solo últimos 3 para no saturar
            st.markdown(f"**@{m['user']}**: {m['text']}")
        
        with st.form("chat", clear_on_submit=True):
            msg = st.text_input("Saluda:")
            if st.form_submit_button("Enviar"):
                if msg:
                    st.session_state.messages.append({"user": "Tú", "text": msg})
                    st.rerun()

    elif st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        t1, t2 = st.tabs(["🎯 Identificación", "🧠 Desafío"])
        
        with t1:
            st.selectbox("Fase", ["Fase 3", "Fase 4", "Fase 5"])
            st.text_input("Tema de la Unidad")
        
        with t2:
            st.text_area("Plantea el Desafío:", 
                         placeholder="Escribe aquí tu pregunta detonadora...",
                         help="Evita responder con sí o no.")
            
            if st.button("🚀 GENERAR CON IA"):
                st.balloons()
                st.success("¡Analizando datos para tu planeación!")
