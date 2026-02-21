import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V1.3", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE CONTENIDO PEDAGÓGICO ---
def obtener_contenido_estaciones(tema):
    return [
        {
            "campo": "Lenguajes",
            "nombre": "Estación 1: Aprendamos a Comunicar",
            "materiales": "Papel bond, recortes de periódico, pegamento, tijeras, colores y marcadores.",
            "instrucciones": "Utilizar diferentes lenguajes (escrito y gráfico) para expresar ideas sobre nuestro entorno.",
            "actividades": [
                f"1. Muro de palabras: Identifica en periódicos 5 palabras relacionadas con '{tema}' y pégalas en un mural colectivo.",
                "2. Cartel informativo: Elabora un dibujo grande que explique qué es lo que más te gusta de este tema.",
                "3. Mensaje a la comunidad: Redacta una frase corta invitando a otros a aprender sobre lo que descubriste hoy."
            ]
        },
        {
            "campo": "Saberes y Pensamiento Científico",
            "nombre": "Estación 2: Explorando y Contando",
            "materiales": "Objetos de la región (piedras, semillas), cinta métrica, lupas y cuadernos.",
            "instrucciones": "Aplicar el pensamiento matemático y la observación científica para analizar elementos reales.",
            "actividades": [
                f"1. Clasificación por atributos: Agrupa los materiales por tamaño, peso o color relacionados con '{tema}'.",
                "2. Registro de datos: Mide tres objetos diferentes y anota los resultados comparando cuál es más grande.",
                "3. Laboratorio de dibujo: Observa un objeto con la lupa y dibuja detalladamente sus partes ocultas a simple vista."
            ]
        },
        {
            "campo": "Ética, Naturaleza y Sociedades",
            "nombre": "Estación 3: Guardianes de la Vida",
            "materiales": "Cartulinas, imágenes del plato del buen comer, gises, botes de reciclaje.",
            "instrucciones": "Reflexionar sobre la salud personal y el cuidado del medio ambiente en nuestra comunidad.",
            "actividades": [
                "1. El plato del buen ambiente: Clasifica imágenes de alimentos en saludables y no saludables explicando por qué.",
                "2. Mi compromiso natural: Dibuja una acción que realizarás en casa para cuidar a los seres vivos estudiados hoy.",
                "3. Mapa de la comunidad: Ubica en un dibujo dónde se encuentran los recursos naturales más importantes de tu pueblo."
            ]
        },
        {
            "campo": "De lo Humano y lo Comunitario",
            "nombre": "Estación 4: Construyendo Juntos",
            "materiales": "Estambre, telas, música, material de reúso.",
            "instrucciones": "Desarrollar habilidades socioemocionales y trabajo en equipo mediante la expresión corporal.",
            "actividades": [
                "1. El hilo que nos une: En círculo, lanza una bola de estambre a un compañero mencionando algo nuevo que aprendiste hoy.",
                "2. Dramatización: En equipo, representen una escena donde ayuden a proteger la naturaleza.",
                "3. Invento comunitario: Usando material de reúso, construyan un objeto que sea útil para todos en el salón."
            ]
        }
    ]

# --- 3. CLASE PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'PLANEACIÓN', 0, 1, 'C')
        self.ln(5)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11); self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', True); self.ln(2)

# --- 4. INTERFAZ ---
st.header("📋 Generador de Planeación Pedagógica")

with st.form("form_completo"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", placeholder="Ej. 1º Multigrado")
        nombre_ed = st.text_input("Educador")
        nombre_eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha de planeación")
        tema = st.text_input("Tema de Interés", placeholder="Ej. Tortugas Marinas")
        rincon = st.text_input("Rincón asignado")
    
    st.markdown("---")
    st.subheader("Materias Post-Receso")
    m1 = st.text_input("Materia 1", value="Educación Física")
    m2 = st.text_input("Materia 2", placeholder="Ej. Tipos de texto")
    
    submit = st.form_submit_button("🔨 GENERAR PLANEACIÓN COMPLETA")

if submit:
    if not tema or not nombre_ed:
        st.error("⚠️ Debes ingresar al menos el nombre del Educador y el Tema.")
    else:
        estaciones = obtener_contenido_estaciones(tema)
        
        # --- GENERAR PDF ---
        pdf = PDF()
        pdf.add_page()
        
        pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 7, f"Educador: {nombre_ed} | ECA: {nombre_eca} | Nivel/Grado: {nivel}/{grado}", 0, 1)
        pdf.cell(0, 7, f"Comunidad: {comunidad} | Fecha: {fecha} | Rincón: {rincon}", 0, 1)

        pdf.chapter_title("II. MOMENTO DE INICIO")
        pdf.multi_cell(0, 5, "1. Bienvenida rítmica: Dinámica de integración para enfocar la atención.\n2. Regalo de lectura: Texto narrativo que genere curiosidad sobre el entorno.\n3. Activación: Preguntas sobre saberes previos del tema central.")

        pdf.chapter_title("III. ESTACIONES POR CAMPOS FORMATIVOS")
        for est in estaciones:
            pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, est['nombre'], 0, 1)
            pdf.set_font('Arial', 'I', 9); pdf.multi_cell(0, 5, f"Materiales sugeridos: {est['materiales']}")
            pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, f"Instrucciones: {est['instrucciones']}")
            for act in est['actividades']:
                pdf.cell(5); pdf.multi_cell(0, 5, f"- {act}")
            pdf.ln(2)

        pdf.chapter_title(f"IV. TUTOREO: {tema.upper()}")
        pdf.multi_cell(0, 5, f"- Tutor: '¿Sabías que existen dos tipos de tortugas: la marina y la terrestre?'\n- Alumno: 'No profe...'\n- Tutor: '¡Sí! Hoy veremos la MARINA. ¿Sabías que en México hay 7 especies?' (Dejar la terrestre como misterio para fomentar autonomía).")

        pdf.chapter_title("V. ACTIVIDADES POST-RECESO")
        pdf.multi_cell(0, 6, f"1. {m1}: Actividades de desarrollo motor y coordinación.\n2. {m2}: Cierre pedagógico y reflexión sobre los hallazgos del día.")

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 DESCARGAR PDF", data=pdf_bytes, file_name=f"Planeacion_{tema}.pdf", use_container_width=True)
        st.success("¡Planeación generada con éxito!")
