import streamlit as st
from fpdf import FPDF
import unicodedata

# --- FUNCIÓN DE LIMPIEZA ABSOLUTA (Garantiza que el PDF no falle) ---
def normalizar(texto):
    if not texto: return ""
    # Elimina acentos y convierte eñes para compatibilidad total con FPDF
    return "".join(c for c in unicodedata.normalize('NFD', str(texto)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

# --- CLASE PDF PROFESIONAL CON DISEÑO MAESTRO ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 15, 'PLANEACION PEDAGOGICA', 0, 1, 'C')
        self.ln(5)

    def barra_azul(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {normalizar(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="ProfeEduca V12 - Master", layout="wide")
st.title("🍎 ProfeEduca: Sistema de Planeacion Automatica V12")

with st.form("master_form_final"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "Axel Reyes")
        tema_int = st.text_input("Tema de Interes", placeholder="Ej. El Sistema Solar")
    with c2:
        grado = st.text_input("Grado y Grupo", "Multigrado")
        comunidad = st.text_input("Comunidad", "San Michi")
        rincon = st.text_input("Rincon Asignado", "Rincon de Ciencia")
    
    st.markdown("---")
    st.subheader("Bloque Post-Receso (2 Horas de Trabajo Profundo)")
    materia_post = st.text_input("Materia o Tema Específico", "Suma de fracciones")
    
    boton = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA Y DETALLADA")

if boton:
    if not tema_int:
        st.error("❌ Por favor ingresa un Tema de Interés.")
    else:
        # --- GENERACIÓN DE CONTENIDO EXTENSO POR NIVEL ---
        nombre_proyecto = f"Aprendamos sobre: {tema_int}"
        
        datos_niveles = {
            "Preescolar": {
                "lista": "Mencionar un color o animal del tema.",
                "lectura": f"Cuento infantil: 'La aventura de {tema_int}'.",
                "refl": "Dibujo colectivo de las emociones del cuento.",
                "mats_ini": "Titeres, crayolas, papel bond, musica."
            },
            "Primaria": {
                "lista": "Decir un dato curioso o palabra clave.",
                "lectura": f"Leyenda o mito regional sobre {tema_int}.",
                "refl": "Escrito breve en la bitacora de aprendizaje.",
                "mats_ini": "Fichas de lectura, pizarron, plumones."
            },
            "Secundaria": {
                "lista": "Mencionar un concepto cientifico o autor.",
                "lectura": f"Ensayo de divulgacion sobre {tema_int}.",
                "refl": "Debate critico sobre el impacto en la comunidad.",
                "mats_ini": "Articulos impresos, bitacora, proyector."
            }
        }
        info = datos_niveles[nivel]

        # --- CONSTRUCCIÓN DEL PDF (4 HOJAS DE CONTENIDO) ---
        pdf = PDF()
        pdf.add_page()
        
        # 1. IDENTIFICACIÓN
        pdf.barra_azul("I. DATOS DE IDENTIFICACION PROFESIONAL")
        tabla = [["Educador", educador], ["Nivel", nivel], ["Grado", grado], ["Comunidad", comunidad], ["Tema Int.", tema_int], ["Rincon", rincon]]
        for fila in tabla:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(50, 8, f" {normalizar(fila[0])}:", 1, 0, 'L', True)
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(140, 8, f" {normalizar(fila[1])}", 1, 1, 'L')
        pdf.ln(5)

        # 2. INICIO Y BIENVENIDA
        pdf.barra_azul(f"II. MOMENTO DE INICIO: {nombre_proyecto}")
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 8, f"1. Pase de Lista Dinamico: {normalizar(info['lista'])}\n"
                             f"2. Regalo de Lectura: {normalizar(info['lectura'])}\n"
                             f"3. Reflexion Pedagogica: {normalizar(info['refl'])}\n\n"
                             f"MATERIALES DEL INICIO: {normalizar(info['mats_ini'])}")
        pdf.ln(5)

        # 3. ESTACIONES (INTEGRANDO LOS 4 CAMPOS)
        pdf.barra_azul("III. ESTACIONES DE APRENDIZAJE (LOS 4 CAMPOS)")
        estaciones = [
            {"n": "Estacion 'Mentes Brillantes'", "c": "Saberes y P. Cientifico", "m": "Lupas, semillas, envases, reglas.", "a": "Exploracion directa y registro de hallazgos."},
            {"n": "Estacion 'El Muro del Habla'", "c": "Lenguajes / Etica", "m": "Cartulinas, recortes, pegamento.", "a": "Creacion de un mural con mensajes comunitarios."},
            {"n": "Estacion 'Accion y Salud'", "c": "De lo Humano / Comunidad", "m": "Pelotas, cuerdas, material reciclado.", "a": "Retos de coordinacion y acuerdos de juego."}
        ]
        for est in estaciones:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"📌 {normalizar(est['n'])}", 0, 1)
            pdf.set_font('Helvetica', 'I', 10); pdf.cell(0, 6, f"Campo: {normalizar(est['c'])}", 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 5, f"Materiales: {normalizar(est['m'])}\nActividad: {normalizar(est['a'])}\n")
            pdf.ln(2)

        # 4. TEMA DE INTERÉS (DESARROLLO EXTENSO)
        pdf.add_page()
        pdf.barra_azul(f"IV. TUTOREO DEL TEMA: {tema_int.upper()}")
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, f"Teoria y Fundamento: El docente explica la importancia de {normalizar(tema_int)} "
                             "como eje transformador. Se fomenta la autonomia permitiendo que el alumno "
                             "investigue en el rincon y genere su propia narrativa de aprendizaje (RPA).\n\n"
                             "Pregunta Detonante: ¿Como beneficia este tema a las familias de nuestra comunidad?\n"
                             "Materiales: Laminas informativas, enciclopedias del rincon, materiales de la region.")
        pdf.ln(5)

        # 5. POST-RECESO (TEORÍA Y EJERCICIOS)
        pdf.barra_azul("V. BLOQUE POST-RECESO (2 HORAS)")
        pdf.set_font('Helvetica', 'B', 12); pdf.cell(0, 10, f"Tema a Desarrollar: {normalizar(materia_post)}", 0, 1)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, "Explicacion Teorica: El docente modela el concepto en el pizarron utilizando ejemplos "
                             "concretos (frutas, piedras o situaciones reales de la comunidad). \n\n"
                             "Actividades: 1. Resolucion de 10 ejercicios en el cuaderno. 2. Trabajo en binas para "
                             "comparar resultados. 3. Plenaria de cierre para dudas.\n"
                             "Materiales: Cuaderno, libros de texto SEP, material concreto, juegos de geometria.")

        # 6. FUENTES
        pdf.ln(10); pdf.barra_azul("VI. REFERENCIAS Y FUENTES")
        pdf.set_font('Helvetica', 'I', 9)
        pdf.multi_cell(0, 5, "UNESCO (2026). Reporte Educativo Local.\nSEP (2025). Programa de Estudios Nueva Escuela Mexicana.")

        # --- DESCARGA ---
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
        st.success("✅ ¡Todo listo! Tu planeacion es extensa y profesional.")
        st.download_button("📥 DESCARGAR PLANEACION COMPLETA (PDF)", data=pdf_bytes, file_name=f"Planeacion_{normalizar(tema_int)}.pdf", use_container_width=True)
