import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

# Estilo visual de la App (Mantenemos tu gradiente y diseño moderno)
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); 
        background-size: 400% 400%; 
        animation: gradient 15s ease infinite; 
        color: white; 
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-card { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 15px; margin: 10px; border-left: 5px solid #00d4ff; }
    .profile-pic { border-radius: 50%; width: 50px; height: 50px; object-fit: cover; border: 2px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. CLASE PDF PROFESIONAL (ESTILO CONAFE)
class PDF_PRO(FPDF):
    def header(self):
        # Aquí podrías añadir logos si tuvieras los archivos locales
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Texto Reflexivo Trimestral', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Sistema Integral ABCD', 0, 1, 'C')
        self.ln(10)

    def seccion_titulo(self, titulo):
        self.set_fill_color(240, 240, 240)
        self.set_font('Arial', 'B', 11)
        self.cell(0, 8, limpiar(titulo), 1, 1, 'C', fill=True)
        self.ln(2)

    def bloque_campo(self, nombre_campo, contenido):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 51, 102) # Azul oscuro
        self.cell(0, 6, limpiar(nombre_campo.upper()), 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 5, limpiar(contenido), 0, 'J')
        self.ln(4)

def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

# 3. BASE DE DATOS Y LÓGICA (Mantenemos tus funciones anteriores)
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user_data": {}, "alumnos": {}, 
        "comentarios": [{"user": "Admin", "text": "¡Bienvenidos a la era ABCD!", "pic": ""}]
    }

# --- (Omitido por brevedad: Código de Login y Registro igual al anterior) ---
# [Aquí va tu bloque de login/registro anterior]
if not st.session_state.db["auth"]:
    st.info("Por favor, inicia sesión para continuar.")
    # ... (Tu código de login original funciona perfecto aquí)
    st.session_state.db["auth"] = True # Simulación para este ejemplo
    st.session_state.db["user"] = "admin"
    st.session_state.db["user_data"]["admin"] = {"name": "Educador", "pic": ""}

else:
    menu = st.sidebar.radio("MENÚ", ["🏠 Inicio", "✍️ Diario Reflexivo", "📊 Evaluación"])

    if menu == "✍️ Diario Reflexivo":
        st.header("Registro de Avances Diarios")
        alumno = st.text_input("Nombre del Alumno").upper()
        # Campos por Campo Formativo para mayor orden
        c1, c2 = st.columns(2)
        lang = c1.text_area("Lenguajes (Avances)")
        saberes = c2.text_area("Saberes y Pensamiento Científico")
        etica = c1.text_area("Ética, Naturaleza y Sociedades")
        comu = c2.text_area("De lo Humano y lo Comunitario")
        
        if st.button("Guardar Registro"):
            if alumno:
                st.session_state.db["alumnos"][alumno] = {
                    "Lenguajes": lang, "Saberes": saberes, 
                    "Etica": etica, "Comunitario": comu
                }
                st.success(f"Datos de {alumno} actualizados.")

    elif menu == "📊 Evaluación":
        st.header("Generador de Reporte Profesional")
        busqueda = st.text_input("Buscar Alumno").upper()
        
        if busqueda in st.session_state.db["alumnos"]:
            datos = st.session_state.db["alumnos"][busqueda]
            escuela = st.text_input("Nombre de la Escuela", "San Nicolas")
            grado = st.text_input("Nivel/Grado", "4to Primaria")
            
            if st.button("Generar PDF Estilo Profesional"):
                pdf = PDF_PRO()
                pdf.add_page()
                
                # Encabezado de Datos
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 5, f"Nombre de la Escuela: {escuela}", 0, 1)
                pdf.cell(0, 5, f"Nivel: {grado}", 0, 1)
                pdf.cell(0, 5, f"Nombre del alumno: {busqueda}", 0, 1)
                pdf.ln(5)
                
                pdf.seccion_titulo("CAMPOS FORMATIVOS")
                
                # Bloques de contenido (Sintetizados de la base de datos)
                pdf.bloque_campo("Lenguajes", datos.get("Lenguajes", "Sin registro"))
                pdf.bloque_campo("Saberes y Pensamientos Científicos", datos.get("Saberes", "Sin registro"))
                pdf.bloque_campo("Ética, Naturaleza y Sociedades", datos.get("Etica", "Sin registro"))
                pdf.bloque_campo("De lo Humano y lo Comunitario", datos.get("Comunitario", "Sin registro"))
                
                # Cuadro de firmas
                pdf.ln(10)
                y_actual = pdf.get_y()
                pdf.line(10, y_actual, 90, y_actual)
                pdf.line(110, y_actual, 190, y_actual)
                pdf.set_font('Arial', 'B', 8)
                pdf.text(30, y_actual + 5, "Nombre y firma del EC.")
                pdf.text(125, y_actual + 5, "Nombre y firma del padre de familia.")

                pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button("📥 Descargar PDF Profesional", pdf_output, f"Reporte_{busqueda}.pdf")
        else:
            st.warning("Busca un alumno registrado en el Diario.")
