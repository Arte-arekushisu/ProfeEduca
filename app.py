import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
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
    .stButton>button:hover {
        border-color: #38bdf8;
        color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE GENERACIÓN PEDAGÓGICA (Simulación de IA) ---
def redactar_contenido(tema, nivel):
    # Esta función simula la redacción inteligente basada en el tema
    return {
        "pase_lista": f"Dinámica 'La palabra mágica': Al decir presente, el alumno comparte algo que use en su casa relacionado con {tema}.",
        "regalo_lectura": f"Cuento: 'El gran misterio de {tema}'. Un relato corto que explica cómo este tema ayuda a que la comunidad progrese.",
        "bienvenida": f"Actividad: 'El árbol de saberes'. Dibujamos un tronco en el suelo y cada niño pone una piedra (idea) sobre lo que cree que es {tema}.",
        "estacion1": f"OBSERVACIÓN: Usar lupas o recipientes para encontrar ejemplos de {tema} en el patio del salón.",
        "estacion2": f"CONSTRUCCIÓN: Crear una representación de {tema} usando lodo, ramitas o envases de plástico limpios.",
        "estacion3": f"DIÁLOGO: En parejas, explicarle al compañero cómo se vive el tema {tema} en su propia familia.",
        "tutoreo_tema": f"El estudio profundo de {tema} nos permite entender cómo funcionan los ciclos en nuestra región y valorar los recursos locales.",
        "tutoreo_actividades": f"1. Elaborar un dibujo narrativo del proceso de {tema}.\n2. Realizar una entrevista a un sabio de la comunidad sobre este tema.",
        "producto": f"Un 'Periódico Mural' hecho con cartones donde se peguen los hallazgos del día sobre {tema}."
    }

# --- 3. CLASE PARA DISEÑO DE PDF ---
class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'GUÍA DE APRENDIZAJE BASADA EN EL DIÁLOGO', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

def crear_pdf_maestro(d):
    pdf = PlaneacionPDF()
    pdf.add_page()
    
    # 1. TABLA DE IDENTIFICACIÓN
    pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
    pdf.set_font('Arial', 'B', 10)
    col_width = 45
    
    # Filas de la tabla
    campos = [
        ["Nivel Educativo", d['nivel']], ["Grado", d['grado']],
        ["Educador", d['nombre_ed']], ["ECA", d['nombre_eca']],
        ["Comunidad", d['comunidad']], ["Fecha", d['fecha']],
        ["Rincón", d['rincon']]
    ]
    
    for row in campos:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(col_width, 8, row[0], 1, 0, 'L', True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 8, str(row[1]), 1, 1, 'L')
        pdf.set_font('Arial', 'B', 10)
    pdf.ln(5)

    # 2. OBJETIVO GENERAL
    pdf.chapter_title("II. OBJETIVO GENERAL")
    pdf.set_font('Arial', '', 10)
    obj = (f"Que los estudiantes de {d['nivel']} logren una comprensión integral del tema '{d['tema']}' "
           "mediante la investigación participativa y el intercambio de ideas. Se busca que el alumno "
           "no solo memorice, sino que sea capaz de aplicar estos conocimientos en su entorno comunitario.")
    pdf.multi_cell(0, 5, obj)
    pdf.ln(5)

    # 3. CONTENIDO PEDAGÓGICO REDACTADO
    ia = redactar_contenido(d['tema'], d['nivel'])
    
    pdf.chapter_title("III. MOMENTOS DE INICIO (ESTRATEGIA VISUAL)")
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Pase de lista (5 min):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, ia['pase_lista']); pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Regalo de lectura (10 min):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, ia['regalo_lectura']); pdf.ln(2)

    pdf.chapter_title("IV. ESTACIONES DE APRENDIZAJE (PARA CARTULINA)")
    pdf.multi_cell(0, 6, f"Estación 1: {ia['estacion1']}\n\nEstación 2: {ia['estacion2']}\n\nEstación 3: {ia['estacion3']}")
    pdf.ln(5)

    pdf.chapter_title(f"V. TUTOREO UNO A UNO: {d['tema'].upper()}")
    pdf.multi_cell(0, 5, f"Tema a desarrollar: {ia['tutoreo_tema']}\n\nActividades:\n{ia['tutoreo_actividades']}")
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Producto Sugerido:", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, ia['producto'])

    pdf.chapter_title("VI. ACTIVIDADES POST-RECESO (TIEMPOS PEDAGÓGICOS)")
    pdf.multi_cell(0, 6, f"Materia 1: {d['materia1']} - Actividad práctica integradora.\nMateria 2: {d['materia2']} - Sesión de motricidad o expresión.")

    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ DE USUARIO ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"

col_menu, col_main =
