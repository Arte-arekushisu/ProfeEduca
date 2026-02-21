# --- SECCIÓN PLANEACIÓN ABCD (FASE 0.4 CORREGIDA) ---
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
            # AQUÍ ESTABA EL ERROR, YA ESTÁ CORREGIDO:
            desafio = st.text_area(
                "Plantea el Desafío:", 
                placeholder="Ej. ¿Cómo explicar por qué llueve sin lagos cerca?",
                help="Debe ser una pregunta que invite a investigar."
            )
            st.info("💡 Un buen desafío ABCD no se responde con un 'sí' o 'no'.")

        with tab3:
            st.subheader("Vinculación Local")
            st.text_area("¿Cómo se relaciona esto con la comunidad?", height=100)
            st.text_area("Recursos del entorno (materiales locales)", height=100)
            
            st.markdown("---")
            if st.button("🚀 GENERAR PLANEACIÓN CON IA", use_container_width=True):
                st.success("¡Analizando datos! En la Fase 0.5 conectaremos esto con Gemini.")
