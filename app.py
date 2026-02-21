# --- LADO DERECHO: CONTENIDO DINÁMICO ---
with col_main:
    # Bloque de INICIO (Asegúrate de que este 'if' esté alineado con el 'elif' de abajo)
    if st.session_state.seccion == "inicio":
        st.markdown('✨ **IA Motivadora:** "Tu impacto en la comunidad es infinito."')
        st.markdown('<div class="apple-stage"><span class="worm-move">🐛</span>🍎</div>', unsafe_allow_html=True)
        
        st.subheader("💬 El Café del Maestro (Amistad)")
        # ... (aquí va tu código del chat)

    # Bloque de PLANEACIÓN (Aquí estaba el error de indentación)
    elif st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        st.write("Estructura tu tutoría basándote en el diálogo y el desafío.")
        
        tab1, tab2, tab3 = st.tabs(["🎯 Identificación", "🧠 El Desafío", "🤝 Comunidad"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.selectbox("Campo Formativo", [
                    "Lenguajes", 
                    "Saberes y Pensamiento Científico", 
                    "Ética, Naturaleza y Sociedades", 
                    "De lo Humano y lo Comunitario"
                ])
                st.selectbox("Fase", ["Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6"])
            with col_b:
                st.text_input("Nombre del Tema / Unidad")
                st.text_area("PDA (Procesos de Desarrollo)", height=100)

        with tab2:
            st.subheader("El Motor del Aprendizaje")
            desafio = st.text_area(
                "Plantea el Desafío:", 
                placeholder="Ej. ¿Cómo explicar por qué llueve sin lagos cerca?",
                help="Debe ser una pregunta que invite a investigar."
            )

        with tab3:
            st.subheader("Vinculación Local")
            st.text_area("¿Cómo se relaciona esto con la comunidad?", height=100)
            st.text_area("Recursos del entorno (materiales locales)", height=100)
            
            if st.button("🚀 GENERAR PLANEACIÓN CON IA", use_container_width=True):
                st.success("¡Analizando datos! En la Fase 0.5 conectaremos esto con Gemini.")
