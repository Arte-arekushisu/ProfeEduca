import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- SEGURIDAD DE CARACTERES ---
def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

class PlaneacionSaaS(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(20, 40, 80)
        self.cell(0, 10, 'SISTEMA DE GESTION PEDAGOGICA - PROFEEDUCA', 0, 1, 'C')
        self.ln(5)

    def seccion_premium(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(3)

# --- INTERFAZ PROFESIONAL ---
st.set_page_config(page_title="ProfeEduca SaaS v0.4", layout="wide")
st.title("🚀 Consolidación de Fase 4: Motor de Información")

with st.form("SaaS_Pro_Form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Educador Responsable", "AXEL REYES")
        tema = st.text_input("Proyecto de Interés", "LAS TORTUGAS MARINAS")
    with c2:
        comunidad = st.text_input("Comunidad / Localidad", "CRUZ")
        rincon = st.text_input("Rincón de Trabajo", "CIENCIAS")
        materia_post = st.text_input("Bloque Post-Receso", "MATEMATICAS")

    boton = st.form_submit_button("🔨 GENERAR DOCUMENTACION TECNICA")

if boton:
    # --- MOTOR DE TEXTO EXTENSO (BIBLIOTECA) ---
    # Esto simula la búsqueda profunda que pediste
    info_pro = (f"Las {tema} representan un pilar en la biodiversidad de {comunidad}. "
                f"Para el nivel {nivel}, el abordaje pedagogico debe ser vivencial. "
                "Cientificamente, se estudian como reptiles marinos que han sobrevivido millones de años. "
                "Su ciclo de vida incluye la migracion, el desove en playas y el regreso al oceano. "
                "En esta planeacion, el alumno no solo lee; se convierte en un observador de fenomenos naturales.")

    pdf = PlaneacionSaaS()
    pdf.add_page()
    
    # I. IDENTIFICACIÓN PROFESIONAL
    pdf.seccion_premium("I. IDENTIFICACION DEL PROYECTO")
    pdf.set_font('Helvetica', 'B', 10)
    # Evitamos IndexError usando un diccionario estable
    datos = {"Maestro": educador, "Nivel": nivel, "Comunidad": comunidad, "Proyecto": tema}
    for k, v in datos.items():
        pdf.cell(40, 8, f" {clean(k)}:", 1, 0, 'L', True)
        pdf.cell(150, 8, f" {clean(v)}", 1, 1, 'L')
    pdf.ln(5)

    # II. ESTACIONES DE AUTONOMÍA (INSTRUCCIONES LARGAS)
    pdf.seccion_premium("II. GUIAS DE APRENDIZAJE AUTONOMO")
    estaciones = [
        {
            "n": "Estacion de Lenguajes: El Relato del Mar",
            "m": "Hojas de dibujo, acuarelas, pinceles, libros de consulta.",
            "i": "1. Investiga en los libros del rincon 3 datos asombrosos sobre el tema.\n2. Crea una secuencia de 4 dibujos que expliquen el ciclo de vida sin usar palabras.\n3. Al finalizar, escribe una carta a la comunidad explicando por que debemos cuidar este recurso."
        },
        {
            "n": "Estacion de Saberes: El Laboratorio del Cientifico",
            "m": "Cinta metrica, balanza, arena, figuras a escala.",
            "i": "1. Mide el largo y ancho de las figuras y anota los datos en tu tabla de registro.\n2. Compara los pesos y ordena los objetos de menor a mayor masa.\n3. Plantea una hipotesis: ¿Que pasaria si el clima de la playa cambia? Registra tu respuesta."
        }
    ]
    for e in estaciones:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(e['n']), 0, 1)
        pdf.set_font('Helvetica', 'I', 10); pdf.multi_cell(0, 6, f"Materiales: {clean(e['m'])}")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, f"CONSIGNA PARA EL ALUMNO:\n{clean(e['i'])}\n")
        pdf.ln(2)

    # III. MARCO TEÓRICO (FASE 4: MOTOR PEDAGÓGICO)
    pdf.add_page()
    pdf.seccion_premium("III. SUSTENTO TEORICO Y PEDAGOGICO (MARCO MAESTRO)")
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 8, clean(info_pro))
    
    # IV. POST-RECESO DETALLADO
    pdf.ln(5); pdf.seccion_premium("IV. BLOQUE POST-RECESO: TRABAJO TECNICO")
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Tema: {clean(materia_post)}", 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 7, "1. Explicacion en pizarron mediante el metodo de descubrimiento guiado.\n2. Practica individual: El alumno resuelve una serie de 10 ejercicios contextualizados.\n3. Cierre: El alumno explica a un compañero el procedimiento que utilizo.")

    # --- DESCARGA SEGURA ---
    pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PLANEACION COMPLETA F4", data=pdf_out, file_name="SaaS_ProfeEduca_F4.pdf", use_container_width=True)
