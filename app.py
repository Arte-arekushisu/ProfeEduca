import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE SEGURIDAD PARA CARACTERES (Evita UnicodeEncodeError) ---
def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

class PlaneacionCompleta(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(31, 52, 94)
        self.cell(0, 10, 'SISTEMA INTEGRAL DE PLANEACION - PROFEEDUCA', 0, 1, 'C')
        self.ln(5)

    def barra_titulo(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="ProfeEduca v0.4 Final", layout="wide")
st.title("🍎 ProfeEduca: Consolidacion Total (Fase 4)")

with st.form("Form_Final_F4"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Proyecto de Interes", "LAS TORTUGAS MARINAS")
        nombre_eca = st.text_input("Nombre del ECA", "reyes")
    with c2:
        grado = st.text_input("Grado y Grupo", "1")
        comunidad = st.text_input("Comunidad", "CRUZ")
        rincon = st.text_input("Rincon Asignado", "RICON DE LECTURA")
        materia_post = st.text_input("Materia Post-Receso", "MATEMATICAS")

    boton = st.form_submit_button("🔨 GENERAR PLANEACION PROFESIONAL")

if boton:
    # --- RECUPERACIÓN DE LÓGICA DE VERSIONES ANTERIORES ---
    logica_niveles = {
        "Preescolar": {"pase": "Imitar un sonido de la naturaleza.", "regalo": "Cuento narrado con titeres."},
        "Primaria": {"pase": "Mencionar una palabra clave del tema.", "regalo": "Leyenda o mito regional."},
        "Secundaria": {"pase": "Cita de un autor relevante.", "regalo": "Articulo de divulgacion cientifica."}
    }
    info_v = logica_niveles[nivel]

    pdf = PlaneacionCompleta()
    pdf.add_page()

    # I. IDENTIFICACIÓN (Corregido para evitar IndexError)
    pdf.barra_titulo("I. DATOS DE IDENTIFICACION")
    datos_id = [
        ["Educador", educador], ["ECA", nombre_eca],
        ["Nivel/Grado", f"{nivel} / {grado}"], ["Comunidad", comunidad],
        ["Rincon", rincon], ["Fecha", str(datetime.date.today())]
    ]
    for d in datos_id:
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(50, 8, f" {clean(d[0])}:", 1, 0, 'L', True)
        pdf.set_font('Helvetica', '', 10); pdf.cell(140, 8, f" {clean(d[1])}", 1, 1, 'L')
    pdf.ln(5)

    # II. MOMENTO DE INICIO (Recuperado de V10/V11)
    pdf.barra_titulo("II. INICIO Y BIENVENIDA")
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, f"- Pase de Lista Dinamico: {clean(info_v['pase'])}\n"
                         f"- Regalo de Lectura: {clean(info_v['regalo'])}\n"
                         f"- Reflexion: Dialogo guiado sobre el tema central: {clean(tema)}.")
    pdf.ln(5)

    # III. ESTACIONES DE TRABAJO AUTONOMO (4 CAMPOS FORMATIVOS)
    pdf.barra_titulo("III. ESTACIONES AUTONOMAS POR CAMPOS")
    estaciones = [
        {"c": "Lenguajes", "n": "El Mural de las Palabras", "i": "1. Elige 3 palabras clave del tema.\n2. Diseña un cartel creativo.\n3. Comparte tu definicion con un compañero."},
        {"c": "Saberes y P.C.", "n": "Laboratorio de Formas", "i": "1. Mide los objetos del rincon.\n2. Registra los datos en tu bitacora.\n3. Compara resultados y encuentra patrones."},
        {"c": "Etica / Humano", "n": "Acuerdos Comunitarios", "i": "1. Identifica un problema ambiental.\n2. Escribe una accion para resolverlo.\n3. Firma tu compromiso en el mural."}
    ]
    for e in estaciones:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Campo: {clean(e['c'])} - {clean(e['n'])}", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"CONSIGNA:\n{clean(e['i'])}\n")
    
    # IV. SUSTENTO PEDAGÓGICO (Motor de Información)
    pdf.add_page()
    pdf.barra_titulo("IV. SUSTENTO PEDAGOGICO Y PROFUNDIZACION")
    teoria_extensa = (f"El estudio de {tema} en el nivel {nivel} permite desarrollar el pensamiento critico. "
                      "Cientificamente, se aborda como un fenomeno de interdependencia natural. "
                      "El alumno lidera su aprendizaje mediante la investigacion en el rincon asignado.")
    pdf.set_font('Helvetica', '', 11); pdf.multi_cell(0, 8, clean(teoria_extensa))

    # V. POST-RECESO
    pdf.ln(5); pdf.barra_titulo("V. BLOQUE POST-RECESO")
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Materia: {clean(materia_post)}", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 7, "1. Explicacion teorica.\n2. Practica individual de 10 ejercicios.\n3. Plenaria de cierre.")

    # --- GENERACIÓN FINAL ---
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PLANEACION COMPLETA", data=pdf_bytes, file_name="ProfeEduca_Fase4_Final.pdf", use_container_width=True)
