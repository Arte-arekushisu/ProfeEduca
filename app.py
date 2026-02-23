import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time
from PIL import Image
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

# Inicializar estados si no existen
if "step" not in st.session_state:
    st.session_state.step = "login"
if "p" not in st.session_state:
    st.session_state.p = "home"
if "db" not in st.session_state:
    st.session_state.db = {"usuarios": {}, "temp": {}}

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

# --- 2. CLASES DE PDF (Módulos 0.4, 0.5, 0.7) ---
class PlaneacionPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('PLANEACION SEMANAL'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, eca, comunidad, fecha, nivel, grado):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(95, 8, clean(f" EC: {ec}"), 1, 0, 'L', True)
        self.cell(95, 8, clean(f" ECA: {eca}"), 1, 1, 'L', True)
        self.cell(95, 8, clean(f" COMUNIDAD: {comunidad}"), 1, 0, 'L')
        self.cell(95, 8, clean(f" FECHA: {fecha}"), 1, 1, 'L')
        self.cell(95, 8, clean(f" NIVEL: {nivel}"), 1, 0, 'L', True)
        self.cell(95, 8, clean(f" GRADO: {grado}"), 1, 1, 'L', True)
        self.ln(5)

    def seccion_dia(self, dia):
        self.set_fill_color(128, 0, 0)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, clean(f" {dia}"), 0, 1, 'L', True)
        self.ln(2)

# --- 3. LÓGICA DE INTERFAZ ---

# MÓDULO: LOGIN (Basado en Fase 0.1)
if st.session_state.step == "login":
    st.title("🍎 Bienvenid@ a ProfeEduca")
    col1, col2 = st.columns(2)
    with col1:
        user = st.text_input("Usuario (Correo)")
        pw = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            st.session_state.step = "dashboard"
            st.rerun()

# MÓDULO: DASHBOARD (Basado en Fase 0.2/0.3)
elif st.session_state.step == "dashboard":
    with st.sidebar:
        st.header("Menú Principal")
        if st.button("🏠 Inicio"): st.session_state.p = "home"
        if st.button("📝 Planeación Semanal"): st.session_state.p = "planeacion"
        if st.button("👤 Escrito Reflexivo"): st.session_state.p = "escrito"
        if st.button("📊 Evaluación Trimestral"): st.session_state.p = "evaluacion"
        st.divider()
        if st.button("🚪 Cerrar Sesión"): 
            st.session_state.step = "login"
            st.rerun()

    # --- CONTENIDO DINÁMICO ---
    if st.session_state.p == "home":
        st.subheader("Panel de Control")
        st.info("Selecciona una opción del menú lateral para comenzar a trabajar.")

    elif st.session_state.p == "planeacion":
        st.header("📝 Planeación Semanal")
        with st.form("form_plan"):
            ec = st.text_input("Nombre del EC")
            comunidad = st.text_input("Comunidad")
            nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
            obs = st.text_area("Observaciones de la semana")
            if st.form_submit_button("Generar PDF"):
                pdf = PlaneacionPDF()
                pdf.add_page()
                pdf.tabla_datos(ec, "ECA Ejemplo", comunidad, "2024", nivel, "1")
                pdf.seccion_dia("LUNES")
                pdf.multi_cell(0, 5, clean(obs))
                st.download_button("Descargar Planeación", data=pdf.output(dest='S'), file_name="planeacion.pdf")

    elif st.session_state.p == "escrito":
        st.header("👤 Escrito Reflexivo")
        # Aquí va la lógica de la fase 0.4
        st.write("Formulario para el seguimiento del alumno...")

    elif st.session_state.p == "evaluacion":
        st.header("📊 Evaluación Trimestral")
        # Aquí va la lógica de la fase 0.6/0.7
        st.write("Registro de notas y desempeño...")
