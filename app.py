import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'MOTOR PEDAGOGICO PROFEEDUCA - FASE 4', 0, 1, 'C')
        self.ln(5)

    def seccion_barra(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(3)

st.set_page_config(page_title="ProfeEduca v0.4 - Consolidado", layout="wide")
st.title("🛡️ Finalización de Fase 4: Autonomía y Profundidad")

with st.form("SaaS_Final_F4"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Educador", "AXEL REYES")
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        rincon = st.text_input("Rincón Asignado", "LECTURA")
        materia_post = st.text_input("Materia Post-Receso", "FRACCIONES")
    
    boton = st.form_submit_button("🔨 GENERAR PLANEACION EXTENSA")

if boton:
    # --- MOTOR DE GENERACIÓN DE ACTIVIDADES AUTÓNOMAS ---
    # Aquí definimos el contenido largo que pediste
    estaciones_detalladas = [
        {
            "campo": "Lenguajes",
            "titulo": "El Diario del Explorador",
            "materiales": "Hojas de colores, pegamento, revistas, tijeras y plumones.",
            "pasos": "1. Busca imagenes relacionadas al tema en las revistas.\n2. Crea un collage que cuente una historia sin usar palabras.\n3. Escribe un titulo creativo para tu historia y pegalo en el muro."
        },
        {
            "campo": "Saberes y P. Científico",
            "titulo": "Laboratorio de Medidas",
            "materiales": "Regla, cinta metrica, balanza escolar y objetos del rincon.",
            "pasos": "1. Elige 5 objetos y estima cuanto pesan.\n2. Usa la balanza para comprobar tu estimacion y anota los resultados.\n3. Dibuja el objeto mas pesado y el mas ligero explicando por que crees que es asi."
        },
        {
            "campo": "Ética, Naturaleza y Soc.",
            "titulo": "Guardianes del Entorno",
            "materiales": "Cartulina, gises y fotografias de la comunidad.",
            "pasos": "1. Observa las fotografias y detecta un problema ambiental.\n2. Diseña un cartel con una solucion que tu puedas hacer hoy mismo.\n3. Explica tu cartel a un compañero y busquen una firma de compromiso."
        }
    ]

    pdf = PlaneacionPDF()
    pdf.add_page()
    
    # I. IDENTIFICACIÓN
    pdf.seccion_barra("I. DATOS DE IDENTIFICACION")
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, f"Educador: {clean(educador)} | Nivel: {clean(nivel)}\nComunidad: {clean(comunidad)} | Tema: {clean(tema)}")
    pdf.ln(5)

    # II. ESTACIONES (TRABAJO AUTÓNOMO DETALLADO)
    pdf.seccion_barra("II. ESTACIONES DE TRABAJO AUTONOMO (MOMENTO CENTRAL)")
    for est in estaciones_detalladas:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, f"Estacion: {clean(est['titulo'])} ({clean(est['campo'])})", 0, 1)
        pdf.set_font('Helvetica', 'I', 10)
        pdf.multi_cell(0, 6, f"Materiales necesarios: {clean(est['materiales'])}")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, f"PASOS PARA EL ALUMNO:\n{clean(est['pasos'])}")
        pdf.ln(4)

    # III. MARCO TEÓRICO AMPLIADO (MOTOR DE INFORMACIÓN)
    pdf.add_page()
    pdf.seccion_barra(f"III. PROFUNDIZACION DEL TEMA: {clean(tema)}")
    pdf.set_font('Helvetica', '', 11)
    informacion_ia = (f"El tema de {clean(tema)} es fundamental para el desarrollo del pensamiento critico en {clean(nivel)}. "
                      "Desde una perspectiva cientifica, esto implica comprender los ciclos de vida y la interdependencia "
                      "dentro del ecosistema local. El docente debe actuar como facilitador, permitiendo que el alumno "
                      "descubra mediante la observacion y el registro en su RPA (Relacion Tutora).\n\n"
                      "DATOS TECNICOS PARA EL MAESTRO:\n"
                      "- Conectar el tema con la realidad de la comunidad.\n"
                      "- Fomentar la demostracion publica como cierre del aprendizaje.\n"
                      "- Utilizar el error como una oportunidad de aprendizaje guiado.")
    pdf.multi_cell(0, 7, clean(informacion_ia))

    # --- CIERRE ---
    pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PLANEACION EXTENSA", data=pdf_out, file_name=f"Fase4_Final.pdf", use_container_width=True)
