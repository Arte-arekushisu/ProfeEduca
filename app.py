import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V0.9", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE REDACCIÓN EXTENSA ---
def redactar_guia_completa(d):
    # Adaptación de complejidad según nivel
    if d['nivel'] == "Preescolar":
        pautas = "Uso de cantos, manipulación de texturas y dibujos grandes."
    elif d['nivel'] == "Primaria":
        pautas = "Uso de esquemas simples, investigación en libros y experimentos."
    else:
        pautas = "Debates, análisis de textos científicos y prototipos complejos."

    return {
        "inicio_grupo": {
            "pase": "Actividad 'El eco de mi voz': Al mencionar su nombre, el alumno imita un sonido de la naturaleza o dice una palabra positiva. Ayuda a romper el hielo y centrar la atención.",
            "lectura": f"Momento literario: El educador lee con pausas dramáticas para fomentar la imaginación. Al terminar, los alumnos explican en voz alta qué harían ellos en el lugar del protagonista.",
            "bienvenida": "Dinámica 'El nudo de amistad': El grupo forma un círculo tomándose de las manos y debe desenredarse sin soltarse, fomentando la resolución de problemas en equipo."
        },
        "estaciones": [
            {"t": "Estación de Lenguaje", "d": f"Instrucciones: Los alumnos crearán un mural de palabras clave. {pautas} Materiales sugeridos: Cartón reciclado, gises, recortes de revistas."},
            {"t": "Estación de Pensamiento", "d": f"Instrucciones: Resolución de retos lógicos usando semillas o piedras de la región para contar o medir. {pautas}"},
            {"t": "Estación de Saberes", "d": f"Instrucciones: Observación directa del entorno para identificar cambios en la naturaleza o el clima local. {pautas}"}
        ],
        "tutoreo_especifico": {
            "tema_desarrollo": f"Estudio profundo sobre: {d['tema']}. El tutor guiará al alumno para investigar los orígenes, funciones e importancia de este tema en la vida real.",
            "pasos": [
                f"1. Diagnóstico Inicial: ¿Qué sabemos sobre {d['tema']}? Anotamos ideas previas.",
                "2. Investigación Dirigida: Consultar el rincón de lectura y seleccionar dos fuentes confiables.",
                "3. Registro RPA (Relación de Aprendizaje): El alumno narra su proceso de descubrimiento paso a paso.",
                "4. Producto Final: Elaboración de un objeto tangible (maqueta, cartel o prototipo) que demuestre lo aprendido."
            ]
        },
        "post_receso": [
            {"m": d['m1'], "d": "Actividad: Desarrollo de habilidades motrices y coordinación grupal a través de juegos tradicionales adaptados al espacio del aula."},
            {"m": d['m2'], "d": "Actividad: Integración de saberes mediante el arte o la expresión corporal, utilizando materiales sobrantes de las estaciones anteriores."}
        ]
    }

# --- 3. CLASE PARA PDF DE ALTA CALIDAD ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PLANEACIÓN INTEGRAL - MODELO DE DIÁLOGO', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- 4. INTERFAZ DE USUARIO ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"

col_menu, col_main = st.columns([1, 3])

with col_menu:
    st.title("🍎 Menú")
    if st.button("🏠 Inicio", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"

with col_main:
    if st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación")
        
        with st.form("mi_formulario"):
            c1, c2 = st.columns(2)
            with c1:
                nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
                grado = st.text_input("Grado", placeholder="Ej. 1º Multigrado")
                nombre_ed = st.text_input("Educador")
                nombre_eca = st.text_input("Nombre del ECA")
            with c2:
                comunidad = st.text_input("Comunidad")
                fecha = st.date_input("Fecha de planeación")
