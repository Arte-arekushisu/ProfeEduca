import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca | Versión 0.2", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Fondo General Unificado */
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Contenedor Izquierdo (Lista de Navegación) */
    .nav-list {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 20px;
    }

    /* Animación del Gusanito entrando y saliendo de la manzana */
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        25% { transform: translate(30px, -45px) scale(1.1); opacity: 1; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
        75% { transform: translate(-30px, -45px) scale(1.1); opacity: 1; }
        90% { transform: translate(-45px, -30px) scale(1); opacity: 0; }
    }
    
    .apple-container {
        position: relative;
        display: inline-block;
        font-size: 8rem;
        margin-top: 50px;
    }
    
    .worm-icon {
        position: absolute;
        font-size: 3rem;
        animation: worm-move 5s ease-in-out infinite;
    }

    /* Estilo del Nombre con Regla y Lápiz unidos */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-size: 2.5rem;
        font-weight: 900;
        color: #38bdf8;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    .slogan-final {
        font-style: italic;
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 400px;
        margin: 20px auto;
        line-height: 1.6;
    }

    /* Botones de la lista izquierda */
    .stButton>button {
        text-align: left;
        padding: 15px;
        font-size: 1.1rem;
        background: transparent;
        color: #f8fafc;
        border: none;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(56, 189, 248, 0.1);
        padding-left: 25px;
        color: #38bdf8;
        border-bottom: 1px solid #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DISEÑO DE PANTALLA DIVIDIDA ---
col_menu, col_visual = st.columns([1, 1.5])

# LADO IZQUIERDO: LISTA DE OPCIONES
with col_menu:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🚀 Menú Maestro")
    
    # Lista de botones como solicitaste
    if st.button("🏠 Inicio"): st.session_state.p = "inicio"
    if st.button("📝 Planeación ABCD"): st.session_state.p = "plan"
    if st.button("📓 Escrito Reflexivo"): st.session_state.p = "reflexivo"
    if st.button("📅 Diario del Maestro"): st.session_state.p = "diario"
    if st.button("📊 Estadísticas"): st.session_state.p = "stats"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Ecosistema Digital ProfeEduca © 2026")

# LADO DERECHO: IDENTIDAD Y ANIMACIÓN
with col_visual:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    
    # Animación de la Manzana y el Gusanito
    st.markdown("""
        <div class="apple-container">
            <span class="worm-icon">🐛</span>
            🍎
        </div>
    """, unsafe_allow_html=True)
    
    # Nombre de marca con Regla y Lápiz unidos
    st.markdown("""
        <div class="brand-header">
            📏 ProfeEduca ✏️
        </div>
        <div style="font-weight: 700; color: white; margin-top: 10px;">
            PLANEACIONES PARA EL MAESTRO ABCD
        </div>
        <div class="slogan-final">
            "Guía de luz en las comunidades más remotas, transformando cada desafío en una oportunidad para el México del mañana."
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. CONTENIDO DINÁMICO (Debajo del menú) ---
st.divider()
if 'p' not in st.session_state: st.session_state.p = "inicio"

if st.session_state.p == "inicio":
    st.subheader("Bienvenido al Centro de Innovación Pedagógica")
    st.write("Tu centro de mando está listo para operar bajo el modelo de aprendizaje autónomo.")
