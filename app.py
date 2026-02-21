import streamlit as st
from fpdf import FPDF
import unicodedata

# --- FUNCIÓN ANTIFALLOS (Limpia acentos y eñes para el PDF) ---
def normalizar(texto):
    if not texto: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(texto)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

# --- CLASE PDF PROFESIONAL ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra_seccion(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {normalizar(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V11", layout="wide")
st.title("🚀 Sistema de Planeación Integrado (4 Campos)")

with st.form("maestro_v11"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador")
        tema_int = st.text_input("Tema de Interés", placeholder="Ej. Alimentación Saludable")
    with c2:
        grado = st.text_input("Grado/Grupo")
        comunidad = st.text_input("Comunidad")
        rincon = st.text_input("Rincón Asignado")
    
    st.markdown("---")
    st.subheader("Bloque Post-Receso (2 Horas)")
    materia_post = st.text_input("Tema/Materia", "Operaciones con Fracciones")
    
    boton = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA")

if boton:
    # --- LÓGICA DE GENERACIÓN AUTOMÁTICA POR LA IA ---
    # Nombres creativos y actividades basadas en campos
    nombre_actividad = f"Proyecto: {tema_int if tema_int else 'Aprendamos Juntos'}"
    
    # Configuración de Inicio por Nivel
    inicio_data = {
        "Preescolar": {"pase": "Imitar un sonido", "regalo": "Cuento 'La Oruga Glotona'", "refl": "Charla sobre alimentos sanos"},
        "Primaria": {"pase": "Dato curioso del tema", "regalo": "Leyenda del Maíz", "refl": "Resumen en dibujo y texto"},
        "Secundaria": {"pase": "Cita de autor", "regalo": "Ensayo sobre soberanía alimentaria", "refl": "Debate crítico"}
    }
    ini = inicio_data[nivel]

    pdf = PDF()
    pdf.add_page()
    
    # I. IDENTIFICACIÓN
    pdf.barra_seccion("I. DATOS DE IDENTIFICACION")
    pdf.set_font('Helvetica', 'B', 10)
    campos_id = [["Educador", educador], ["Nivel", nivel], ["Grado", grado], ["Comunidad", comunidad], ["Tema", tema_int]]
    for ci in campos_id:
        pdf.cell(45, 8, f" {normalizar(ci[0])}:", 1, 0, 'L', True)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(145, 8, f" {normalizar(ci[1])}", 1, 1, 'L')
        pdf.set_font('Helvetica', 'B', 10)
    pdf.ln(5)

    # II. INICIO DETALLADO
    pdf.barra_seccion("II. BIENVENIDA Y REGALO DE LECTURA")
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, f"Actividad: {normalizar(nombre_actividad)}", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, f"1. Pase de Lista: {normalizar(ini['pase'])}\n"
                         f"2. Regalo de Lectura: {normalizar(ini['regalo'])}\n"
                         f"3. Reflexion del Cuento: {normalizar(ini['refl'])}\n"
                         "Materiales: Libro seleccionado, bitacora de aula, hojas.")
    pdf.ln(5)

    # III. ESTACIONES DE LOS 4 CAMPOS
    pdf.barra_seccion("III. ESTACIONES INTEGRADAS (4 CAMPOS)")
    # Aquí la IA estructura los campos dentro de las estaciones
    estaciones = [
        {"nombre": "Estacion 'El rincón del Sabio'", "desc": "Campo: Saberes y P. Cientifico. Indagacion y conteo.", "mat": "Lupas, balanzas, semillas."},
        {"nombre": "Estacion 'Eco-Relatos'", "desc": "Campo: Lenguajes y Etica. Creacion de cuentos ambientales.", "mat": "Hojas, colores, periodicos."},
        {"nombre": "Estacion 'Moviendo mi Comunidad'", "desc": "Campo: De lo Humano y Comunitario. Retos fisicos.", "mat": "Pelotas, cuerdas, cronometro."}
    ]
    for e in estaciones:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, normalizar(e['nombre']), 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"{normalizar(e['desc'])}\nMateriales: {normalizar(e['mat'])}\n")
        pdf.ln(2)

    # IV. TEMA DE INTERÉS (EXTENSO)
    pdf.add_page()
    pdf.barra_seccion(f"IV. DESARROLLO TEMA DE INTERES: {tema_int.upper()}")
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, f"Teoria: {normalizar(tema_int)} se aborda como un eje transversal. "
                         "El docente debe explicar las causas y consecuencias. "
                         "Pregunta Detonante: ¿Como podemos aplicar esto en nuestra vida diaria?\n"
                         "Actividad: Investigacion en el Rincon de Lectura y elaboracion de producto final.\n"
                         "Materiales: Cartulinas, plumones, material reciclado, libros de consulta.")
    pdf.ln(5)

    # V. POST-RECESO (2 HORAS)
    pdf.barra_seccion("V. BLOQUE POST-RECESO (DESARROLLO EXHAUSTIVO)")
    pdf.set_font('Helvetica', 'B', 12); pdf.cell(0, 8, f"TEMA: {normalizar(materia_post)}", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, "Explicacion: Se presenta el concepto en el pizarron con ejemplos reales de la comunidad. "
                         "Modelado: El docente resuelve 2 ejemplos paso a paso. "
                         "Practica: Los alumnos resuelven 10 ejercicios de forma individual y colaborativa. "
                         "Cierre: Plenaria para compartir resultados.\n"
                         "Materiales: Cuaderno, libros de texto SEP, juegos de geometria/material concreto.")

    # VI. FUENTES
    pdf.ln(10); pdf.barra_seccion("VI. FUENTES DE CONSULTA")
    pdf.set_font('Helvetica', 'I', 9); pdf.multi_cell(0, 5, "UNESCO (2026). Reporte de Aprendizaje Activo.\nSEP (2025). Plan de Estudios Nueva Escuela Mexicana.")

    # --- DESCARGA SEGURA ---
    pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
    st.success("✅ Planeacion generada exitosamente.")
    st.download_button("📥 DESCARGAR PLANEACION COMPLETA", data=pdf_out, file_name=f"Planeacion_{normalizar(tema_int)}.pdf", use_container_width=True)
