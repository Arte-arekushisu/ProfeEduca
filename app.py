import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca | Versión 0.2", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS (DISEÑO EMPRESARIAL EDUCATIVO) ---
st.markdown("""
    <style>
    /* Fondo General Profundo */
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Contenedor de Identidad en la Barra Lateral */
    .brand-container {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #38bdf8;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.2);
        margin-bottom: 25px;
    }

    /* Título de Planeación con Iconos */
    .nav-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.3;
        margin: 15px 0;
        text-transform: uppercase;
    }

    /* Nombre de la Marca */
    .brand-profe {
        color: #38bdf8;
        font-size: 1.8rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    /* Eslogan Profesional para Maestros */
    .slogan-box {
        font-style: italic;
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid rgba(56, 189, 248, 0.2);
        line-height: 1.5;
    }

    /* Botones de Navegación */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        border: 1px solid #38bdf8;
        transition: all 0.3s;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: #38bdf8;
        color: #020617;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA LATERAL (SIDEBAR) - IDENTIDAD ---
with st.sidebar:
    # Bloque de Identidad solicitado
    st.markdown(f"""
        <div class="brand-container">
            <div style="font-size: 4rem; margin-bottom: 10px;">🍎🐛📏✏️</div>
            <div class="nav-title">
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
    
    st.divider()
    
    # Navegación
    opcion = st.radio("MENÚ DE CONTROL", ["🏠 Inicio", "📝 Área de Planeación ABCD", "📊 Mis Estadísticas", "💬 Comunidad"], label_visibility="collapsed")

# --- 4. ÁREA DE TRABAJO DINÁMICA ---
if opcion == "🏠 Inicio":
    st.title("🚀 Bienvenida, Maestro(a)")
    st.markdown("""
    ### Tu centro de innovación pedagógica está listo.
    Desde aquí podrás gestionar tus secuencias didácticas basadas en el **Modelo ABCD**. 
    Este ecosistema ha sido diseñado para potenciar la labor educativa en contextos comunitarios.
    
    **¿Qué deseas hacer hoy?**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Dato ABCD:** El diálogo es el motor del aprendizaje autónomo.")
    with col2:
        st.success("✅ **Suscripción:** Tu plan está activo y listo para generar.")

elif opcion == "📝 Área de Planeación ABCD":
    st.title("📋 Área de Planeación ABCD")
    st.write("Estructura tu clase con el poder de la IA y el modelo oficial.")
    # Aquí irá la Fase 0.3...
