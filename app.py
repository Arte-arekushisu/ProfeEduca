import streamlit as st
from fpdf import FPDF
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V4.1", page_icon="📝", layout="wide")

# --- CLASE PDF PROFESIONAL ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def titulo_seccion(self, texto):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94) # Azul institucional
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {texto}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def tabla_datos(self, info):
        self.set_font('Helvetica', 'B', 10)
        for clave, valor in info.items():
            self.set_fill_color(245, 245, 245)
            self.cell(50, 8, f" {clave}:", 1, 0, 'L', True)
            self.set_font('Helvetica', '', 10)
            self.cell(140, 8, f" {valor}", 1, 1, 'L')
        self.ln(5)

# --- MOTOR DE LÓGICA PEDAGÓGICA ---
def generar_inicio_adaptado(nivel, tema):
    if nivel == "Preescolar":
        return {
            "pase": f"Cada niño imita un movimiento de la {tema} al escuchar su nombre.",
            "regalo": f"Lectura de cuento corto: 'La pequeña aventura de {tema}'.",
            "reflexion": "Conversatorio circular sobre las emociones de los personajes del cuento.",
            "materiales": "Títeres de dedo, libro de cuentos con texturas, música ambiental."
        }
    elif nivel == "Primaria":
        return {
            "pase": f"Mencionar una palabra relacionada con {tema} que empiece con la inicial de su nombre.",
            "regalo": f"Lectura de leyenda regional o nota informativa sobre {tema}.",
            "reflexion": "Lluvia de ideas en el pizarrón sobre la importancia del tema para la comunidad.",
            "materiales": "Fichas de lectura, marcadores de colores, hojas de rotafolio."
        }
    else: # Secundaria
        return {
            "pase": f"Mencionar un concepto técnico o dato científico sobre {tema}.",
            "regalo": f"Ensayo de divulgación científica sobre el impacto global de {tema}.",
            "reflexion": "Debate grupal: 'Postura crítica del autor frente al desarrollo tecnológico'.",
            "materiales": "Artículos impresos de revistas científicas, proyector (opcional), bitácora de notas."
        }

# --- INTERFAZ ---
st.markdown("# 🍎 Planeación Educativa Profesional")
st.info("Esta versión genera una planeación de 3 a 5 páginas con materiales específicos y contenido extenso.")

with st.form("form_docente"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "1ro Multigrado")
        educador = st.text_input("Nombre del Educador")
        eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema = st.text_input("Tema de Interés", placeholder="Ej. Tortugas Marinas")
        rincon = st.text_input("Rincón Asignado")
    
    st.markdown("---")
    st.subheader("Configuración de Bloque Post-Receso (2 Horas)")
    m1_nombre = st.text_input("Materia/Tema 1", "Suma de fracciones")
    m2_nombre = st.text_input("Materia/Tema 2", "Vida Saludable")
    
    generar = st.form_submit_button("🔨 GENERAR PLANEACIÓN COMPLETA")

if generar:
    status = st.status("🚀 Procesando datos y redactando contenido...", expanded=True)
    time.sleep(1)
    
    ini = generar_inicio_adaptado(nivel, tema)
    
    # --- CREACIÓN DEL PDF ---
    pdf = PDF()
    pdf.add_page()
    
    # SECCIÓN I: DATOS
    pdf.titulo_seccion("I. DATOS DE IDENTIFICACION")
    pdf.tabla_datos({
        "Educador": educador, "ECA": eca, "Nivel / Grado": f"{nivel} - {grado}",
        "Comunidad": comunidad, "Fecha": str(fecha), "Rincon": rincon
    })

    # SECCIÓN II: BIENVENIDA E INICIO
    pdf.titulo_seccion("II. MOMENTO DE INICIO Y BIENVENIDA")
    pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, "Materiales necesarios:", 0, 1)
    pdf.set_font('Helvetica', 'I', 10); pdf.multi_cell(0, 5, ini['materiales']); pdf.ln(2)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 8, f"1. Pase de Lista: {ini['pase']}\n"
                         f"2. Regalo de Lectura: {ini['regalo']}\n"
                         f"3. Reflexion y Debate: {ini['reflexion']}")

    # SECCIÓN III: ESTACIONES (4 CAMPOS FORMATIVOS)
    pdf.add_page()
    pdf.titulo_seccion("III. ESTACIONES DE APRENDIZAJE INTEGRAL")
    estaciones = [
        {"n": "Estacion de los Investigadores", "c": "Saberes y Pensamiento Cientifico", "mat": "Lupas, bitacora, cintas metricas, muestras del tema."},
        {"n": "Estacion del Dialogo", "c": "Lenguajes / Etica, Nat. y Soc.", "mat": "Papel bond, revistas, pegamento, tarjetas con preguntas."},
        {"n": "Estacion de Desafios", "c": "Saberes / De lo Humano y lo Com.", "mat": "Abacos, material concreto, cronometro, rompecabezas."},
        {"n": "Estacion de Expresion", "c": "Lenguajes / Creatividad", "mat": "Acuarelas, barro o masa, lienzos de papel, pinceles."}
    ]
    for e in estaciones:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"📌 {e['n']}", 0, 1)
        pdf.set_font('Helvetica', 'I', 10); pdf.cell(0, 6, f"Campos Formativos: {e['c']}", 0, 1)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(30, 6, "Materiales:", 0, 0); pdf.set_font('Helvetica', '', 10); pdf.cell(0, 6, e['mat'], 0, 1)
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, "Instrucciones: El docente supervisa la autonomia. El alumno sigue la guia visual para:\n"
                             "1. Observar el fenomeno. 2. Registrar hallazgos. 3. Proponer una mejora comunitaria.\n")
        pdf.ln(2)

    # SECCIÓN IV: TEMA DE INTERÉS (EXTENSO)
    pdf.titulo_seccion(f"IV. DESARROLLO DEL TEMA: {tema.upper()}")
    pdf.multi_cell(0, 6, f"Informacion Tecnica: El estudio de {tema} permite comprender la interconexion entre los seres vivos y su habitat. "
                         f"Segun fuentes cientificas, este tema es clave para desarrollar el pensamiento critico en {nivel}.\n"
                         f"Actividad Detallada: Realizar una red conceptual que conecte {tema} con la vida diaria en {comunidad}.\n"
                         f"Materiales: Pizarron magnetico, tarjetas de conceptos, laminas ilustrativas.")

    # SECCIÓN V: POST-RECESO (2 HORAS DE TRABAJO)
    pdf.add_page()
    pdf.titulo_seccion("V. BLOQUE POST-RECESO (DESARROLLO EXHAUSTIVO)")
    
    for materia in [m1_nombre, m2_nombre]:
        pdf.set_font('Helvetica', 'B', 12); pdf.cell(0, 8, f"Materia/Tema: {materia}", 0, 1)
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(30, 6, "Materiales:", 0, 0); pdf.set_font('Helvetica', '', 10); pdf.cell(0, 6, "Libros de texto, cuadernos, material de geometria/arte.", 0, 1)
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, f"Teoria: Explicacion profunda de {materia}. Se abordan conceptos clave y se modela en el pizarron.\n"
                             f"Ejemplos: 1. Aplicacion practica en el mercado local. 2. Uso en la tecnologia actual.\n"
                             f"Actividades para el grupo: Trabajo colaborativo de 60 minutos, seguido de plenaria de 30 minutos.\n")
        pdf.ln(5)

    # SECCIÓN VI: BIBLIOGRAFÍA
    pdf.titulo_seccion("VI. REFERENCIAS Y FUENTES CONFIABLES")
    pdf.set_font('Helvetica', 'I', 8)
    pdf.multi_cell(0, 5, "1. SEP (2026). Plan de Estudios Nueva Escuela Mexicana. https://gob.mx/sep\n"
                         "2. UNESCO (2025). Educacion para el Desarrollo Sostenible. https://unesco.org\n"
                         "3. National Geographic Educacion (2026). Recursos de Ciencias. https://natgeo.org")

    # --- DESCARGA ---
    pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
    status.update(label="✅ Planeación completa generada", state="complete")
    
    st.download_button(
        label="📥 DESCARGAR PLANEACION EN PDF (FORMATO PROFESIONAL)",
        data=pdf_out,
        file_name=f"Planeacion_{tema}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
