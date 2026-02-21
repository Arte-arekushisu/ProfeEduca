import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V1.2", page_icon="🍎", layout="wide")

# --- 2. LÓGICA DE CONTENIDO EXTENSO ---
def generar_planeacion_detallada(d):
    t = d['tema']
    
    return {
        "estaciones": [
            {
                "campo": "Lenguajes",
                "nombre": "Estación 1: El Arte de Comunicar",
                "materiales": "Revistas viejas, periódicos, pegamento, tijeras, hojas blancas y plumones.",
                "instrucciones": "Explorar diversas fuentes escritas para identificar palabras que nos ayuden a describir nuestro entorno.",
                "actividades": [
                    "1. Collage de palabras: Recorta letras o palabras de periódicos que te llamen la atención.",
                    "2. Mi mensaje al mundo: Con los recortes, arma una frase que exprese algo positivo para tus compañeros.",
                    "3. Diccionario visual: Dibuja el significado de una palabra nueva que hayas encontrado hoy."
                ]
            },
            {
                "campo": "Saberes y Pensamiento Científico",
                "nombre": "Estación 2: Exploradores de la Materia",
                "materiales": "Semillas de la región, vasos de plástico, agua, tierra, reglas y lupas.",
                "instrucciones": "Observar y medir elementos de la naturaleza para entender cómo cambian y crecen.",
                "actividades": [
                    "1. Clasificación científica: Separa las semillas por tamaño y color usando la lupa.",
                    "2. Midiendo la vida: Usa la regla para medir tres objetos naturales diferentes y anota los resultados.",
                    "3. Hipótesis: Dibuja qué crees que le pasará a una semilla si le ponemos mucha o poca agua."
                ]
            },
            {
                "campo": "Ética, Naturaleza y Sociedades",
                "nombre": "Estación 3: Guardianes del Planeta",
                "materiales": "Cartulinas, gises de colores, material reciclado (envases, cartón).",
                "instrucciones": "Reflexionar sobre nuestra responsabilidad en el cuidado de los seres vivos y el agua.",
                "actividades": [
                    "1. El plato del buen ambiente: Clasifica acciones que ayudan al planeta y las que lo dañan.",
                    "2. Propuesta comunitaria: Elige un problema de basura en tu calle y dibuja cómo lo solucionarías.",
                    "3. Mural colectivo: Usa los gises para crear un compromiso grupal de cuidado a la naturaleza."
                ]
            },
            {
                "campo": "De lo Humano y lo Comunitario",
                "nombre": "Estación 4: Tejiendo Comunidad",
                "materiales": "Estambre, telas, música rítmica, objetos de identidad local.",
                "instrucciones": "Fomentar la empatía y el reconocimiento de nuestras habilidades personales dentro del grupo.",
                "actividades": [
                    "1. El hilo de la amistad: Pasa el estambre a un compañero mencionando una cualidad que admiras de él.",
                    "2. Mi talento secreto: Representa con gestos algo que te gusta hacer por los demás.",
                    "3. Juego de roles: Dramatiza una situación donde ayudes a alguien de tu comunidad."
                ]
            }
        ],
        "tutoreo_dialogado": f"""
**Diálogo Sugerido (Tutor - Alumno):**
- **Tutor:** "¿Sabías que existen dos tipos de tortugas: la marina y la terrestre?"
- **Alumno:** "No profe, ¿cuál es la diferencia?"
- **Tutor:** "¡Mira! Hoy nos enfocaremos en la **Tortuga Marina**. ¿Sabías que en México tenemos 7 de las 8 especies que existen en el mundo?"
- **Propósito:** Generar curiosidad por la marina hoy, dejando la terrestre como un misterio que el niño podrá investigar por su cuenta más tarde (Fomentar autonomía).

**Preguntas Dinámicas:**
1. "¿Si fueras una tortuga, qué parte del océano te gustaría explorar?"
2. "¿Te gustaría ser un científico que protege sus nidos algún día?"
        """
    }

# --- 3. CLASE PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'PLANEACIÓN', 0, 1, 'C') # Título solicitado
        self.ln(5)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11); self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, 0, 1, 'L', True); self.ln(2)

# --- 4. INTERFAZ ---
st.header("📋 Generador de Planeación Pedagógica")

with st.form("form_v12"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", value="Multigrado")
        nombre_ed = st.text_input("Educador")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema = st.text_input("Tema de Interés", placeholder="Ej. Tortugas Marinas")
    
    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN COMPLETA")

if submit:
    if not tema or not nombre_ed:
        st.error("⚠️ Falta completar el Nombre o el Tema.")
    else:
        info = {"nivel": nivel, "grado": grado, "nombre_ed": nombre_ed, "comunidad": comunidad, "fecha": str(fecha), "tema": tema}
        content = generar_planeacion_detallada(info)
        
        # --- PDF GENERATION ---
        pdf = PDF()
        pdf.add_page()
        
        # I. Identificación
        pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 7, f"Educador: {nombre_ed} | Nivel/Grado: {nivel} {grado} | Comunidad: {comunidad}", 0, 1)
        pdf.cell(0, 7, f"Fecha: {fecha} | Tema Central: {tema}", 0, 1)

        # II. Estaciones
        pdf.chapter_title("II. ESTACIONES DE APRENDIZAJE (4 CAMPOS FORMATIVOS)")
        for est in content['estaciones']:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f"{est['nombre']} ({est['campo']})", 0, 1)
            pdf.set_font('Arial', 'I', 9)
            pdf.multi_cell(0, 5, f"Materiales: {est['materiales']}")
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, f"Instrucciones: {est['instrucciones']}")
            for act in est['actividades']:
                pdf.cell(5); pdf.multi_cell(0, 5, f"- {act}")
            pdf.ln(3)

        # III. Tutoreo
        pdf.chapter_title(f"III. TUTOREO UNO A UNO: {tema.upper()}")
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, content['tutoreo_dialogado'])

        # IV. Cierre
        pdf.chapter_title("IV. ACTIVIDADES POST-RECESO")
        pdf.multi_cell(0, 5, "1. Reflexión colectiva: ¿Qué estación fue la más difícil hoy?\n2. Limpieza del aula: Organización de materiales para la siguiente jornada.")

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 DESCARGAR PLANEACIÓN (PDF)", data=pdf_bytes, file_name=f"Planeacion_{tema}.pdf", use_container_width=True)
        st.success("¡Planeación lista para imprimir!")
