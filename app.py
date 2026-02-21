import streamlit as st
from fpdf import FPDF
import time

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(page_title="ProfeEduca V7.0", page_icon="🍎", layout="wide")

# --- CLASE PDF BLINDADA (SIN ACENTOS PARA EVITAR ERRORES) ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def titulo_tabla(self, texto):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(40, 54, 85)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {texto}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def tabla_identificacion(self, info):
        self.set_font('Helvetica', 'B', 10)
        for clave, valor in info.items():
            self.set_fill_color(240, 240, 240)
            self.cell(50, 8, f" {clave}:", 1, 0, 'L', True)
            self.set_font('Helvetica', '', 10)
            self.cell(140, 8, f" {valor}", 1, 1, 'L')
        self.ln(5)

# --- LOGICA PEDAGOGICA ADAPTATIVA ---
def configurar_inicio(nivel, tema):
    if nivel == "Preescolar":
        return {
            "pase": f"Mencionar un animal que les recuerde a {tema}.",
            "regalo": f"Cuento infantil corto sobre {tema} con apoyo visual.",
            "reflexion": "Dibujo rapido: ¿Que parte del cuento te hizo sonreir?",
            "materiales": "Titeres, hojas blancas, crayolas."
        }
    elif nivel == "Primaria":
        return {
            "pase": f"Decir un dato curioso de {tema} que hayan visto en casa.",
            "regalo": f"Lectura de una leyenda o fabula relacionada con {tema}.",
            "reflexion": "Circulo de dialogo: ¿Cual es la ensenanza principal?",
            "materiales": "Libro de texto, plumones, tarjetas de colores."
        }
    else: # Secundaria
        return {
            "pase": f"Mencionar un dato cientifico o estadistico de {tema}.",
            "regalo": f"Ensayo corto de divulgacion cientifica sobre {tema}.",
            "reflexion": "Debate rapido: ¿Cual es la postura del autor ante el problema?",
            "materiales": "Articulos impresos, cuadernos, boligrafos."
        }

# --- INTERFAZ DE USUARIO ---
st.title("📝 Generador de Planeacion Profesional")
st.markdown("---")

with st.form("planeacion_form"):
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "1ro Multigrado")
        educador = st.text_input("Nombre del Educador")
        eca = st.text_input("Nombre del ECA")
    with col2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema_interes = st.text_input("Tema de Interes (Ej. Las Abejas)")
        rincon = st.text_input("Rincon Asignado")
    
    st.subheader("Bloque Post-Receso (2 Horas)")
    mat1 = st.text_input("Materia/Tema 1", "Fracciones")
    mat2 = st.text_input("Materia/Tema 2", "Cuidado del Agua")
    
    enviar = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA")

if enviar:
    with st.status("🚀 Redactando documento detallado...", expanded=True) as s:
        time.sleep(1)
        ini = configurar_inicio(nivel, tema_interes)
        
        pdf = PDF()
        pdf.add_page()
        
        # 1. IDENTIFICACION
        pdf.titulo_tabla("I. DATOS DE IDENTIFICACION")
        pdf.tabla_identificacion({
            "Educador": educador, "ECA": eca, "Nivel y Grado": f"{nivel} - {grado}",
            "Comunidad": comunidad, "Fecha": str(fecha), "Rincon": rincon
        })

        # 2. INICIO Y RUTINA
        pdf.titulo_tabla("II. INICIO Y RUTINA GRUPAL")
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, f"Materiales: {ini['materiales']}", 0, 1)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 8, f"1. Pase de lista: {ini['pase']}\n"
                             f"2. Regalo de lectura: {ini['regalo']}\n"
                             f"3. Reflexion: {ini['reflexion']}")
        pdf.ln(5)

        # 3. ESTACIONES (INTEGRANDO LOS 4 CAMPOS)
        pdf.titulo_tabla("III. ESTACIONES DE TRABAJO (4 CAMPOS FORMATIVOS)")
        estaciones = [
            {"nombre": "Estacion del Investigador", "campo": "Saberes y P. Cientifico", "act": "Analisis de datos y observacion directa del tema.", "mat": "Lupas, bitacoras, reglas."},
            {"nombre": "Estacion de las Palabras", "campo": "Lenguajes", "act": "Creacion de un glosario ilustrado y narrativas.", "mat": "Papel bond, colores, revistas."},
            {"nombre": "Estacion de la Comunidad", "campo": "De lo Humano y lo Com.", "act": "Juego de roles y acuerdos de convivencia.", "mat": "Material reciclado, pegamento."},
            {"nombre": "Estacion de Guardianes", "campo": "Etica, Nat. y Soc.", "act": "Propuesta de acciones para proteger el entorno.", "mat": "Cartulinas, marcadores."}
        ]
        for est in estaciones:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, f"📌 {est['nombre']}", 0, 1)
            pdf.set_font('Helvetica', 'I', 10); pdf.cell(0, 6, f"Campo Formativo: {est['campo']}", 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 5, f"Materiales: {est['mat']}\nInstrucciones: Los alumnos realizaran: {est['act']} buscando siempre la autonomia.\n")
            pdf.ln(2)

        # 4. TEMA DE INTERES EXTENSO
        pdf.add_page()
        pdf.titulo_tabla(f"IV. DESARROLLO DEL TEMA: {tema_interes.upper()}")
        pdf.set_font('Helvetica', '', 11)
        contenido_tema = (f"El tema de {tema_interes} es fundamental para el desarrollo del pensamiento critico. "
                          f"Desde el punto de vista cientifico, se aborda bajo la premisa de la interconectividad. \n\n"
                          f"Informacion para el Maestro: Se debe enfatizar en como {tema_interes} impacta en la comunidad de {comunidad}. \n"
                          f"Pregunta Detonante: ¿Que pasaria en nuestro futuro si no comprendemos el valor de este tema hoy?\n"
                          f"Materiales Sugeridos: Laminas educativas, proyector (si hay disponible), rincon de lectura.")
        pdf.multi_cell(0, 7, contenido_tema)
        pdf.ln(5)

        # 5. POST-RECESO (TEORIA Y EJEMPLOS)
        pdf.titulo_tabla("V. ACTIVIDADES POST-RECESO (DESARROLLO EXHAUSTIVO)")
        for m in [mat1, mat2]:
            pdf.set_font('Helvetica', 'B', 12); pdf.cell(0, 8, f"Tema: {m}", 0, 1)
            pdf.set_font('Helvetica', '', 10)
            teoria = (f"Teoria: Para abordar {m}, iniciaremos con una explicacion de los conceptos base en el pizarron. \n"
                      f"Ejemplo: Si estamos viendo {m}, aplicaremos un caso real (ej. el uso de medidas en la cocina local). \n"
                      f"Actividades: 1. Ejercicios practicos en el cuaderno. 2. Resolucion de dudas grupal.\n"
                      f"Materiales: Cuaderno del alumno, pizarron, libros de texto de la SEP.")
            pdf.multi_cell(0, 6, teoria)
            pdf.ln(4)

        # 6. FUENTES
        pdf.titulo_tabla("VI. REFERENCIAS BIBLIOGRAFICAS")
        pdf.set_font('Helvetica', 'I', 9)
        pdf.multi_cell(0, 5, "1. SEP (2026). Plan de Estudios Nueva Escuela Mexicana.\n2. UNESCO (2025). Guias para el Aprendizaje Activo.\n3. National Geographic Educacion.")

        # --- GENERACION FINAL ---
        # El .encode('latin-1', 'replace') es el truco final que evita que el PDF falle por acentos
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
        s.update(label="✅ Planeacion finalizada con exito", state="complete")
        
        st.download_button(
            label="📥 DESCARGAR PLANEACION COMPLETA (PDF)",
            data=pdf_bytes,
            file_name=f"Planeacion_{tema_interes}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
