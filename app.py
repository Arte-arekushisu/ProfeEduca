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

st.set_page_config(page_title="PLANEACION PRO FINAL", layout="wide")
st.title("🛡️ Generador de Planeación Pedagógica (Versión Final)")

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

    st.subheader("🗓️ Materias Post-Receso")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO FINAL")

if submit:
    with st.spinner("⏳ Generando contenido pedagógico final..."):
        time.sleep(1)
        
        if nivel == "Preescolar":
            regalo_lectura = "Lectura: 'La Tortuga que no podia correr'. El docente leera pausadamente usando onomatopeyas."
            bienvenida = "Bienvenida: Actividad 'El caparazon gigante'. Uso de manta para simbolizar equipo."
        elif nivel == "Primaria":
            regalo_lectura = "Lectura: 'Leyenda Maya de la Tortuga y el Venado'. Lectura compartida sobre perseverancia."
            bienvenida = "Bienvenida: Dinamica 'Red de Conocimientos' con estambre."
        else:
            regalo_lectura = "Lectura: 'Informe Cientifico: Impacto de microplasticos'. Analisis y postura critica."
            bienvenida = "Bienvenida: Actividad 'Debate de Posturas' sobre economia vs conservacion."

        # MARCO TEÓRICO: Asegúrate de que las comillas triples cierren al final del párrafo.
        marco_teorico = f"""El estudio de {tema} en la comunidad de {comunidad} es vital para entender la biodiversidad local. 
Las tortugas marinas son reptiles ancestrales que cumplen la funcion de mantener la salud de los pastos marinos y arrecifes. 
Anatomia: Poseen un caparazon oseo unido a la columna vertebral, aletas adaptadas para el nado y un sistema de orientacion magnetica. 
Este proyecto integra campos de Saberes (biologia/fisica), Lenguajes (redaccion de informes) y Etica (preservacion ambiental)."""

        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        pdf.barra("I. DATOS GENERALES")
        pdf.set_font('Helvetica', '', 10)
        # LÍNEA SOLICITADA AGREGADA
        pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Grado: {grado}"), 0, 1)
        pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | ECA: {eca} | Fecha: {fecha}"), 0, 1)

        pdf.ln(5); pdf.barra("II. SUSTENTO TEORICO (TEMA DE INTERES)")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, clean(marco_teorico))

        pdf.ln(5); pdf.barra("III. RUTINAS DE INICIO Y LENGUAJES")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Regalo de Lectura:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(regalo_lectura))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Actividad de Bienvenida:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        pdf.add_page(); pdf.barra("IV. DESARROLLO: ESTACIONES DE AUTONOMIA")
        estaciones = [
            ("LENGUAJES", "Creacion de bitacora de campo: Investigar datos, redactar cronica e ilustrar."),
            ("SABERES Y P.C.", "Calculo de supervivencia: Simulacion de nido, conteo y grafica."),
            ("ETICA, NAT. Y SOC.", "Cartografia de nidos: Dibujar mapa, identificar riesgos y proteccion.")
        ]
        for tit, proc in estaciones:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"CAMPO: {tit}"), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(proc))
            pdf.ln(3)

        pdf.add_page(); pdf.barra("V. ACTIVIDADES POST-RECESO (TIEMPO COMPLEMENTARIO)")
        for dia, m_text in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"JORNADA: {dia}"), 1, 1, 'C', True)
            mats = m_text.split('\n')
            for m in mats:
                if m.strip():
                    pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean(f"Materia: {m}"), "LR", 1)
                    pdf.set_font('Helvetica', '', 9)
                    pdf.multi_cell(0, 5, clean(f"Secuencia: Inicio (Saberes), Desarrollo (Practica con {tema}) y Cierre (Evaluacion)."), "LBR")
            pdf.ln(3)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        st.divider()
        st.subheader("👁️ Vista Previa")
        st.write(marco_teorico)

        st.download_button(
            label="📥 DESCARGAR PLANEACION FINAL (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_Final_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
