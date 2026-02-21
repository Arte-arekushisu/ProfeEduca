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
        # TÍTULO EXACTO SOLICITADO
        self.set_font('Helvetica', 'B', 25)
        self.set_text_color(30, 30, 30)
        self.cell(0, 20, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(40, 40, 40)):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(*color); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(2)

st.set_page_config(page_title="PLANEACION", layout="wide")
st.title("📑 Generador de Planeación Semanal Consolidada")

with st.form("Form_V17"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "1")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "reyes")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interes", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincon", "LECTURA/CIENCIAS")

    st.subheader("🗓️ Configuracion de Materias Post-Receso (Lunes a Viernes)")
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias[i]] = col.text_area(f"Materias {dias[i]}", "Matematicas\nEd. Fisica")

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO COMPLETO")

if submit:
    pdf = PlaneacionFinal()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # I. IDENTIFICACIÓN
    pdf.barra("I. DATOS GENERALES")
    pdf.set_font('Helvetica', '', 10)
    info = [["Educador", educador], ["Nivel/Grado", f"{nivel}/{grado}"], ["ECA", eca], ["Comunidad", comunidad], ["Tema", tema], ["Fecha", str(fecha)]]
    for row in info:
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(45, 8, f" {clean(row[0])}:", 1, 0, 'L', True)
        pdf.set_font('Helvetica', '', 10); pdf.cell(145, 8, f" {clean(row[1])}", 1, 1, 'L')
    pdf.ln(5)

    # II. INICIO DIARIO (TIEMPOS PEDAGÓGICOS)
    pdf.barra("II. MOMENTOS DE INICIO (25 MINUTOS)")
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, f"• PASE DE LISTA (5 min): Actividad vinculada a {tema}. Mat: Tarjetas recicladas.\n"
                         f"• REGALO DE LECTURA (10 min): Lectura en voz alta sobre biodiversidad. Mat: Libros del rincon.\n"
                         f"• BIENVENIDA (10 min): Dinamica de integracion y preguntas de saberes previos.")
    pdf.ln(5)

    # III. ESTACIONES DIDÁCTICAS (5 DÍAS / 4 CAMPOS / 3 ACT POR DÍA)
    pdf.barra("III. ESTACIONES DE TRABAJO (4 CAMPOS FORMATIVOS)")
    campos = [
        {"n": "Estacion de los Relatos (Lenguajes)", "m": "Revistas, pegamento, hojas, gises.", 
         "d": "L: Collage de palabras. M: Diario de observacion. Mi: Cartel de cuidado. J: Escritura de hipotesis. V: Exposición grupal."},
        {"n": "Laboratorio del Cientifico (Saberes)", "m": "Semillas, balanza, botes, arena.", 
         "d": "L: Conteo de nidos. M: Clasificacion por peso. Mi: Medidas de rastro. J: Registro de datos. V: Grafica de resultados."},
        {"n": "Guardianes de la Tierra (Etica/Nat)", "m": "Carton, gises, basura limpia.", 
         "d": "L: Mapa comunitario. M: Rastro de contaminacion. Mi: Maqueta de refugio. J: Firma de acuerdos. V: Mural de compromisos."},
        {"n": "Circulo de Saberes (De lo Humano)", "m": "Telas, material sobrante, espejos.", 
         "d": "L: Juego de roles. M: Tutoria entre pares. Mi: Dialogo emocional. J: Intercambio de saberes. V: Reflexion final."}
    ]
    
    for c in campos:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(c['n']), 0, 1)
        pdf.set_font('Helvetica', 'I', 9); pdf.cell(0, 6, f"Materiales sugeridos: {clean(c['m'])}", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, f"Secuencia Semanal (3 act. diarias): {clean(c['d'])}\n")
    
    # IV. POST-RECESO Y TAREAS
    pdf.add_page()
    pdf.barra("IV. BLOQUE POST-RECESO Y EXTENSION AL HOGAR")
    for dia, mat in mats_inputs.items():
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, f"{dia}:", 1, 1, 'L', True)
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, f"MATERIAS: {clean(mat)} (90 min total). Uso de materiales sobrantes.\n"
                             f"TAREA DIARIA: Investigar con familia un dato de {tema} y recolectar un material reciclable.")
        pdf.ln(2)

    # V. FIN DE SEMANA Y REFERENCIAS
    pdf.ln(5); pdf.barra("V. PROYECTO DE FIN DE SEMANA")
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, f"Mision: Realizar una entrevista a un adulto mayor de la comunidad sobre la historia de {tema} en la region. Entregar reporte creativo el lunes.")
    
    pdf.ln(5); pdf.barra("VI. REFERENCIAS (.EDU / .GOV)", (100, 100, 100))
    pdf.set_font('Helvetica', 'I', 8)
    pdf.multi_cell(0, 5, "SEP (2022). Plan de Estudios para la Educacion Basica. www.gob.mx/sep\nUNESCO (2024). Recursos Educativos para la Sostenibilidad. www.unesco.org")

    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PLANEACION FINAL CONSOLIDADA", data=pdf_bytes, file_name="Planeacion.pdf", use_container_width=True)
