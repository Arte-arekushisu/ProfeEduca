import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="ProfeEduca V0.6", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .stButton>button {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(248, 250, 252, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(8px);
    }
    .stButton>button:hover { border-color: #38bdf8; color: #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CLASE PARA EL PDF (DISEÑO PROFESIONAL) ---
class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'GUÍA PEDAGÓGICA INTEGRAL - MODELO DE DIÁLOGO', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

def crear_guia_pdf(d):
    pdf = PlaneacionPDF()
    pdf.add_page()
    
    # I. TABLA DE IDENTIFICACIÓN (PRIMER PUNTO)
    pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
    pdf.set_font('Arial', 'B', 10)
    campos = [
        ["Nivel Educativo", d['nivel']], ["Grado", d['grado']],
        ["Educador", d['nombre_ed']], ["ECA", d['nombre_eca']],
        ["Comunidad", d['comunidad']], ["Fecha", d['fecha']],
        ["Tema de Interés", d['tema']], ["Rincón", d['rincon']]
    ]
    for row in campos:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(50, 8, row[0], 1, 0, 'L', True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 8, str(row[1]), 1, 1, 'L')
        pdf.set_font('Arial', 'B', 10)
    pdf.ln(5)

    # II. OBJETIVO GENERAL (SEGUNDO PUNTO)
    pdf.chapter_title("II. OBJETIVO GENERAL")
    pdf.set_font('Arial', '', 10)
    objetivo = (f"Lograr que los alumnos de {d['nivel']} se apropien del tema '{d['tema']}' mediante un "
                "proceso de diálogo, investigación y experimentación. El estudiante aprenderá a "
                "identificar problemas, proponer soluciones y comunicar sus hallazgos de forma clara, "
                "desarrollando una conciencia crítica sobre su entorno y fortaleciendo sus capacidades "
                "cognitivas y socioemocionales a través del trabajo colaborativo.")
    pdf.multi_cell(0, 5, objetivo)
    pdf.ln(5)

    # III. INICIO (MOMENTOS PEDAGÓGICOS)
    pdf.chapter_title("III. MOMENTOS DE INICIO (PARA CARTULINA)")
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "1. Pase de lista dinámico (5 min):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, f"Actividad 'La voz del tema': Al escuchar su nombre, el niño dice un ejemplo de {d['tema']} que haya visto en su camino al salón.")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "2. Regalo de lectura (10 min):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, f"Lectura en voz alta de un texto informativo o leyenda local sobre {d['tema']}. Actividad: Identificar en el mapa del salón dónde se ubicaría esta historia.")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "3. Actividad de bienvenida (10 min):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, f"Juego 'La red de saberes': Con un estambre, formamos una red mientras cada alumno comparte qué quiere descubrir hoy sobre {d['tema']}.")
    pdf.ln(5)

    # IV. ESTACIONES DE APRENDIZAJE
    pdf.chapter_title("IV. ESTACIONES DE TRABAJO (45 min c/u)")
    pdf.multi_cell(0, 6, f"Estación 1 (Lenguajes): Redactar un 'Aviso Comunitario' sobre {d['tema']} usando recortes de periódicos.\n\n"
                         f"Estación 2 (Saberes): Clasificar elementos de {d['tema']} recolectados en el rincón según su forma y utilidad.\n\n"
                         f"Estación 3 (Comunidad): Representación teatral breve de cómo {d['tema']} ayuda a los vecinos de la zona.")
    pdf.ln(5)

    # V. TUTOREO PROFUNDO
    pdf.chapter_title(f"V. TUTOREO UNO A UNO: {d['tema'].upper()}")
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, f"Desarrollo del Tema: Se explica que {d['tema']} es un pilar fundamental para entender nuestro entorno. Por ejemplo, si estudiamos los ciclos del agua o la tierra, vemos cómo impactan en nuestra comida diaria.")
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Actividades Sugeridas:", 0, 1); pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, "1. Investigación de campo: Entrevistar a una persona mayor sobre el tema.\n2. Registro en cuaderno de campo: Dibujar el proceso observado.")
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Producto Final:", 0, 1); pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, f"Creación de una 'Gaceta Escolar' o maqueta con materiales de desecho sobre {d['tema']}.")
    pdf.ln(5)

    # VI. POST-RECESO
    pdf.chapter_title("VI. ACTIVIDADES POST-RECESO (TIEMPOS PEDAGÓGICOS)")
    pdf.multi_cell(0, 6, f"Materia 1 ({d['materia1']}): Actividad práctica de reforzamiento. Ejemplo: Si es matemáticas, contar elementos de {d['tema']}.\n\n"
                         f"Materia 2 ({d['materia2']}): Sesión integradora. Ejemplo: Educación Física con juegos que simulen el movimiento de {d['tema']}.")
    
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, "Referencias: SEP (2022) Plan de Estudios; UNESCO (2021) Reimaginar el futuro.", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- 3. INTERFAZ DE USUARIO (SOLUCIÓN A NAMEERROR) ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"

# Columnas definidas ANTES de usarlas
col_menu, col_main = st.columns([1, 2.5])

with col_menu:
    st.title("🍎 Menú")
    if st.button("🏠 Inicio", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"

with col_main:
    if st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        
        # Formulario limpio
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
                grado = st.text_input("Grado")
                nombre_ed = st.text_input("Nombre del Educador")
                nombre_eca = st.text_input("Nombre del ECA")
            with c2:
                comunidad = st.text_input("Comunidad")
                fecha = st.date_input("Fecha")
                tema = st.text_input("Tema de interés")
                rincon = st.text_input("Rincón (opcional)")
            
            st.subheader("Post-Receso")
            m1 = st.text_input("Materia 1", value="Educación Física")
            m2 = st.text_input("Materia 2", value="Artística")

        if st.button("🚀 GENERAR PLANEACIÓN COMPLETA", use_container_width=True):
            if not tema or not nombre_ed:
                st.error("Por favor completa los campos de Nombre y Tema.")
            else:
                with st.spinner("Redactando guía pedagógica..."):
                    # Recolectamos datos de los inputs definidos arriba
                    datos = {
                        "nivel": nivel, "grado": grado, "nombre_ed": nombre_ed,
                        "nombre_eca": nombre_eca, "comunidad": comunidad,
                        "fecha": str(fecha), "tema": tema, "rincon": rincon,
                        "materia1": m1, "materia2": m2
                    }
                    archivo_pdf = crear_guia_pdf(datos)
                    st.download_button(
                        label="📥 Descargar Guía Pedagógica",
                        data=archivo_pdf,
                        file_name=f"Guia_{tema}.pdf",
                        mime="application/pdf"
                    )
                    st.success("¡Documento generado exitosamente!")
