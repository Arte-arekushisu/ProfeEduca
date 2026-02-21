import streamlit as st
from fpdf import FPDF

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V1.5", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE CONTENIDO EXTENSO ---
def obtener_contenido_completo(tema):
    return [
        {
            "campo": "Lenguajes",
            "nombre": "Estación 1: Aprendamos a Comunicar",
            "materiales": "Hojas blancas, recortes de periódico, revistas, pegamento, tijeras, marcadores de colores.",
            "instrucciones": "El educador preparará una mesa con diversos recortes. El alumno debe explorar cómo las palabras y las imágenes nos ayudan a describir el mundo.",
            "actividades": [
                f"1. Muro de conceptos: Busca y recorta 5 imágenes o palabras que asocias con '{tema}' y pégalas en un cartel común.",
                "2. Reportero escolar: Redacta una noticia corta (o haz un dibujo narrativo) sobre un descubrimiento importante que hayas hecho hoy.",
                "3. El mensaje oculto: Elige una palabra difícil de la lectura y búscala en el periódico para entender cómo se usa en otros textos."
            ]
        },
        {
            "campo": "Saberes y Pensamiento Científico",
            "nombre": "Estación 2: Exploradores del Cálculo",
            "materiales": "Semillas, piedras, balanza escolar (o casera), cintas métricas, cuadernos de registro.",
            "instrucciones": "Utilizar herramientas de medición para comparar objetos del entorno y registrar datos numéricos.",
            "actividades": [
                f"1. Clasificación por peso: Elige 10 objetos del rincón y agrúpalos de los más ligeros a los más pesados.",
                "2. Geometría natural: Encuentra formas circulares o rectangulares en los materiales de '{tema}' y mide su contorno con el estambre.",
                "3. Gráfica de hallazgos: Dibuja una tabla simple donde registres cuántas semillas o piedras de cada color encontraste."
            ]
        },
        {
            "campo": "Ética, Naturaleza y Sociedades",
            "nombre": "Estación 3: Guardianes de la Tierra",
            "materiales": "Cartulinas, gises, imágenes del Plato del Bien Comer, botes para separar basura, agua.",
            "instrucciones": "Analizar nuestras acciones diarias y su impacto en la salud personal y la biodiversidad de la comunidad.",
            "actividades": [
                "1. Clasificación Nutricional: En una cartulina, divide alimentos en 'Saludables' y 'No saludables' justificando por qué uno ayuda a crecer y el otro no.",
                "2. El ciclo del cuidado: Dibuja el proceso de cómo cuidar una planta o un animal de la región para que no desaparezca.",
                "3. Acuerdo de paz con la naturaleza: Escribe o dibuja una regla para el salón que ayude a no desperdiciar agua o papel."
            ]
        },
        {
            "campo": "De lo Humano y lo Comunitario",
            "nombre": "Estación 4: Tejiendo Nuestra Identidad",
            "materiales": "Estambre, telas, música tradicional, objetos de identidad local o familiar.",
            "instrucciones": "Fomentar la convivencia armónica y el reconocimiento de las capacidades de cada integrante del grupo.",
            "actividades": [
                "1. El hilo de la fortaleza: Lanza una bola de estambre a un compañero diciendo una habilidad que él tiene y tú admiras.",
                "2. Dramatización de ayuda: Representa con mímica una situación donde la comunidad se une para resolver un problema.",
                "3. Invento colectivo: Usando solo materiales de reúso, el equipo debe construir una herramienta que facilite una tarea del salón."
            ]
        }
    ]

# --- 3. CLASE PARA PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'PLANEACIÓN', 0, 1, 'C')
        self.ln(5)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11); self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', True); self.ln(2)

# --- 4. INTERFAZ DE USUARIO ---
st.header("📋 Generador Pedagógico ABCD")

with st.form("form_final_v15"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", value="Multigrado")
        nombre_ed = st.text_input("Educador")
        nombre_eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema = st.text_input("Tema de Interés", placeholder="Ej. Tortugas Marinas")
        rincon = st.text_input("Rincón asignado")
    
    st.markdown("---")
    m1 = st.text_input("Materia Post-Receso 1", value="Educación Física")
    m2 = st.text_input("Materia Post-Receso 2", value="Vida Saludable")
    
    submit = st.form_submit_button("🔨 GENERAR Y REVISAR PLANEACIÓN")

if submit:
    if not tema or not nombre_ed:
        st.error("⚠️ Es obligatorio el nombre del Educador y el Tema de Interés.")
    else:
        estaciones = obtener_contenido_completo(tema)
        
        # ---
