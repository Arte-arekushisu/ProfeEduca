# --- AGREGAR ESTO AL INICIO (NUEVA CLASE PARA EL PDF DE FACTURA) ---
class FacturaPDF(FPDF):
    def header(self):
        self.set_fill_color(33, 47, 61)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 20, clean('COMPROBANTE DE PAGO - PROFEEDUCA'), 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, clean('Gracias por contribuir a la educacion comunitaria.'), 0, 0, 'C')

# --- DENTRO DEL CUERPO PRINCIPAL (AÑADIR PESTAÑAS) ---
tabs = st.tabs(["📊 Evaluaciones", "💳 Facturacion"])

with tabs[0]:
    # (Aquí va todo el código de evaluaciones que ya tenemos)
    st.write("Sección de reportes terminada.")

with tabs[1]:
    st.header("🧾 Generación de Comprobantes")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        razon_social = st.text_input("Razón Social / Nombre Receptor")
        rfc = st.text_input("RFC / Identificación Fiscal")
        correo_fac = st.text_input("Correo Electrónico")
    
    with col_f2:
        metodo_pago = st.selectbox("Método de Pago", ["Transferencia", "Efectivo", "Tarjeta"])
        monto = st.number_input("Monto total", min_value=0.0, format="%.2f")
        fecha_pago = st.date_input("Fecha de operación")

    concepto = st.text_area("Concepto del pago", placeholder="Ej. Aportación voluntaria trimestre 1...")

    if st.button("📝 GENERAR FACTURA PDF", use_container_width=True):
        if not razon_social or monto <= 0:
            st.error("⚠️ Indica la razón social y un monto válido.")
        else:
            f_pdf = FacturaPDF()
            f_pdf.add_page()
            f_pdf.set_font('Helvetica', '', 12)
            
            # Datos de la operación
            f_pdf.set_fill_color(240, 240, 240)
            f_pdf.cell(0, 10, clean(f"FECHA: {fecha_pago}"), 0, 1, 'R')
            f_pdf.ln(5)
            
            f_pdf.set_font('Helvetica', 'B', 12)
            f_pdf.cell(0, 10, clean("DATOS DEL RECEPTOR:"), 0, 1)
            f_pdf.set_font('Helvetica', '', 11)
            f_pdf.multi_cell(0, 7, clean(f"Nombre: {razon_social}\nRFC: {rfc}\nCorreo: {correo_fac}"))
            
            f_pdf.ln(10)
            
            # Tabla de concepto
            f_pdf.set_font('Helvetica', 'B', 11)
            f_pdf.set_fill_color(33, 47, 61); f_pdf.set_text_color(255, 255, 255)
            f_pdf.cell(140, 10, clean(" CONCEPTO"), 1, 0, 'L', True)
            f_pdf.cell(50, 10, clean(" TOTAL"), 1, 1, 'C', True)
            
            f_pdf.set_text_color(0, 0, 0); f_pdf.set_font('Helvetica', '', 11)
            f_pdf.cell(140, 20, clean(concepto), 1, 0, 'L')
            f_pdf.cell(50, 20, f"${monto:,.2f}", 1, 1, 'C')
            
            f_pdf.ln(20)
            f_pdf.image(io.BytesIO(f_pdf.output()), x=150, y=f_pdf.get_y(), w=30) # Espacio para QR o Sello
            
            st.download_button("📥 DESCARGAR COMPROBANTE", bytes(f_pdf.output()), f"Factura_{razon_social}.pdf", "application/pdf")
            st.success("Comprobante generado exitosamente.")
