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
        self.cell(0, 10, 'PLANEACION', 0, 1, 'C') # Título simplificado
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="GENERADOR DE PLANEACION", layout="wide")
st.title("🛡️ Generador de Planeación Profesional")

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

    st.subheader("🗓️ Distribución Post-Receso")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO FINAL")

if submit:
    with st.spinner("⏳ Consolidando planeación extensa..."):
        time.sleep(1)
        
        # --- RUTINAS INTEGRADAS ---
        if nivel == "Preescolar":
            regalo_lectura = f"Lectura: 'La aventura de {tema}'. El docente leera pausadamente usando onomatopeyas."
            bienvenida = "Bienvenida: Dinamica 'El caparazon gigante'. Uso de manta para simbolizar proteccion."
        elif nivel == "Primaria":
            regalo_lectura = f"Lectura: 'Leyenda de {tema}'. Lectura compartida analizando la perseverancia."
            bienvenida = "Bienvenida: Dinamica 'Red de Conocimientos'. Conexion de saberes previos con estambre."
        else:
            regalo_lectura = f"Lectura: 'Impacto ambiental de {tema}'. Analisis cientifico y postura critica."
            bienvenida = "Bienvenida: Actividad 'Debate Express' sobre dilemas eticos del entorno."

        # --- MARCO TEÓRICO UNIFICADO Y EXTENSO ---
        # Se usa una sola variable clara para evitar fragmentación
        marco_teorico = f"El estudio profundo de {tema} en la comunidad de {comunidad} es fundamental para el desarrollo del pensamiento critico. Estas especies no solo son parte del ecosistema, sino que representan un pilar de la biodiversidad local. Anatomia y Biologia: Se analizara su estructura osea, metodos de orientacion y ciclos migratorios. Problematicas: Se abordara la contaminacion por plasticos y el cambio climatico de manera detallada. Este proyecto integra los campos de Saberes y Pensamiento Cientifico, Lenguajes y Etica, Naturaleza y Sociedades, garantizando un aprendizaje integral y situado en la realidad de los alumnos."

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # Seccion I: Datos
        pdf.barra("I. DATOS GENERALES")
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Grado: {grado}"), 0, 1)
        pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | ECA: {eca} | Fecha: {fecha} | Rincon: {rincon}"), 0, 1)

        # Seccion II: Marco Teórico (Extenso y continuo)
        pdf.ln(5); pdf.barra("II. SUSTENTO TEORICO Y TEMA DE INTERES")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, clean(marco_teorico))

        # Seccion III: Rutinas de Inicio
        pdf.ln(5); pdf.barra("III. RUTINAS DE INICIO Y LENGUAJES")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Regalo de Lectura:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(regalo_lectura))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Actividad de Bienvenida:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        # Seccion IV: Estaciones
        pdf.add_page(); pdf.barra("IV. DESARROLLO: ESTACIONES DE AUTONOMIA")
        estaciones = [
            ("LENGUAJES", f"Bitacora de {tema}: Investigacion de datos curisos y redaccion de cronicas viajeras."),
            ("SABERES Y P.C.", f"Laboratorio: Simulacion de nidos, calculo de supervivencia y graficas de datos."),
            ("ETICA, NAT. Y SOC.", f"Cartografia: Mapeo de riesgos en la comunidad y propuestas de proteccion.")
        ]
        for tit, proc in estaciones:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"CAMPO: {tit}"), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(proc))
            pdf.ln(4)

        # Seccion V: Post-Receso
        pdf.add_page(); pdf.barra("V. ACTIVIDADES POST-RECESO")
        for dia, m_text in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"JORNADA: {dia}"), 1, 1, 'C', True)
            mats = m_text.split('\n')
            for m in mats:
                if m.strip():
                    pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean(f"Materia: {m}"), "LR", 1)
                    pdf.set_font('Helvetica', '', 9)
                    pdf.multi_cell(0, 5, clean(f"Secuencia: Inicio con saberes de {tema}, desarrollo practico y cierre de evaluacion."), "LBR")
            pdf.ln(3)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        st.divider()
        st.success("✅ ¡Planeación consolidada con éxito!")
        st.download_button(
            label="📥 DESCARGAR PLANEACION (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
