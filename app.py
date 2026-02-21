import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import time

def clean(txt):
    if not txt: return ""
    # Eliminamos acentos y caracteres especiales para compatibilidad con FPDF (latin-1)
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

# Configuración de la aplicación
st.set_page_config(page_title="PLANEACION PRO", layout="wide")
st.title("🛡️ Generador de Planeación: Versión Final")

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

    st.subheader("🗓️ Distribución de Materias Post-Receso")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=100)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO FINAL")

if submit:
    with st.spinner("⏳ Consolidando información pedagógica..."):
        time.sleep(1.5)
        
        # --- LÓGICA DE REGALO DE LECTURA POR NIVEL ---
        if nivel == "Preescolar":
            regalo_lectura = "Lectura: 'La Pequeña Tortuga'. Instrucciones: Lectura en voz alta con énfasis en sonidos. Al finalizar, los alumnos imitan el movimiento de esconderse en su caparazón y describen texturas imaginarias."
            bienvenida = "Dinámica: 'El nido'. Los alumnos se sientan en círculo simulando un nido para compartir cómo se sienten hoy."
        elif nivel == "Primaria":
            regalo_lectura = "Lectura: 'El origen de los mares'. Instrucciones: Lectura compartida (un párrafo por alumno). Discusión sobre la importancia del agua y dibujo rápido de la escena favorita."
            bienvenida = "Dinámica: 'Corriente marina'. Juego de palabras encadenadas relacionadas con el tema de interés."
        else: # Secundaria
            regalo_lectura = "Lectura: 'Crisis Oceánica y Especies Migratorias'. Instrucciones: Análisis de texto informativo. Identificación de causas y consecuencias ambientales. Redacción de un breve comentario crítico."
            bienvenida = "Dinámica: 'Foro abierto'. Preguntas rápidas sobre el impacto de la comunidad en el ecosistema."

        # --- MARCO TEÓRICO EXTENSO ---
        marco_teorico = f"""El abordaje pedagógico sobre {tema} en la comunidad de {comunidad} permite desarrollar una conciencia crítica sobre la biodiversidad local. 
Desde la perspectiva científica, se analizan los ciclos de vida, las rutas migratorias y la anatomía especializada (caparazones, extremidades y sistemas de orientación). 
Impacto Comunitario: Se busca que el alumno identifique la interdependencia entre las actividades humanas locales y la preservación de estas especies. 
Vinculación Curricular: Este proyecto integra el pensamiento matemático (conteo y medición), lenguajes (producción de textos y bitácoras) y ética (responsabilidad ambiental)."""

        # --- GENERACION DEL PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # Sección I: Datos
        pdf.barra("I. DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        datos = [
            ["Educador:", educador], ["Nivel/Grado:", f"{nivel} / {grado}"],
            ["Comunidad:", comunidad], ["ECA:", eca],
            ["Rincon:", rincon], ["Fecha:", str(fecha)]
        ]
        for d in datos:
            pdf.cell(40, 7, clean(d[0]), 0)
            pdf.cell(0, 7, clean(d[1]), 0, 1)

        # Sección II: Marco Teórico
        pdf.ln(5); pdf.barra("II. MARCO TEORICO Y SUSTENTO PEDAGOGICO (EXTENSO)")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, clean(marco_teorico))

        # Sección III: Momentos Iniciales
        pdf.ln(5); pdf.barra("III. RUTINAS DE INICIO (TIEMPOS PEDAGOGICOS)")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean("Regalo de Lectura:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(regalo_lectura))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean("Bienvenida e Integracion:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        # Sección IV: Estaciones
        pdf.add_page(); pdf.barra("IV. ESTACIONES DE TRABAJO Y AUTONOMIA")
        campos = [
            ("LENGUAJES", "Creacion de cronicas y dibujos narrativos sobre el ecosistema. Uso de bitacora diaria."),
            ("SABERES Y P. CIENTIFICO", "Conteo, medicion de caparazones y simulacion de nidos. Analisis de datos."),
            ("ETICA, NATURALEZA Y SOC.", "Investigacion sobre leyes de proteccion y mapeo de zonas de riesgo en la comunidad.")
        ]
        for campo, desc in campos:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"Campo Formativo: {campo}"), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(f"Propuesta: {desc}"))
            pdf.ln(4)

        # Sección V: Post-Receso
        pdf.add_page(); pdf.barra("V. BLOQUE POST-RECESO (VINCULACION POR MATERIAS)")
        for dia, m_text in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 10, clean(f"DIA: {dia}"), 1, 1, 'C', True)
            materias = m_text.split('\n')
            for m in materias:
                if m.strip():
                    pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"Materia: {m}"), "LTR", 1)
                    pdf.set_font('Helvetica', '', 9)
                    pdf.multi_cell(0, 5, clean(f"Procedimiento: Inicio con recuperacion de saberes sobre {tema}. Desarrollo mediante actividad practica. Cierre con reflexion grupal."), "LBR")
                    pdf.ln(2)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        # --- VISUALIZACION EN PANTALLA ---
        st.divider()
        st.subheader("👁️ Visualización Previa")
        v1, v2 = st.columns(2)
        with v1:
            st.info("**Sustento Teórico:**")
            st.write(marco_teorico)
        with v2:
            st.success("**Actividades de Inicio:**")
            st.write(f"**Nivel:** {nivel}")
            st.write(regalo_lectura)

        st.download_button(
            label="📥 DESCARGAR PLANEACION COMPLETA (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_Final_{nivel}_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
