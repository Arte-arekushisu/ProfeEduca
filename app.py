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

st.set_page_config(page_title="PLANEACION PRO", layout="wide")
st.title("🛡️ Generador de Planeación Extensa y Tiempos Pedagógicos")

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

    st.subheader("⏰ Configuración de Horarios (Jornada Diaria)")
    h1, h2, h3, h4 = st.columns(4)
    h_entrada = h1.time_input("Hora de Entrada", datetime.time(8, 0))
    h_receso_in = h2.time_input("Inicio de Receso", datetime.time(10, 30))
    h_receso_fin = h3.time_input("Fin de Receso", datetime.time(11, 0))
    h_salida = h4.time_input("Hora de Salida", datetime.time(13, 0))

    st.subheader("🗓️ Materias Post-Receso")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=80)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO EXTENSO")

if submit:
    with st.spinner("⏳ Redactando sustento teórico y secuencias didácticas..."):
        time.sleep(2)
        
        # --- LÓGICA DE REGALO DE LECTURA EXTENDIDO POR NIVEL ---
        if nivel == "Preescolar":
            regalo_lectura = "Lectura: 'La Tortuga que no podia correr'. Instrucciones: El docente leera pausadamente usando onomatopeyas. Al finalizar, los niños imitaran el bostezo de la tortuga y describiran el color del caparazon usando comparaciones con objetos del salon."
            bienvenida = "Dinamica: 'El caparazon gigante'. Se usa una manta donde todos los niños entran, simbolizando proteccion y equipo."
        elif nivel == "Primaria":
            regalo_lectura = "Lectura: 'Leyenda Maya de la Tortuga y el Venado'. Instrucciones: Lectura compartida donde cada alumno lee un parrafo. Al terminar, realizar un esquema en el aire de los personajes y discutir la moraleja sobre la perseverancia frente a la velocidad."
            bienvenida = "Dinamica: 'Red de Conocimientos'. Usar un estambre para conectar saberes previos sobre el ecosistema local."
        else:
            regalo_lectura = "Lectura: 'Informe Cientifico: El impacto de los microplasticos'. Instrucciones: Lectura de analisis profundo. Los alumnos deberan subrayar terminos desconocidos y redactar una postura critica de 3 lineas sobre la responsabilidad humana en el ciclo de vida marino."
            bienvenida = "Dinamica: 'Debate de Posturas'. Confrontar ideas sobre economia (turismo) vs. conservacion ambiental."

        # --- MARCO TEÓRICO EXTENSO (Sustento para el Maestro) ---
        marco_teorico = f"""El estudio de {tema} en la comunidad de {comunidad} es vital para entender la biodiversidad local. 
Las tortugas marinas son reptiles ancestrales que cumplen la funcion de mantener la salud de los pastos marinos y arrecifes. 
Anatomia: Poseen un caparazon oseo unido a la columna vertebral, aletas adaptadas para el nado de largas distancias y un sistema de orientacion magnetica. 
Problemática Global: La contaminacion por plasticos, la pesca incidental y el cambio climatico que afecta la temperatura de los nidos (determinando el sexo de las crias). 
Este proyecto integra campos de Saberes (biologia/fisica), Lenguajes (redaccion de informes) y Etica (preservacion)."""

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # Seccion I: Datos y Horarios
        pdf.barra("I. DATOS GENERALES Y TIEMPOS")
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, clean(f"Educador: {educador} | Nivel: {nivel} | Grado: {grado}"), 0, 1)
        pdf.cell(0, 7, clean(f"Comunidad: {comunidad} | ECA: {eca} | Fecha: {fecha}"), 0, 1)
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 7, clean(f"HORARIO: Entrada {h_entrada} | Receso {h_receso_in}-{h_receso_fin} | Salida {h_salida}"), 1, 1, 'C')

        # Seccion II: Marco Teórico Extenso
        pdf.ln(5); pdf.barra("II. SUSTENTO TEORICO DEL TEMA DE INTERES (EXTENSO)")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, clean(marco_teorico))

        # Seccion III: Momentos Iniciales
        pdf.ln(5); pdf.barra("III. RUTINAS DE INICIO Y LENGUAJES")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, "Regalo de Lectura:", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(regalo_lectura))
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, "Bienvenida y Vinculacion:", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(bienvenida))

        # Seccion IV: Estaciones (Organización Pedagógica)
        pdf.add_page(); pdf.barra("IV. DESARROLLO: ESTACIONES DE AUTONOMIA (ESTILO TUTORIA)")
        estaciones = [
            ("LENGUAJES", "Creacion de bitacora de campo. Pasos: 1. Investigar 3 datos curiosos. 2. Redactar una cronica del viaje de la tortuga. 3. Ilustrar con materiales naturales."),
            ("SABERES Y P.C.", "Calculo de supervivencia. Pasos: 1. Simulacion de nido con canicas. 2. Conteo y resta de depredadores. 3. Grafica de resultados finales."),
            ("ETICA, NAT. Y SOC.", "Cartografia de nidos. Pasos: 1. Dibujar mapa de la comunidad. 2. Identificar zonas de riesgo. 3. Propuesta de proteccion escrita.")
        ]
        for tit, proc in estaciones:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"CAMPO: {tit}"), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(proc))
            pdf.ln(3)

        # Seccion V: Post-Receso por Día
        pdf.add_page(); pdf.barra("V. ACTIVIDADES POST-RECESO (TIEMPO COMPLEMENTARIO)")
        for dia, m_text in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"JORNADA: {dia}"), 1, 1, 'C', True)
            mats = m_text.split('\n')
            for m in mats:
                pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 6, clean(f"Materia/Area: {m}"), "LR", 1)
                pdf.set_font('Helvetica', '', 9)
                pdf.multi_cell(0, 5, clean(f"Secuencia: Inicio (Recuperacion), Desarrollo (Practica con {tema}) y Cierre (Evaluacion de producto)."), "LBR")
            pdf.ln(3)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')

        # --- VISUALIZACION ---
        st.divider()
        st.subheader("👁️ Vista Previa del Documento Extenso")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.info("**Sustento Teórico para el Maestro**")
            st.write(marco_teorico)
        with col_v2:
            st.success("**Momentos Iniciales (Adaptados)**")
            st.write(f"**Regalo de Lectura:** {regalo_lectura}")
            st.write(f"**Horario de Receso:** {h_receso_in} a {h_receso_fin}")

        st.download_button(
            label="📥 DESCARGAR PLANEACION COMPLETA (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_Pro_{nivel}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
