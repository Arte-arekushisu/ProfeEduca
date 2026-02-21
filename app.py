import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE NORMALIZACIÓN (SEGURIDAD CONTRA ACCENTOS) ---
def clean(txt):
    if not txt: return ""
    # Convierte caracteres especiales para que FPDF no colapse
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

# --- CLASE PDF PROFESIONAL ---
class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(31, 52, 94)
        self.cell(0, 15, 'PLANEACION PEDAGOGICA INTEGRAL', 0, 1, 'C')
        self.ln(5)

    def seccion_barra(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Innovacion Educativa v0.4", layout="wide", page_icon="🍎")
st.title("🧩 Rompecabezas: Consolidacion de Fase 4")

with st.form("SaaS_Form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Tema de Interés", "TORTUGAS MARINAS")
        nombre_eca = st.text_input("Nombre del ECA", "reyes")
    with c2:
        grado = st.text_input("Grado", "1")
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha", datetime.date.today())
        rincon = st.text_input("Rincón asignado", "RICON DE LECTURA")

    st.markdown("---")
    st.subheader("Materia Post-Receso (Trabajo Profundo)")
    materia1 = st.text_input("Materia Post-Receso 1", "ETS")
    materia2 = st.text_input("Materia Post-Receso 2", "Suma de fracciones")
    
    boton = st.form_submit_button("🔨 GENERAR Y REVISAR PLANEACIÓN")

if boton:
    with st.status("🧠 Extrayendo información técnica y unificando fases...", expanded=True) as s:
        
        # --- MOTOR DE INTELIGENCIA (EXTENSIÓN DE CONTENIDO) ---
        # Aquí definimos la "Teoría de Biblioteca" para que el PDF sea extenso
        teoria_dic = {
            "Preescolar": "El enfoque se basa en la curiosidad natural. Se busca que el niño desarrolle nociones espaciales y de cuidado del entorno a través de la exploración táctil y visual del tema.",
            "Primaria": "Se implementa el Pensamiento Crítico. El alumno debe analizar cómo el tema afecta su entorno inmediato y proponer soluciones sencillas basadas en la observación científica.",
            "Secundaria": "Investigación epistemológica profunda. Se requiere que el estudiante conecte el tema con problemáticas globales (ODS) y realice una síntesis técnica usando fuentes bibliográficas diversas."
        }

        pdf = PlaneacionPDF()
        pdf.add_page()
        
        # I. DATOS DE IDENTIFICACIÓN (CORREGIDO)
        pdf.seccion_barra("I. DATOS DE IDENTIFICACION")
        # Estructura de tabla limpia para evitar el IndexError de tu captura
        datos_tabla = [
            ["Educador", educador], ["ECA", nombre_eca],
            ["Nivel/Grado", f"{nivel} / {grado}"], ["Comunidad", comunidad],
            ["Fecha", str(fecha)], ["Rincon", rincon]
        ]
        for fila in datos_tabla:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(50, 8, f" {clean(fila[0])}:", 1, 0, 'L', True)
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(140, 8, f" {clean(fila[1])}", 1, 1, 'L')
        pdf.ln(5)

        # II. BIENVENIDA (Fase 3 recuperada)
        pdf.seccion_barra("II. INICIO Y BIENVENIDA (PEDAGOGIA DEL AFECTO)")
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, f"Actividad: 'El eco de mi voz' centrada en {clean(tema)}. (15 min).\n"
                             "Regalo de lectura: Texto literario profundo acorde al nivel. Reflexion grupal sobre el impacto local.\n"
                             "Dinamica: Sincronizacion ritmica para crear cohesion grupal y enfoque en el aprendizaje.")
        pdf.ln(5)

        # III. ESTACIONES (Los 4 Campos Formativos - Fase 4)
        pdf.seccion_barra("III. ESTACIONES POR CAMPOS FORMATIVOS")
        campos = [
            ["Lenguajes", "Creacion de un 'Codigo Comunitario' sobre el tema. Materiales: Hojas, colores, periodicos."],
            ["Saberes y P.C.", f"Analisis de formas y medidas relacionados con {clean(tema)}. Materiales: Reglas, lupas."],
            ["Etica y Nat.", "Dialogo reflexivo sobre el impacto humano. Propuesta de 'Acuerdo de Convivencia'."],
            ["De lo Humano", "Juego de roles: 'El mercado del pueblo' aplicado al intercambio de saberes."]
        ]
        for c in campos:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, clean(c[0]), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"Instrucciones: {clean(c[1])}\n")
        
        # IV. TUTOREO (MOTOR DE INFORMACIÓN EXTENSA)
        pdf.add_page()
        pdf.seccion_barra(f"IV. TUTOREO Y
