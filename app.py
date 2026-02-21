import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

class PlaneacionFinal(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(31, 52, 94)
        self.cell(0, 15, 'PLANEACION PEDAGOGICA INTEGRAL', 0, 1, 'C')
        self.ln(5)

    def seccion(self, titulo, color=(31, 52, 94)):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(*color); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(2)

st.set_page_config(page_title="ProfeEduca v12 Master", layout="wide")
st.title("🛡️ Consolidación Total: Motor Pedagógico v12")

with st.form("Form_Maestro"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "Multigrado")
        educador = st.text_input("Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "Proyecto Raices")
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha", datetime.date.today())
    with c3:
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
        rincon = st.text_input("Rincón (Opcional)", "CIENCIAS")
    
    st.divider()
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        materia1 = st.text_input("Materia Post-Receso 1", "MATEMATICAS")
    with col_m2:
        materia2 = st.text_input("Materia Post-Receso 2 (ej. Ed. Fisica)", "EDUCACION FISICA")

    submit = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA")

if submit:
    pdf = PlaneacionFinal()
    pdf.add_page()

    # I. IDENTIFICACIÓN
    pdf.seccion("I. DATOS DE IDENTIFICACION")
    pdf.set_font('Helvetica', '', 10)
    tabla = [["Nivel/Grado", f"{nivel} - {grado}"], ["Educador", educador], ["ECA", eca], ["Comunidad", comunidad], ["Tema", tema], ["Rincon", rincon]]
    for item in tabla:
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(40, 7, f" {clean(item[0])}:", 1, 0, 'L')
        pdf.set_font('Helvetica', '', 10); pdf.cell(150, 7, f" {clean(item[1])}", 1, 1, 'L')
    pdf.ln(5)

    # II. BLOQUE DE INICIO (TIEMPOS PEDAGÓGICOS)
    pdf.seccion("II. MOMENTOS INICIALES (25 MIN)")
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, "1. Pase de Lista (5 min):", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"Actividad: Cada alumno menciona un animal que viva en el agua (Relacionado a {tema}).")
    
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, "2. Regalo de Lectura (10 min):", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, "Lectura: 'El viaje de la Tortuga'. Actividad: Dibujar en el aire el camino de la tortuga.")
    
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, "3. Bienvenida (10 min):", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, "Dinamica de integracion: 'La red marina'. Los alumnos se lanzan una estambre creando una red de conocimientos previos.")
    pdf.ln(5)

    # III. ESTACIONES SEMANALES (AUTONOMÍA)
    pdf.seccion("III. ESTACIONES DE TRABAJO AUTONOMO (45 MIN C/U)")
    estaciones = ["Lenguajes", "Saberes y P. Cientifico", "Etica, Nat. y Soc."]
    for est in estaciones:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, f"Campo: {clean(est)}", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, "Lunes-Martes: Identificacion de elementos (Material reciclado).\nMiercoles-Jueves: Registro en bitacora y experimentacion.\nViernes: Presentacion de hallazgos al grupo.\n")

    # IV. TUTOREO IA (DESARROLLO)
    pdf.add_page()
    pdf.seccion("IV. TUTOREO UNO A UNO (MOTOR IA)")
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, "Preguntas Detonantes:", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"1. ¿Como sabe una tortuga a que playa regresar?\n2. ¿Que pasaria si el plastico reemplaza la arena?\n3. ¿Cual es la funcion del caparazon en su vida diaria?")
    
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, "Actividades de Desarrollo:", 0, 1)
    pdf.multi_cell(0, 6, "1. Investigacion en ficheros academicos sobre reptiles marinos.\n2. Modelado de ecosistema con materiales de bajo costo.\n3. PRODUCTO FINAL: Infografia comunitaria sobre proteccion de nidos.")
    pdf.ln(5)

    # V. POST-RECESO
    pdf.seccion("V. MATERIAS POST-RECESO (90 MIN TOTAL)")
    for mat in [materia1, materia2]:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, f"Materia: {clean(mat)} (45 min)", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, "Inicio: Recuperacion de saberes.\nDesarrollo: Actividad practica con materiales sobrantes.\nCierre: Reflexion escrita o juego motor (si es Ed. Fisica).\n")

    # VI. REFERENCIAS
    pdf.ln(5); pdf.seccion("VI. REFERENCIAS Y FUENTES CONFIABLES", (100, 100, 100))
    pdf.set_font('Helvetica', 'I', 8)
    pdf.multi_cell(0, 5, "SEP (2022). Plan de Estudios para la educacion preescolar, primaria y secundaria. Recuperado de www.gob.mx/sep\nUNESCO (2021). Educacion para el Desarrollo Sostenible. www.unesco.org")

    pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PLANEACION INTEGRAL V12", data=pdf_out, file_name="Planeacion_Pedagogica_Integral.pdf", use_container_width=True)
