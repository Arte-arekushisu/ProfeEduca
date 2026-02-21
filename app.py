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
        self.cell(0, 10, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(230, 230, 230)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color)
        self.cell(0, 8, f"  {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION PRO", layout="wide")
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
        
        # --- LÓGICA DE RUTINAS POR NIVEL ---
        if nivel == "Preescolar":
            pase_lista = f"Actividad: 'Sonidos del mar'. Al escuchar su nombre, el niño imita un sonido relacionado con {tema}."
            regalo_lectura = f"Lectura: 'La pequeña aventura de {tema}'. Cuento corto con onomatopeyas."
            bienvenida = "Dinamica: 'El caparazon gigante'. Uso de una manta para simbolizar unidad."
        elif nivel == "Primaria":
            pase_lista = f"Actividad: 'Dato curioso'. Cada alumno menciona una palabra clave sobre {tema} al responder."
            regalo_lectura = f"Lectura: 'Leyendas y mitos sobre {tema}'. Analisis de la perseverancia."
            bienvenida = "Dinamica: 'Red de Conocimientos'. Conexion de saberes con estambre."
        else:
            pase_lista = f"Actividad: 'Hipotesis rapida'. El alumno plantea una duda de investigacion sobre {tema}."
            regalo_lectura = f"Lectura: 'Articulo Cientifico: El impacto de los plasticos'. Analisis critico."
            bienvenida = "Dinamica: 'Debate Express' sobre dilemas ambientales de la comunidad."

        # --- MARCO TEÓRICO UNIFICADO Y EXTENSO ---
        marco_teorico = f"El estudio de {tema} en la comunidad de {comunidad} es fundamental para entender el equilibrio ecologico. Estas especies son pilares de la biodiversidad. Anatomia: Se explorara la estructura osea, adaptaciones para el nado y sistemas de orientacion. Problematicas: Se profundizara en el impacto de los microplasticos y el cambio climatico en los nidos. Este proyecto integra Saberes, Lenguajes y Etica para un aprendizaje situado y critico."

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # I. DATOS GENERALES
        pdf.barra("I. DATOS GENERALES")
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Grado: {grado}"), 0, 1)
        pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | ECA: {eca} | Fecha: {fecha}"), 0, 1)

        # II. SUSTENTO TEORICO
        pdf.ln(5); pdf.barra("II. SUSTENTO TEORICO Y TEMA DE INTERES")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, clean(marco_teorico))

        # III. RUTINAS DE INICIO (PASE DE LISTA INCLUIDO)
        pdf.ln(5); pdf.barra("III. RUTINAS DE INICIO Y LENGUAJES")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Pase de Lista Pedagogico:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(pase_lista))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Regalo de Lectura:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(regalo_lectura))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean("Actividad de Bienvenida:"), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        # IV. ESTACIONES
        pdf.add_page(); pdf.barra("IV. DESARROLLO: ESTACIONES DE AUTONOMIA")
        estaciones = [
            ("LENGUAJES", f"Produccion: Escribir cronicas sobre {tema} y crear bitacoras de campo."),
            ("SABERES Y P.C.", f"Laboratorio: Calculo de supervivencia en nidos y graficas de crecimiento."),
            ("ETICA, NAT. Y SOC.", f"Cartografia: Mapeo de riesgos locales y propuestas de proteccion ambiental.")
        ]
        for tit, proc in estaciones:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"CAMPO: {tit}"), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(proc))
            pdf.ln(4)

        # V. POST-RECESO
        pdf.add_page(); pdf.barra("V. ACTIVIDADES POST-RECESO")
        for dia, m_text in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"JORNADA: {dia}"), 1, 1, 'C', True)
            mats = m_text.split('\n')
            for m in mats:
                if m.strip():
                    pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean(f"Materia: {m}"), "LR", 1)
                    pdf.set_font('Helvetica', '', 9)
                    pdf.multi_cell(0, 5, clean(f"Secuencia: Inicio (Saberes previos), Desarrollo (Actividad practica vinculada a {tema}) y Cierre."), "LBR")
            pdf.ln(3)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        st.divider()
        st.success("✅ Planeación generada con éxito.")
        st.download_button(
            label="📥 DESCARGAR PLANEACION (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
