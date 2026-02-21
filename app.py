import streamlit as st
from fpdf import FPDF
import io

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Profe Educa ABCD", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stTextInput, .stTextArea { background-color: #262730 !important; }
    </style>
    """, unsafe_allow_html=True)

# Función para evitar errores de caracteres especiales en PDF
def limpiar_texto(t):
    replacements = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in replacements.items():
        t = str(t).replace(k, v)
    return t

# 2. CLASE PARA EL REPORTE PDF
class ReporteTrimestral(FPDF):
    def header(self):
        # Espacio para logos (puedes cargar imágenes locales si las tienes)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'TEXTO REFLEXIVO TRIMESTRAL', 0, 1, 'C')
        self.ln(5)

# 3. LÓGICA DE BASE DE DATOS TEMPORAL
if 'alumnos_db' not in st.session_state:
    st.session_state.alumnos_db = {}

# 4. INTERFAZ DE NAVEGACIÓN
menu = st.sidebar.selectbox("Selecciona una sección", ["Registro Diario", "Evaluación Trimestral"])

# --- SECCIÓN REGISTRO ---
if menu == "Registro Diario":
    st.title("✍️ Registro de Avances Diarios")
    nombre = st.text_input("Nombre del Alumno").upper()
    reflexion = st.text_area("Descripción de lo aprendido hoy")
    
    if st.button("Guardar Avance"):
        if nombre and reflexion:
            if nombre not in st.session_state.alumnos_db:
                st.session_state.alumnos_db[nombre] = []
            st.session_state.alumnos_db[nombre].append(reflexion)
            st.success(f"Registro guardado para {nombre}")
        else:
            st.warning("Completa los campos.")

# --- SECCIÓN EVALUACIÓN ---
elif menu == "Evaluación Trimestral":
    st.title("📊 Evaluación Trimestral Estructurada")
    
    busqueda = st.text_input("Buscar Alumno").upper()
    
    if busqueda in st.session_state.alumnos_db:
        # Recuperar historial
        historial = " ".join(st.session_state.alumnos_db[busqueda])
        
        # Formulario de Evaluación
        c1, c2 = st.columns(2) # CORREGIDO: Se agregaron paréntesis
        escuela = c1.text_input("Escuela", "San Nicolas")
        nivel = c2.text_input("Nivel", "4to Primaria")
        
        st.subheader("Campos Formativos")
        f1 = st.text_area("LENGUAJES", historial) # Se pre-carga el historial
        f2 = st.text_area("SABERES Y PENSAMIENTO CIENTÍFICO")
        f3 = st.text_area("ÉTICA, NATURALEZA Y SOCIEDADES")
        f4 = st.text_area("DE LO HUMANO Y LO COMUNITARIO")
        
        recom = st.text_area("RECOMENDACIONES Y COMPROMISOS")

        if st.button("Generar PDF"):
            pdf = ReporteTrimestral()
            pdf.add_page()
            
            # Datos Generales
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 5, f"Nombre de la Escuela: {limpiar_texto(escuela)}", 0, 1)
            pdf.cell(0, 5, f"Nivel: {limpiar_texto(nivel)}", 0, 1)
            pdf.cell(0, 5, f"Alumno: {limpiar_texto(busqueda)}", 0, 1)
            pdf.ln(10)

            # Secciones (Campos Formativos)
            secciones = [
                ("LENGUAJES", f1),
                ("SABERES Y PENSAMIENTOS CIENTIFICOS", f2),
                ("ETICA, NATURALEZA Y SOCIEDADES", f3),
                ("DE LO HUMANO Y LO COMUNITARIO", f4)
            ]

            for titulo, contenido in secciones:
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 8, titulo, 0, 1, 'C')
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, limpiar_texto(contenido))
                pdf.ln(4)

            # Firmas al final
            pdf.ln(20)
            pdf.line(20, pdf.get_y(), 80, pdf.get_y())
            pdf.line(120, pdf.get_y(), 180, pdf.get_y())
            pdf.set_font("Arial", '', 8)
            pdf.text(25, pdf.get_y() + 5, "Firma del EC.")
            pdf.text(125, pdf.get_y() + 5, "Firma del Padre de Familia.")

            # Descarga
            output = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Reporte", output, f"Evaluacion_{busqueda}.pdf")
    else:
        st.info("Alumno no encontrado. Asegúrate de haberlo registrado en la sección 'Registro Diario'.")
