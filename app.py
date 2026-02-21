import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import time

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionFinalPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION PEDAGOGICA INTEGRAL', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 5, 'Organizacion por Tiempos Pedagogicos y Autonomia', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION PRO FINAL", layout="wide")
st.title("🛡️ Generador de Planeación Pedagógica (Versión Final)")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "Multigrado")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "Proyecto Raices")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interes", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincon", "CIENCIAS")

    st.subheader("🗓️ Materias Post-Receso")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO FINAL")

if submit:
    with st.spinner("⏳ Generando contenido pedagógico final..."):
        time.sleep(1)
        
        # --- LÓGICA DE RUTINAS INTEGRADAS ---
        if nivel == "Preescolar":
            regalo_lectura = "Lectura: 'La Tortuga que no podia correr'. El docente leera pausadamente usando onomatopeyas e invitando a los niños a imitar sonidos del mar."
            bienvenida = "Bienvenida: Actividad 'El caparazon gigante'. Usar una manta donde todos los niños entran para simbolizar proteccion y trabajo en equipo."
        elif nivel == "Primaria":
            regalo_lectura = "Lectura: 'Leyenda Maya de la Tortuga y el Venado'. Lectura compartida para discutir la moraleja sobre la perseverancia y la sabiduria."
            bienvenida = "Bienvenida: Dinamica 'Red de Conocimientos'. Conectar saberes previos sobre el ecosistema usando una madeja de estambre."
        else: # Secundaria
            regalo_lectura = "Lectura: 'Informe Cientifico: Impacto de microplasticos'. Analisis de terminos tecnicos y redaccion de postura critica sobre la responsabilidad humana."
            bienvenida = "Bienvenida: Actividad 'Debate de Posturas'. Confrontar ideas sobre desarrollo economico vs. conservacion ambiental."

        # --- MARCO TEÓRICO ---
        marco_teorico = f"""El estudio de {tema} en la comunidad de {comunidad} es vital para entender la biodiversidad local. 
Las tortugas marinas son reptiles ancestrales que cumplen la funcion de mantener la salud de los pastos marinos y arrecifes. 
Anatomia: Poseen un caparazon oseo unido a la columna vertebral, aletas adaptadas para el nado y un sistema de orientacion magnetica. 
Este proyecto integra campos de Saberes (biologia/fisica), Lenguajes (redaccion de informes) y Etica (preservacion ambiental)."""

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # Seccion I: Datos
        pdf.barra("I. DATOS GENERALES")
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, clean(f"Educador: {educador} |
