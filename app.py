import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io
import datetime

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(-45deg, #050505, #1a1c24, #004d66, #050505); 
        background-size: 400% 400%; 
        animation: gradient 15s ease infinite; 
        color: white; 
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .stTextInput width, .stTextArea width { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES TÉCNICAS
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_Reporte(FPDF):
    def __init__(self, logo_izq=None, logo_der=None):
        super().__init__()
        self.logo_izq = logo_izq
        self.logo_der = logo_der

    def header(self):
        if self.logo_izq:
            self.image(self.logo_izq, 10, 8, 33)
        if self.logo_der:
            self.image(self.logo_der, 165, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.ln(10)
        self.cell(0, 10, 'Texto Reflexivo Trimestral', 0, 1, 'C')
        self.ln(5)

# 3. BASE DE DATOS DE SESIÓN
if 'db' not in st.session_state:
    st.session_state.db = {"auth": True, "user_data": {"admin": {"name": "Educador"}}, "alumnos": {}}

# --- MENÚ ---
st.sidebar.title("Panel de Control")
menu = st.sidebar.radio("Ir a:", ["✍️ Diario Reflexivo", "📊 Generar Evaluación"])

# --- MODULO 1: DIARIO REFLEXIVO (CON TEMAS DE INTERÉS) ---
if menu == "✍️ Diario Reflexivo":
    st.header("📝 Registro de Avances Diarios")
    col_a, col_b = st.columns(2)
    
    with col_a:
        nom_alumno = st.text_input("Nombre del Alumno").upper()
        temas = st.text_input("Temas de interés hoy (ej: Ciclo del agua, Fracciones)")
    
    texto_hoy = st.text_area("Escrito reflexivo del día")
    
    if st.button("Guardar en Base de Datos"):
        if nom_alumno and texto_hoy:
            if nom_alumno not in st.session_state.db["alumnos"]:
                st.session_state.db["alumnos"][nom_alumno] = {"diario": [], "temas": []}
            
            st.session_state.db["alumnos"][nom_alumno]["diario"].append(texto_hoy)
            st.session_state.db["alumnos"][nom_alumno]["temas"].append(temas)
            st.success(f"Log registrado para {nom_alumno}")

# --- MODULO 2: EVALUACIÓN (ESTRUCTURA DE CUADROS) ---
elif menu == "📊 Generar Evaluación":
    st.header("Generador de Reporte Estructurado")
    
    with st.expander("🖼️ Configuración de Imagenes y Logos", expanded=True):
        col1, col2 = st.columns(2)
        logo1 = col1.file_uploader("Subir Logo Izquierdo (CONAFE)", type=["jpg", "png"])
        logo2 = col2.file_uploader("Subir Logo Derecho (Proyecto)", type=["jpg", "png"])

    with st.form("form_eval"):
        c1, c2, c3 = st.columns(3)
        alumno_busc = c1.text_input("Nombre del Alumno a evaluar").upper()
        nivel_esc = c2.text_input("Nivel / Grado", "4to Primaria")
        escuela = c3.text_input("Nombre de la Escuela", "San Nicolas")
        
        c4, c5 = st.columns(2)
        nombre_ec = c4.text_input("Nombre del Educador (Manual)")
        nombre_eca = c5.text_input("Nombre del ECA (Manual)")

        st.subheader("Campos Formativos (Sintetizar de la Base de Datos)")
        f1 = st.text_area("LENGUAJES", height=100)
        f2 = st.text_area("SABERES Y PENSAMIENTO CIENTÍFICO", height=100)
        f3 = st.text_area("ETICA, NATURALEZA Y SOCIEDADES", height=100)
        f4 = st.text_area("DE LO HUMANO Y LO COMUNITARIO", height=100)
        f5 = st.text_area("PROYECTO COMUNITARIO (Nuevo)", height=80)
        
        st.subheader("Recomendaciones y Compromisos")
        recom = st.text_area("Escriba las recomendaciones finales")

        generar = st.form_submit_button("GENERAR DOCUMENTO FORMAL")

    if generar:
        # Recuperar temas de interés de la DB para incluirlos
        temas_acumulados = ""
        if alumno_busc in st.session_state.db["alumnos"]:
            temas_acumulados = ", ".join(filter(None, st.session_state.db["alumnos"][alumno_busc]["temas"]))

        pdf = PDF_Reporte(logo1, logo2)
        pdf.add_page()
        
        # Datos Generales
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 5, f"Nombre de la Escuela: {limpiar(escuela)}", 0, 1, 'C')
        pdf.cell(0, 5, f"Nivel: {limpiar(nivel_esc)}", 0, 1, 'C')
        pdf.ln(2)
        pdf.cell(0, 8, f"Nombre del alumno: {limpiar(alumno_busc)}", 0, 1, 'C')
        
        if temas_acumulados:
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(0, 5, f"Temas de interes detectados: {limpiar(temas_acumulados)}", 0, 1, 'C')

        # Secciones de Cuadros
        secciones = [
            ("LENGUAJES", f1),
            ("SABERES Y PENSAMIENTOS CIENTIFICOS", f2),
            ("ETICA, NATURALEZA Y SOCOCIEDADES", f3),
            ("DE LO HUMANO Y LO COMUNITARIO", f4),
            ("PROYECTO COMUNITARIO", f5)
        ]

        for titulo, contenido in secciones:
            pdf.ln(3)
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 7, titulo, 1, 1, 'C', fill=True)
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(0, 5, limpiar(contenido) if contenido else "Sin informacion registrada.", 1, 'L')

        # Recomendaciones
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, "RECOMENDACION Y COMPROMISOS", 0, 1, 'L')
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 5, limpiar(recom))

        # Firmas
        pdf.ln(20)
        y_firma = pdf.get_y()
        pdf.line(20, y_firma, 90, y_firma)
        pdf.line(110, y_firma, 180, y_firma)
        pdf.set_y(y_firma + 2)
        pdf.set_x(20)
        pdf.cell(70, 5, f"Nombre y firma del EC: {limpiar(nombre_ec)}", 0, 0, 'C')
        pdf.set_x(110)
        pdf.cell(70, 5, "Nombre y firma del padre de familia", 0, 1, 'C')

        # Descarga
        pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 Descargar Texto Reflexivo PDF", pdf_output, f"Reporte_{alumno_busc}.pdf")
