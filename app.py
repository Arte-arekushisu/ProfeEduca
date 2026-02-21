import streamlit as st
import random

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V0.3 | Comunidad", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS (ANIMACIONES, CHAT Y BOTONES) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Animación del Gusanito: Entra por un lado, sale por otro */
    @keyframes worm-peek {
        0% { transform: translate(40px, 0px) scale(0); opacity: 0; }
        30% { transform: translate(30px, -30px) scale(1.2); opacity: 1; }
        50% { transform: translate(0px, -45px) rotate(15deg); }
        70% { transform: translate(-30px, -30px) scale(1.2); opacity: 1; }
        100% { transform: translate(-40px, 0px) scale(0); opacity: 0; }
    }
    .apple-stage { position: relative; font-size: 7rem; text-align: center; margin: 10px 0; }
    .worm-move { position: absolute; font-size: 2.5rem; animation: worm-peek 5s infinite; left: 47%; top: 15%; }

    /* Estilo del Chat de Amistad (Tipo Discord) */
    .chat-wall {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.4); /* Color morado para amistad */
        border-radius: 15px;
        padding: 20px;
        height: 350px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .msg-bubble {
        background: rgba(168, 85, 247, 0.1);
        padding: 12px;
        border-radius: 15px;
        border-left: 4px solid #a855f7;
    }
    .user-id { color: #a855f7; font-weight: 800; font-size: 0.85rem; margin-bottom: 4px; display: block; }
    .msg-text { color: #f1f5f9; font-size: 1rem; }

    /* Frase Motivadora IA */
    .ia-quote-box {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE ESTADO (MEMORIA DEL CHAT) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"user": "Profe_Michi", "text": "¡Hola a todos! ¿Cómo va su café de la mañana?"},
        {"user": "Educa_Gael", "text": "¡Qué onda Michi! Aquí saludando desde el fresco de la sierra."},
        {"user": "Maestra_Paty", "text": "Hola equipo, ¡tengan un excelente y bendecido día!"}
    ]

if 'seccion' not in st.session_state:
    st.session_state.seccion = "inicio"

# --- 4. DISEÑO DE PANTALLA DIVIDIDA ---
col_menu, col_main = st.columns([1, 1.8])

with col_menu:
    st.title("🚀 Menú")
    if st.button("🏠 Inicio / Comunidad", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"
    if st.button("📓 Escrito Reflexivo", use_container_width=True): st.session_state.seccion = "reflexivo"
    if st.button("📅 Diario del Maestro", use_container_width=True): st.session_state.seccion = "diario"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📏 ProfeEduca ✏️")
    st.caption("Conectando corazones educadores.")

with col_main:
    if st.session_state.seccion == "inicio":
        # Frase Motivadora IA
        frases = [
            "Tu sonrisa es el primer paso para que un niño quiera aprender.",
            "No solo enseñas letras, regalas oportunidades de vida.",
            "Eres el ejemplo de resiliencia que México necesita.",
            "Tómate un respiro, lo estás haciendo increíble."
        ]
        st.markdown(f'<div class="ia-quote-box">✨ Palabra de Aliento: "{random.choice(frases)}"</div>', unsafe_allow_html=True)

        # Animación Manzana/Gusanito
        st.markdown("""
            <div class="apple-stage">
                <span class="worm-move">🐛</span>🍎
            </div>
        """, unsafe_allow_html=True)

        # Chat de Amistad Abierto
        st.subheader("💬 El Café del Maestro (Espacio de Amistad)")
        st.write("Un lugar para saludarnos y platicar, ¡fuera de las planeaciones!")
        
        # Renderizado de mensajes
        chat_html = '<div class="chat-wall">'
        for m in st.session_state.messages:
            chat_html += f'''
                <div class="msg-bubble">
                    <span class="user-id">@{m["user"]}</span>
                    <span class="msg-text">{m["text"]}</span>
                </div>
            '''
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        # Input de mensaje
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Saluda a la comunidad:", placeholder="Escribe un 'Hola'...")
            if st.form_submit_button("Enviar Saludo 📤"):
                if user_msg:
                    st.session_state.messages.append({"user": "Tú", "text": user_msg})
                    st.rerun()

    elif st.session_state.seccion == "plan":
        st.title("📝 Área de Planeación ABCD")
        st.info("Fase 0.2 intacta. Aquí trabajaremos la lógica de Gemini próximamente.")
