if submit:
    with st.spinner("🤖 Conectando con el cerebro de Google..."):
        try:
            # CAMBIO CLAVE: Usamos el nombre técnico completo del modelo
            # Esto ayuda a que el servidor lo encuentre sin importar la versión de la API
            model_id = "models/gemini-1.5-flash"
            
            response = client.models.generate_content(
                model=model_id, 
                contents=f"Genera una planeación pedagógica para {nivel} sobre {tema}. Comunidad: {comunidad}."
            )
            
            if response.text:
                pdf = PlaneacionPDF()
                pdf.add_page()
                pdf.barra("I. DATOS GENERALES")
                pdf.set_font('Helvetica', '', 11)
                pdf.cell(0, 8, clean(f"Educador: {educador} | Tema: {tema}"), 0, 1)
                
                pdf.ln(5); pdf.barra("II. DESARROLLO")
                pdf.multi_cell(0, 6, clean(response.text))

                pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
                st.success("✅ ¡CONSEGUIDO! Ya puedes descargar tu documento.")
                st.download_button("📥 DESCARGAR PDF", pdf_output, f"Planeacion.pdf", "application/pdf")
            else:
                st.warning("La IA no devolvió texto. Revisa tu conexión.")

        except Exception as e:
            # Si sale error, este mensaje nos dirá exactamente qué puerta está cerrada
            st.error(f"Aviso técnico: {e}")
            st.info("Axel, si ves un error de 'API_KEY_INVALID', revisa que no haya espacios extras en tu clave.")
