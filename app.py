import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca | Versión 0.2", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS AVANZADOS ---
st.markdown("""
    <style>
    /* Fondo General */
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* Animación de "Levitación" para los iconos */
    @keyframes floating {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    .animated-icons {
        font-size: 5rem;
        display: inline-block;
        animation: floating 4s ease-in-out infinite;
        filter: drop-shadow(0 0 15px rgba(56, 189, 248, 0.5));
    }

    /* Contenedor de Identidad (Ahora a la derecha) */
    .brand-card-right {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #38bdf8;
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: -10px 10px 30px rgba(0, 0, 0, 0.5);
    }

    .brand-profe {
        color: #38bdf8;
        font-size: 2rem;
        font-weight: 900;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        margin: 10px 0;
    }

    /* Menú Superior Estilizado */
    .top-menu {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 15px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 15px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-bottom: 30px;
    }

    /* Eslogan */
    .slogan-box {
        font-style: italic;
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.6;
        border-top: 1px solid rgba(56, 189, 248, 0.2);
        padding-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MENÚ DE NAVEGACIÓN SUPERIOR ---
# Usamos columnas para simular una barra de herramientas superior
st.markdown('<div class="top-menu">', unsafe_allow_html=True)
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    btn_inicio = st.button("🏠 INICIO", use_container_width=True)
with col_nav2:
    btn_plan = st.button("📝 PLANEACIÓN ABCD", use_container_width=True)
with col_nav3:
    btn_stats = st.button("📊 ESTADÍSTICAS", use_container_width=True)
with col_nav4:
    btn_user = st.button("👤 MI PERFIL", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Lógica simple de navegación
if 'page' not in st.session_state:
    st.session_state.page = "inicio"

if btn_inicio: st.session_state.page = "inicio"
if btn_plan: st.session_state.page = "plan"

# --- 4. CUERPO PRINCIPAL (Layout Invertido) ---
col_main, col_brand = st.columns([2, 1])

with col_main:
    if st.session_state.page == "inicio":
        st.title("🚀 Centro de Innovación Pedagógica")
        st.subheader("Bienvenido al entorno profesional ProfeEduca")
        
        st.markdown("""
        Desde este panel principal, tendrás acceso a todas las herramientas de planeación 
        optimizadas para el modelo educativo comunitario. 
        """)
        
        # Tarjetas informativas
        c1, c2 = st.columns(2)
        with c1:
            st.info("💡 **Dato del día:** El aprendizaje basado en desafíos fomenta la autonomía.")
        with c2:
            st.success("✅ **Sistema IA:** Gemini está listo para generar tu próxima planeación.")

    elif st.session_state.page == "plan":
        st.title("📋 Generador de Planeación ABCD")
        st.write("Configura los parámetros de tu lección aquí.")
        # Aquí irá el contenido de la Fase 0.3

with col_brand:
    # Panel de Identidad a la derecha con animación
    st.markdown(f"""
        <div class="brand-card-right">
            <div class="animated-icons">🍎🐛</div>
            <div class="animated-icons" style="animation-delay: 1s;">📏✏️</div>
            <div style="color:white; font-weight:800; font-size: 1.1rem; margin-top:15px;">
                PLANEACIONES PARA EL<br>MAESTRO ABCD
            </div>
            <div class="brand-profe">ProfeEduca 🍎</div>
            <div class="slogan-box">
                "Guía de luz en las comunidades más remotas,<br>
                transformando cada desafío en una oportunidad,<br>
                porque el saber no conoce fronteras ni distancias,<br>
                educando con el corazón para el México del mañana."
            </div>
        </div>
    """, unsafe_allow_html=True)
