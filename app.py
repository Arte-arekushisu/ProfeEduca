from fpdf import FPDF
import datetime

def generar_pdf(datos):
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración de Títulos
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Planeación Pedagógica - Modelo de Aprendizaje Diálogo", ln=True, align='C')
    pdf.ln(5)
    
    # Objetivo General (Máximo 6 párrafos)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Objetivo General", ln=True)
    pdf.set_font("Arial", '', 10)
    objetivo = (
        f"Esta planeación busca que los alumnos de {datos['nivel']} aprendan sobre {datos['tema']} "
        "a través de la investigación activa y el diálogo tutorado. El enfoque principal es la "
        "autonomía, donde el estudiante construye su conocimiento utilizando recursos de su entorno. "
        "Se desarrollarán habilidades de pensamiento crítico, resolución de problemas y vinculación "
        "comunitaria, permitiendo que el saber local se transforme en un aprendizaje significativo."
    )
    pdf.multi_cell(0, 5, objetivo)
    pdf.ln(5)

    # Tabla de Identificación
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 10)
    for clave, valor in datos.items():
        if clave not in ['tema', 'nivel']:
            pdf.cell(50, 8, f"{clave.capitalize()}:", border=1, fill=True)
            pdf.cell(0, 8, str(valor), border=1, ln=True)
    
    pdf.ln(10)
    # Aquí se agregarían las secciones de Estaciones, Tutoreo e IA...
    # (El código completo generaría todas las tablas de lunes a viernes)
    
    # Referencias
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 5, "Referencias: SEP (2022) Plan de Estudios; UNESCO (2021) Reimaginar el futuro.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- DENTRO DEL BOTÓN DE PLANEACIÓN EN STREAMLIT ---
if st.button("🚀 GENERAR PLANEACIÓN EN PDF"):
    # Recolectamos los datos de los inputs de la Fase 0.4
    datos_maestro = {
        "nivel": nivel_seleccionado,
        "grado": grado_input,
        "maestro": nombre_maestro,
        "comunidad": comunidad_input,
        "tema": tema_interes
    }
    
    pdf_bytes = generar_pdf(datos_maestro)
    st.download_button(
        label="📥 Descargar Planeación Completa",
        data=pdf_bytes,
        file_name=f"Planeacion_{tema_interes}.pdf",
        mime="application/pdf"
    )
