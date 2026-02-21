import streamlit as st

# --- 1. CONFIGURACIÓN ---
# (Asumimos que la configuración de página y CSS ya están cargados de las versiones anteriores)

# --- 2. LÓGICA DE NAVEGACIÓN (Actualizada para V0.4) ---
if 'seccion' not in st.session_state:
    st.session_state.seccion = "inicio"

# --- 3. DISEÑO DE PANTALLA (CONTENIDO DEL ÁREA DE PLANEACIÓN) ---
# Este bloque se ejecuta cuando el usuario hace clic en "📝 Planeación ABCD"

if st.session_state.seccion == "plan":
    st.title("📋 Generador de Planeación ABCD")
    st.markdown("---")
    
    # Usaremos pestañas (Tabs) para que el proceso sea ordenado
    tab_datos, tab_desafio, tab_comunidad = st.tabs([
        "📍 Datos Generales", 
        "🧠 El Gran Desafío", 
        "🏠 Vinculación Comunitaria"
    ])
    
    with tab_datos:
        st.subheader("Configuración de la Lección")
        col1, col2 = st.columns(2)
        with col1:
            campo = st.selectbox("Campo Formativo", [
                "Lenguajes", 
                "Saberes y Pensamiento Científico", 
                "Ética, Naturaleza y Sociedades", 
                "De lo Humano y lo Comunitario"
            ])
            fase = st.selectbox("Fase / Grado", ["Fase 2 (Prescolar)", "Fase 3 (1º y 2º)", "Fase 4 (3º y 4º)", "Fase 5 (5º y 6º)", "Fase 6 (Secundaria)"])
        with col2:
            tema = st.text_input("Nombre de la Unidad de Aprendizaje", placeholder="Ej. El ciclo del agua")
            pda = st.text_area("PDA (Proceso de Desarrollo de Aprendizaje)", placeholder="Copia aquí el proceso que deseas trabajar...")

    with tab_desafio:
        st.subheader("El Motor del Aprendizaje")
        desafio = st.text_area("Escribe el Desafío o Pregunta Detonadora:", 
            placeholder="Ej. ¿Cómo podríamos explicarle a alguien de otra comunidad por qué ll
