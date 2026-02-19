elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación Semanal: {nivel}")
    col1, col2 = st.columns(2)
    with col1:
        tema_p = st.text_input("Tema de la Unidad (UAA):")
        rincón_p = st.text_input("Rincón Permanente a usar:", placeholder="Ej. Rincón de Lectura / Rincón de Ciencia")
    with col2:
        objetivo = st.text_area("Objetivo General:")

    if st.button("🚀 Generar Planeación Completa"):
        with st.spinner("Preparando jornada y materiales de estudio..."):
            prompt = f"""
            Actúa como experto pedagogo CONAFE. Genera una planeación SEMANAL (Lunes a Viernes) para {nivel}.
            TEMA: {tema_p} | RINCÓN PERMANENTE: {rincón_p} | OBJETIVO: {objetivo}.
            
            ESTRUCTURA DIARIA (Sin asteriscos):
            - Horarios desde Bienvenida (8:00) hasta Cierre (14:00).
            - Propuesta de una ESTACIÓN DE TRABAJO semanal para el rincón {rincón_p}.
            - Momentos de Relación Tutora y Regalo de Lectura.
            
            SECCIÓN DE PREPARACIÓN DEL EDUCADOR:
            1. Enlaces sugeridos: Proporciona frases de búsqueda para YouTube y Google que lleven a videos educativos y documentos PDF sobre {tema_p}.
            2. Guía de estudio rápido: 3 conceptos técnicos sobre el tema que el educador debe dominar para resolver dudas.
            3. Material de lectura: Sugiere títulos de libros de la biblioteca de aula o temas de la unidad que se relacionen.
            
            Incluye 2 temas de reserva. Sin firmas.
            """
            resultado = llamar_ia(prompt)
            st.markdown(resultado)
            st.download_button(
                label="📥 Descargar Planeación (Word)", 
                data=generar_word_planeacion("PLANEACIÓN SEMANAL", resultado, datos_id), 
                file_name=f"Planeacion_{tema_p}.docx"
            )
