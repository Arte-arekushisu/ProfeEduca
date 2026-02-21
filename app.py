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
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'PLANEACION PEDAGOGICA INTEGRAL', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(240, 240, 240)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION PRO", layout="wide")
st.title("🛡️ Generador de Planeación con Contenido Real e Instrucciones")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "1")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "Proyecto Raices")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interes", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincon", "LECTURA/CIENCIAS")

    st.subheader("🗓️ Configuración de Materias Post-Receso")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=100)

    submit = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA")

if submit:
    with st.spinner("⏳ La IA está redactando las instrucciones y ejemplos detallados..."):
        time.sleep(2)
        
        # --- LÓGICA DE CONTENIDO DINÁMICO SEGÚN NIVEL ---
        if nivel == "Preescolar":
            # Momentos Iniciales
            pase_lista = f"Actividad: 'El tren de la asistencia'. Cada niño coloca su foto en el vagón mientras menciona un color relacionado con {tema}."
            bienvenida = "Dinamica: 'El baile de los animales'. Imitar movimientos lentos y rápidos de especies marinas."
            # Estación Mural
            est_mural_proc = f"1. Recolectar tapas de botellas. 2. Dibujar la silueta de una tortuga en cartulina. 3. Pegar las tapas como si fuera el caparazon. 4. Contar cuántas tapas usaron (Saberes)."
            est_mural_ej = "Ejemplo: Una tortuga verde con caparazon de taparroscas rojas."
            # Post Receso Matemáticas
            mats_det = f"Actividad: 'Conteo de nidos'. \nInstrucciones: Dibujar 5 círculos (nidos). Poner dentro de cada uno el número de 'huevos' (bolitas de papel) que indique el maestro. \nEjemplo: Nido A = 3 huevos."
            tarea = f"Con ayuda de papas, buscar en un recorte de revista algo que se parezca a una tortuga y pegarlo."
            
        elif nivel == "Primaria":
            pase_lista = f"Mencionar una parte del cuerpo de la tortuga al escuchar su nombre."
            bienvenida = "Dinamica: 'Telaraña marina'. Lanzar estambre compartiendo un dato que sepan del tema."
            # Estación Mural
            est_mural_proc = f"1. Investigar en fichas qué comen {tema}. 2. Dibujar el plato del buen comer adaptado a la tortuga. 3. Clasificar alimentos en el dibujo. 4. Redactar una frase sobre por qué es importante su dieta."
            est_mural_ej = "Ejemplo: Dibujo dividido en 3: algas, crustaceos y medusas, con cantidades escritas."
            # Post Receso Matemáticas
            mats_det = f"Tema: Suma de fracciones. \nInstrucciones: 1. Representar una tortuga dividida en 4 partes. 2. Colorear 1/4 de un color y 2/4 de otro. 3. Sumar las fracciones para ver cuánto del cuerpo está pintado. \nEjemplo: 1/4 + 2/4 = 3/4."
            tarea = f"Investigar cuántos huevos pone una tortuga y representarlo con una gráfica de barras simple."
            
        else: # Secundaria
            pase_lista = f"Plantear una pregunta de investigacion sobre {tema}."
            bienvenida = "Debate express: ¿Turismo o preservación en {comunidad}?"
            # Estación Mural
            est_mural_proc = f"1. Analizar el impacto del plastico en el ecosistema. 2. Diseñar un prototipo de nido artificial con malla reciclada. 3. Medir el area del nido (Matematicas). 4. Escribir un manifiesto de proteccion."
            est_mural_ej = "Ejemplo: Maqueta con escala 1:10 detallando materiales y costos de producción."
            # Post Receso Matemáticas
            mats_det = f"Tema: Probabilidad y estadística. \nInstrucciones: Analizar la tasa de supervivencia de las tortugas (1 de cada 1000). Calcular cuántas llegan al mar si nacen 5000. \nEjemplo: Regla de tres simple."
            tarea = f"Redactar un ensayo de una cuartilla sobre la interconexión de los campos formativos en la preservación ambiental."

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # Seccion I: Datos
        pdf.barra("I. DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        datos = [["Educador", educador], ["Nivel", nivel], ["Comunidad", comunidad], ["Tema", tema], ["Rincon", rincon]]
        for d in datos:
            pdf.cell(40, 7, clean(d[0]), 0); pdf.cell(0, 7, clean(d[1]), 0, 1)

        # Seccion II: Rutinas
        pdf.ln(5); pdf.barra("II. MOMENTOS INICIALES")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, "Pase de Lista:", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(pase_lista))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, "Bienvenida:", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        # Seccion III: Trabajo Autónomo con INDICACIONES
        pdf.add_page(); pdf.barra("III. ESTACIONES DE TRABAJO (INSTRUCCIONES Y PASOS)")
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean("Estacion: Mural / Laboratorio Integrado"), 0, 1)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, "Indicaciones para el Alumno:", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(est_mural_proc))
        pdf.set_font('Helvetica', 'I', 10); pdf.cell(0, 6, clean(f"Ejemplo: {est_mural_ej}"), 0, 1)

        # Seccion IV: Post-Receso Detallado
        pdf.add_page(); pdf.barra("IV. BLOQUE POST-RECESO (CONTENIDO TECNICO)")
        for dia, texto in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 10, clean(f"DIA: {dia}"), 1, 1, 'C', True)
            mats = texto.split('\n')
            
            # Hora 1: Matemáticas u otra
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"HORA 1: {mats[0]}"), "LTR", 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean(mats_det), "LR")
            
            # Hora 2: Artes / Fisica
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"HORA 2: {mats[1] if len(mats)>1 else 'Actividad 2'}"), "LTR", 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean("Realizar la actividad practica siguiendo el ejemplo visual. Cierre: Compartir resultados."), "LBR")
            pdf.ln(4)

        # Seccion V: Tarea
        pdf.ln(5); pdf.barra("V. TAREA / TRABAJO EN CASA")
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, clean(tarea))

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        # --- VISUALIZACION COMPLETA EN PANTALLA ---
        st.divider()
        st.subheader("👁️ Visualización de la Planeación Completa")
        
        tab1, tab2, tab3 = st.tabs(["Inicio y Estaciones", "Post-Receso", "Tarea"])
        with tab1:
            st.markdown(f"### I. Identificación\n**Educador:** {educador} | **Tema:** {tema}")
            st.markdown(f"### II. Momentos Iniciales\n**Pase de Lista:** {pase_lista}\n\n**Bienvenida:** {bienvenida}")
            st.info(f"### III. Estación de Trabajo\n**Instrucciones:**\n{est_mural_proc}\n\n**Ejemplo:** {est_mural_ej}")
        with tab2:
            st.markdown(f"### IV. Detalle de Clases Post-Receso")
            st.write(mats_det)
        with tab3:
            st.warning(f"### V. Tarea Sugerida\n{tarea}")

        st.download_button(
            label="📥 DESCARGAR PLANEACION COMPLETA (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_{nivel}_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
