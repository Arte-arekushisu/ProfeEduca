import streamlit as st
from fpdf import FPDF
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V3.0", page_icon="🍎", layout="wide")

# --- 2. CLASE PDF OPTIMIZADA (Soporta caracteres especiales) ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PLANEACION PEDAGOGICA - MODELO ABCD', 0, 1, 'C')
        self.ln(5)

    def seccion_titulo(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(40, 54, 85)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f" {titulo}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

# --- 3. LÓGICA DE CONTENIDO ---
def generar_dinamica_inicio(nivel):
    opciones = {
        "Preescolar": {
            "lista": "Cantar 'Sol solecito' y cada niño imita un animal al decir presente.",
            "lectura": "Cuento 'El monstruo de colores'.",
            "reflexion": "Dialogar sobre cómo se siente hoy cada color en nuestro salon."
        },
        "Primaria": {
            "lista": "Mencionar una palabra que rime con su nombre.",
            "lectura": "Leyenda de los volcanes.",
            "reflexion": "Analizar la importancia de la perseverancia en los personajes."
        },
        "Secundaria": {
            "lista": "Mencionar un dato curioso del tema de interes.",
            "lectura": "Ensayo corto de divulgacion cientifica.",
            "reflexion": "Debate rapido sobre la postura del autor."
        }
    }
    return opciones.get(nivel)

# --- 4. INTERFAZ DE USUARIO ---
st.title("🍎 Taller de Planeacion ABCD")
st.markdown("### Llenado de Guia Maestra")

with st.form("form_docente"):
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "1ro Multigrado")
        nombre_ed = st.text_input("Educador", "Axel Reyes")
        nombre_eca = st.text_input("Nombre del ECA", "Comunidad de Aprendizaje")
    with col2:
        comunidad = st.text_input("Comunidad", "San Michi")
        fecha_p = st.date_input("Fecha")
        tema_int = st.text_input("Tema de Interes", "Tortugas Marinas")
        rincon = st.text_input("Rincon Asignado", "Rincon de Lectura")

    st.markdown("---")
    st.subheader("Bloque Post-Receso (2 Horas)")
    m1_t = st.text_input("Materia 1 y Actividad", "Suma de fracciones con material concreto")
    m2_t = st.text_input("Materia 2 y Actividad", "Vida Saludable: El plato del buen comer")
    
    boton = st.form_submit_button("🚀 GENERAR PLANEACION COMPLETA")

if boton:
    # --- CUENTA REGRESIVA ---
    progreso = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progreso.progress(i + 1)
    
    st.success("✅ ¡Planeacion generada con exito! Revisa la vista previa abajo.")

    # Datos calculados
    din = generar_dinamica_inicio(nivel)
    
    # --- VISTA PREVIA ---
    st.subheader(f"Vista Previa: {tema_int}")
    with st.expander("Ver estructura detallada"):
        st.write(f"**Inicio:** {din['lista']}")
        st.write(f"**Lectura:** {din['lectura']}")
        st.write(f"**Post-Receso:** {m1_t} y {m2_t}")

    # --- CONSTRUCCIÓN DEL PDF ---
    pdf = PDF()
    pdf.add_page()
    
    # I. DATOS
    pdf.seccion_titulo("I. DATOS DE IDENTIFICACION")
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 7, f"Educador: {nombre_ed} | ECA: {nombre_eca}", 1, 1)
    pdf.cell(0, 7, f"Nivel: {nivel} | Grado: {grado} | Comunidad: {comunidad}", 1, 1)
    pdf.cell(0, 7, f"Fecha: {fecha_p} | Rincon: {rincon}", 1, 1)
    pdf.ln(5)

    # II. INICIO
    pdf.seccion_titulo("II. INICIO Y BIENVENIDA (PEDAGOGIA DEL AFECTO)")
    pdf.multi_cell(0, 7, f"1. Pase de lista: {din['lista']}\n"
                         f"2. Regalo de lectura: {din['lectura']}\n"
                         f"3. Reflexion: {din['reflexion']}")
    pdf.ln(5)

    # III. ESTACIONES
    pdf.seccion_titulo("III. ESTACIONES POR 4 CAMPOS FORMATIVOS")
    campos = ["Lenguajes", "Saberes y P. Cientifico", "Etica, Nat. y Soc.", "De lo Humano y Com."]
    for campo in campos:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, f"Estacion: {campo}", 0, 1)
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, f"Proposito: Que el alumno desarrolle autonomia explorando {tema_int}.\n"
                             f"Materiales: Material reciclado, libros del rincon, hojas y colores.\n"
                             f"Actividades: 1. Investigacion libre, 2. Creacion de prototipo, 3. Registro en cuaderno.\n")
        pdf.ln(2)

    # IV. TEMA DE INTERÉS
    pdf.seccion_titulo(f"IV. TUTOREO: {tema_int.upper()}")
    pdf.multi_cell(0, 6, f"Informacion del tema: {tema_int} es vital para el ecosistema de {comunidad}. "
                         f"Cientificamente se sabe que su ciclo de vida depende de la temperatura del nido...\n"
                         f"Pregunta detonante: ¿Que pasaria si en nuestra comunidad ya no existiera {tema_int}?\n"
                         f"Fuentes: UNESCO (2025) 'La biodiversidad local', SEP 'Libro de proyectos'.")

    # V. POST-RECESO
    pdf.seccion_titulo("V. BLOQUE POST-RECESO (DESARROLLO EXTENSO)")
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, f"Materia 1: {m1_t}", 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, "Explicacion: Se inicia con una lluvia de ideas. Se presenta el concepto en el pizarron. "
                         "Ejemplo: Si tenemos 1/4 y sumamos 2/4... Actividad: Resolver 5 ejercicios en parejas.")
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, f"Materia 2: {m2_t}", 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, "Actividad de cierre: Plenaria grupal donde cada alumno comparte su mayor aprendizaje del dia.")

    # --- DESCARGA ---
    # Usamos 'latin-1' con reemplazo para evitar el error de caracteres extraños
    pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button(
        label="📥 DESCARGAR PLANEACION COMPLETA PDF",
        data=pdf_output,
        file_name=f"Planeacion_{tema_int}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
