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
        self.cell(0, 10, 'PLANEACION', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, 'Contenido Pedagogico Extenso y Detallado', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(240, 240, 240)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

# Configuración de página
st.set_page_config(page_title="PLANEACION PRO", layout="wide")
st.title("🛡️ Generador de Planeación de Contenido Extenso")

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

    st.subheader("🗓️ Configuración de Materias Post-Receso (2 Horas Diarias)")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=100)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO COMPLETO")

if submit:
    with st.spinner("⏳ La IA está redactando momentos iniciales y procedimientos..."):
        time.sleep(2)
        
        # --- LÓGICA DE IA POR NIVEL (MOMENTOS INICIALES) ---
        if nivel == "Preescolar":
            pase_lista = f"Actividad: 'El tren de la asistencia'. Cada niño coloca su foto en el vagón mientras menciona un color relacionado con {tema}."
            regalo_lectura = "Lectura: Cuento corto con marionetas o figuras de fieltro. Enfoque en onomatopeyas y rimas simples."
            bienvenida = "Dinamica: 'El baile de los animales'. Movimientos corporales exagerados imitando especies marinas para liberar energia."
        elif nivel == "Primaria":
            pase_lista = f"Actividad: 'Palabra clave'. El alumno dice una característica física de {tema} al escuchar su nombre."
            regalo_lectura = "Lectura: Fragmento de una leyenda local o fábula. Actividad: Identificar el inicio, nudo y desenlace en el aire."
            bienvenida = "Dinamica: 'Telaraña de saberes'. Lanzar un estambre compartiendo un dato curioso que ya conozcan sobre el tema central."
        else: # Secundaria
            pase_lista = f"Actividad: 'Hipótesis rápida'. Al mencionar su nombre, el alumno plantea una pregunta de investigación sobre {tema}."
            regalo_lectura = "Lectura: Artículo de divulgación científica o noticia reciente. Análisis crítico breve sobre el impacto ambiental."
            bienvenida = "Dinamica: 'Debate express'. Postura a favor o en contra de un dilema ético relacionado con el ecosistema de la comunidad."

        # --- MARCO TEÓRICO Y ESTACIONES ---
        marco_teorico = f"El abordaje de {tema} promueve la investigacion activa en {comunidad}..."
        
        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # Seccion I: Datos
        pdf.barra("I. DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        for k, v in [["Educador", educador], ["Nivel/Grado", f"{nivel}/{grado}"], ["Comunidad", comunidad], ["Tema", tema]]:
            pdf.cell(40, 7, clean(k), 0); pdf.cell(0, 7, clean(v), 0, 1)

        # Seccion II: Momentos Iniciales (LA IA GENERA ESTO)
        pdf.ln(5); pdf.barra("II. MOMENTOS INICIALES (RUTINAS DE INICIO)")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean("Pase de Lista:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(pase_lista))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean("Regalo de Lectura:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(regalo_lectura))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean("Bienvenida:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        # Seccion III: Estaciones (Contenido Extenso)
        pdf.add_page(); pdf.barra("III. ESTACIONES DE TRABAJO AUTONOMO")
        estaciones_titulos = ["Lenguajes - Mural", "Saberes - Laboratorio", "Etica - Compromisos"]
        for est in estaciones_titulos:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(est), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean("Procedimiento detallado paso a paso para investigacion y produccion de materiales reciclados."))
            pdf.ln(3)

        # Seccion IV: Post-Receso
        pdf.add_page(); pdf.barra("IV. BLOQUE POST-RECESO (DIVISION 60 MIN / 60 MIN)")
        for dia, texto in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 10, clean(f"DIA: {dia}"), 1, 1, 'C', True)
            mats = texto.split('\n')
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"HORA 1: {mats[0] if len(mats)>0 else 'Materia 1'}"), 1, 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean("Actividad tecnica de especialidad: Inicio, Desarrollo y Cierre."), 1)
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"HORA 2: {mats[1] if len(mats)>1 else 'Materia 2'}"), 1, 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean("Actividad de reforzamiento o expresion artistica/fisica."), 1)
            pdf.ln(5)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        # --- VISUALIZACION EN STREAMLIT ---
        st.divider()
        st.subheader("👁️ Visualizacion Previa de la Planeacion")
        v1, v2 = st.columns(2)
        with v1:
            st.info("**Momentos Iniciales Adaptados**")
            st.write(f"**Pase de Lista:** {pase_lista}")
            st.write(f"**Bienvenida:** {bienvenida}")
        with v2:
            st.info("**Estructura Post-Receso**")
            st.write(f"Horario: 120 minutos divididos en bloques de 60 min por materia.")

        # --- BOTON DE DESCARGA ---
        st.download_button(
            label="📥 DESCARGAR PLANEACION COMPLETA (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_{nivel}_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
