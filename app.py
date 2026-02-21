import streamlit as st
import random

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V0.4", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS (ANIMACIONES Y DISEÑO) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Animación del Gusanito Interactiva */
    @keyframes worm-peek {
        0%, 100% { transform: translate(40px, 0px) scale(0); opacity: 0; }
        50% { transform: translate(0px, -45px) rotate(15deg) scale(1.2); opacity: 1; }
    }
    .apple-stage { position: relative; font-size: 7rem; text-align: center; margin: 15px 0; }
    .worm-move { position: absolute; font-size: 2.5rem; animation: worm-peek 5s infinite; left: 47%; top: 15%; }

    /* Estilo del Chat de Amistad */
    .chat-wall {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 15px;
        padding: 15px;
        height: 300px;
        overflow-y: auto;
    }
    .msg-bubble { background: rgba(168, 85, 247, 0.1); padding: 10px; border-radius: 12px; margin-bottom: 8px; border-left: 4px solid #a855f7; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE NAVEGACIÓN Y CHAT ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"
if 'messages' not in st.session_state:
    st.session_state.messages = [{"user": "Profe_Michi", "text": "¡Hola colegas! ¿Listos para el desafío de hoy?"}]

# --- 4. ESTRUCTURA DE PANTALLA DIVIDIDA ---
col_menu, col_main = st.columns([1, 2])

with col_menu:
    st.title("🚀 Menú")
    if st.button("🏠 Inicio / Comunidad", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"
    if st.button("📓 Escrito Reflexivo", use_container_width=True): st.session_state.seccion = "reflexivo"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📏 ProfeEduca ✏️")
    st.caption("Donde el saber trasciende.")

with col_main:
    # --- SECCIÓN INICIO (COMUNIDAD) ---
    if st.session_state.seccion == "inicio":
        st.markdown(f'<div class="ia-quote-box">✨ Aliento IA: "Tu impacto en la comunidad es infinito."</div>', unsafe_allow_html=True)
        st.markdown('<div class="apple-stage"><span class="worm-move">🐛</span>🍎</div>', unsafe_allow_html=True)
        
        st.subheader("💬 El Café del Maestro (Amistad)")
        chat_html = '<div class="chat-wall">'
        for m in st.session_state.messages:
            chat_html += f'<div class="msg-bubble"><b>@{m["user"]}</b>: {m["text"]}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Saluda a tus colegas:")
            if st.form_submit_button("Enviar Saludo"):
                if user_msg:
                    st.session_state.messages.append({"user": "Tú", "text": user_msg})
                    st.rerun()

    # --- SECCIÓN PLANEACIÓN ABCD (NUEVA FASE 0.4) ---
    elif st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        st.write("Estructura tu tutoría basándote en el diálogo y el desafío.")
        
        tab1, tab2, tab3 = st.tabs(["🎯 Identificación", "🧠 El Desafío", "🤝 Comunidad"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.selectbox("Campo Formativo", ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"])
                st.selectbox("Fase", ["Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6"])
            with col_b:
                st.text_input("Nombre del Tema / Unidad")
                st.text_area("PDA (Procesos de Desarrollo)", height=100)

        with tab2:
            st.subheader("El Motor del Aprendizaje")
            desafio = st.text_area("Plantea el Desafío:",
