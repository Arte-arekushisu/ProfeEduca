import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import time

def clean(txt):
    if not txt: return ""
    # Normalización para mantener tildes básicas en latin-1
    txt = txt.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    txt = txt.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionFinalPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 25)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def seccion_titulo(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f" {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION CONAFE", layout="wide")
st.title("🛡️ Sistema de Planeación Pedagógica Profesional")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "1")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "Proyecto Raices")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincón", "CIENCIAS / LECTURA")

    st.subheader("🗓️ Configuración de Materias Post-Receso (2 Horas)")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matemáticas\nArtes", height=100)

    submit = st.form_submit_button("🔨 GENERAR PLANEACION DETALLADA")

if submit:
    with st.spinner("⏳ Redactando procedimientos pedagógicos detallados..."):
        time.sleep(2)
        
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # --- I. IDENTIFICACIÓN ---
        pdf.seccion_titulo("I. DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        col_width = 95
        pdf.cell(col_width, 8, clean(f"Educador: {educador}"), 1)
        pdf.cell(col_width, 8, clean(f"Nivel/Grado: {nivel} - {grado}"), 1, 1)
        pdf.cell(col_width, 8, clean(f"ECA: {eca}"), 1)
        pdf.cell(col_width, 8, clean(f"Comunidad: {comunidad}"), 1, 1)
        pdf.cell(col_width, 8, clean(f"Tema: {tema}"), 1)
        pdf.cell(col_width, 8, clean(f"Rincon: {rincon}"), 1, 1)
        pdf.ln(5)

        # --- II. ESTACIONES CON PROCEDIMIENTO PASO A PASO ---
        pdf.seccion_titulo("II. ESTACIONES DE TRABAJO AUTONOMO")
        
        # Estación 1: Lenguajes
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean("Estacion: Mural Literario (Lenguajes)"), 0, 1)
        pdf.set_font('Helvetica', '', 10)
        proc_leng = (
            "1. Investigacion: Los alumnos buscan en el fichero 3 palabras clave del tema.\n"
            "2. Borrador: Escriben en su cuaderno el significado con sus propias palabras.\n"
            "3. Diseno: En una cartulina, dibujan el concepto central y pegan las definiciones.\n"
            "4. Exposicion: Se colocan en circulo para explicar su mural al resto del grupo."
        )
        pdf.multi_cell(0, 5, clean(proc_leng)); pdf.ln(3)

        # Estación 2: Saberes y P.C.
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean("Estacion: Laboratorio Cientifico (Saberes)"), 0, 1)
        proc_sab = (
            "1. Medicion: Usar una cinta metrica para medir objetos del rincon que simulen el tamaño de las tortugas.\n"
            "2. Registro: Anotar en la bitacora los pesos comparativos (usando una balanza casera).\n"
            "3. Analisis: Identificar cual objeto es mas pesado y por que, vinculandolo a la biomasa marina."
        )
        pdf.multi_cell(0, 5, clean(proc_sab)); pdf.ln(3)

        # --- III. BLOQUE POST-RECESO (DIVISION DETALLADA) ---
        pdf.add_page()
        pdf.seccion_titulo("III. BLOQUE POST-RECESO (DIVISION POR HORAS)")
        
        for dia, texto in mats_inputs.items():
            materias = texto.split('\n')
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(0, 10, clean(f"DIA: {dia}"), 1, 1, 'C', True)
            
            # HORA 1: MATEMÁTICAS DETALLE
            m1 = materias[0] if len(materias) > 0 else "Matemáticas"
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 8, clean(f"HORA 1: {m1}"), "LTR", 1)
            pdf.set_font('Helvetica', '', 9)
            if "MAT" in m1.upper():
                detalle_m1 = (
                    "PROCEDIMIENTO DE SUMA DE FRACCIONES:\n"
                    "- Inicio: Recordar el concepto de numerador y
