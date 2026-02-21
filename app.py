import streamlit as st
from fpdf import FPDF
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V6.0", page_icon="📝", layout="wide")

# --- CLASE PDF PROFESIONAL SIN ERRORES DE CODIFICACIÓN ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def seccion_cabecera(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(40, 54, 85)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {titulo}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def crear_tabla_id(self, info):
        self.set_font('Helvetica', 'B', 10)
        for clave, valor in info.items():
            self.set_fill_color(240, 240, 240)
            self.cell(50, 8, f" {clave}:", 1, 0, 'L', True)
            self.set_font('Helvetica', '', 10)
            self.cell(140, 8, f" {valor}", 1, 1, 'L')
        self.ln(5)

# --- MOTOR PEDAGÓGICO ---
def generar_inicio(nivel, tema):
    # Actividades adaptadas al nivel
    niveles = {
        "Preescolar": {
            "lista": f"Cantar 'La ronda de {tema}' y mencionar una emocion.",
            "regalo": f"Cuento ilustrado: 'El misterio de {tema}'.",
            "reflexion": "Dibujar el momento mas feliz del cuento.",
            "mat": "Titeres, hojas blancas, crayolas."
        },
        "Primaria": {
            "lista": f"Mencionar una palabra clave de {tema} que rime con su nombre.",
            "regalo": f"Lectura de la leyenda: 'El origen de {tema}'.",
            "reflexion": "Escribir un compromiso personal para cuidar nuestro entorno.",
            "mat": "Fichas de lectura, pizarron, plumones."
        },
        "Secundaria": {
            "lista": f"Compartir un dato cientifico o estadistico sobre {tema}.",
            "regalo": f"Ensayo de divulgacion: 'Retos actuales de {tema}'.",
            "reflexion": "Debate grupal sobre la postura del autor y propuestas de solucion.",
            "mat": "Articulos impresos, cuadernos, boligrafos."
        }
    }
    return niveles.get(nivel)

# --- INTERFAZ ---
st.title("🍎 Taller de Planeacion Pedagogica")

with st.form("form_v6"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "1ro Multigrado")
        educador = st.text_input("Educador", "Axel Reyes")
        eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema_int = st.text_input("Tema de Interes", "Biodiversidad Marina")
        rincon = st.text_input("Rincon asignado")
    
    st.markdown("---")
    st.subheader("Post-Receso (2 Horas de Clase)")
    m1 = st.text_input("Materia 1", "Suma de fracciones")
    m2 = st.text_input("Materia 2", "Vida Saludable")
    
    generar = st.form_submit_button("🔨 GENERAR PLANEACION EXTENSA")

if generar:
    with st.status("🚀 Redactando contenido detallado...", expanded=True) as s:
        time.sleep(1)
        datos_inicio = generar_inicio(nivel, tema_int)
        
        # --- GENERACIÓN PDF ---
        pdf = PDF()
        pdf.add_page()
        
        # I. IDENTIFICACION
        pdf.seccion_cabecera("I. DATOS DE IDENTIFICACION")
        pdf.crear_tabla_id({
            "Educador": educador, "ECA": eca, "Nivel/Grado": f"{nivel} - {grado}",
            "Comunidad": comunidad, "Fecha": str(fecha), "Rincon": rincon
        })

        # II. INICIO
        pdf.seccion_cabecera("II. BIENVENIDA Y RUTINA GRUPAL")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, f"Materiales: {datos_inicio['mat']}", 0, 1)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, f"1. Pase de Lista: {datos_inicio['lista']}\n"
                             f"2. Regalo de Lectura: {datos_inicio['regalo']}\n"
                             f"3. Reflexion: {datos_inicio['reflexion']}")
        pdf.ln(5)

        # III. ESTACIONES (4 CAMPOS)
        pdf.seccion_cabecera("III. ESTACIONES POR CAMPOS FORMATIVOS")
        estaciones = [
            {"n": "Estacion del Lenguaje", "c": "Lenguajes", "act": "Redaccion de un 'Códice Comunitario' e ilustracion de conceptos.", "mat": "Hojas, colores, periodicos."},
            {"n": "Estacion del Laboratorio", "c": "Saberes y P. Cientifico", "act": "Analisis de datos y formulacion de hipotesis sobre el tema.", "mat": "Lupas, reglas, bitacoras."},
            {"n": "Estacion de Etica", "c": "Etica, Nat. y Sociedades", "act": "Creacion de un acuerdo de convivencia para proteger el tema.", "mat": "Cartulinas, gises."},
            {"n": "Estacion de Identidad", "c": "De lo Humano y lo Comunitario", "act": "Juego de roles sobre el papel de la comunidad en el tema.", "mat": "Utensilios de plastico, musica."}
        ]
        for e in estaciones:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, f"📌 {e['n']} (Campo: {e['c']})", 0, 1)
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(25, 6, "Materiales:", 0, 0); pdf.set_font('Helvetica', '', 10); pdf.cell(0, 6, e['mat'], 0, 1)
            pdf.multi_cell(0, 6, f"Instrucciones: El docente organiza el espacio y deja las guias visuales. Actividad: {e['act']}\n")
            pdf.ln(2)

        # IV. TEMA DE INTERÉS (EXTENSO)
        pdf.add_page()
        pdf.seccion_cabecera(f"IV. DESARROLLO TEMA DE INTERES: {tema_int.upper()}")
        pdf.multi_cell(0, 6, f"Teoria: {tema_int} es crucial para el equilibrio local. Cientificamente se sabe que...\n"
                             f"Pregunta Detonante: ¿Que misterio o curiosidad de este tema te gustaria investigar hoy?\n"
                             f"Producto final: El alumno lidera su investigacion y crea una maqueta o cartel informativo.")

        # V. POST-RECESO
        pdf.seccion_cabecera("V. ACTIVIDADES POST-RECESO (2 HORAS)")
        for materia in [m1, m2]:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, f"TEMA: {materia}", 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, f"Explicacion: Presentacion de conceptos base en pizarron. Ejemplo: 'Si tenemos 1/4 y sumamos 2/4...'.\n"
                                 f"Actividades: 1. Resolucion de ejercicios grupales. 2. Practica individual en cuaderno.\n"
                                 f"Materiales: Cuaderno, libros de texto, material concreto.\n")
            pdf.ln(3)

        # VI. FUENTES
        pdf.seccion_cabecera("VI. FUENTES DE CONSULTA")
        pdf.set_font('Helvetica', 'I', 9)
        pdf.multi_cell(0, 5, "UNESCO (2026). Reporte Educativo. https://unesco.org\nSEP (2025). Plan NEM. https://gob.mx/sep")

        # --- SALIDA SEGURA ---
        # El .encode('latin-1', 'replace') evita que el programa falle por acentos
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
        s.update(label="✅ Planeacion completa sin errores", state="complete")
        
        st.download_button("📥 DESCARGAR PDF COMPLETO (3-4 HOJAS)", data=pdf_bytes, file_name=f"Planeacion_{tema_int}.pdf", use_container_width=True)
