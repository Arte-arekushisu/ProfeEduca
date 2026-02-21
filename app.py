import streamlit as st
from fpdf import FPDF
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V5.0", page_icon="📚", layout="wide")

# --- CLASE PDF PROFESIONAL BLINDADA ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 22)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def seccion_azul(self, texto):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {texto}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def tabla_datos(self, info):
        self.set_font('Arial', 'B', 10)
        for clave, valor in info.items():
            self.set_fill_color(245, 245, 245)
            self.cell(50, 8, f" {clave}:", 1, 0, 'L', True)
            self.set_font('Arial', '', 10)
            self.cell(140, 8, f" {valor}", 1, 1, 'L')
        self.ln(5)

# --- MOTOR DE LÓGICA PEDAGÓGICA ---
def obtener_dinamicas(nivel, tema):
    if nivel == "Preescolar":
        return {
            "pase": f"Cada nino imita un animal que viva cerca de donde hay {tema}.",
            "regalo": f"Cuento motor: 'El viaje magico hacia {tema}'.",
            "reflexion": "Dialogo sobre que partes del cuento nos hicieron sentir alegres."
        }
    elif nivel == "Primaria":
        return {
            "pase": f"Mencionar una cualidad de {tema} que empiece con su inicial.",
            "regalo": f"Lectura de una infografia sobre {tema} y sus beneficios.",
            "reflexion": "Escribir en una frase por que debemos cuidar {tema}."
        }
    else: # Secundaria
        return {
            "pase": f"Mencionar un dato estadistico o cientifico sobre {tema}.",
            "regalo": f"Ensayo de divulgacion: 'Perspectivas actuales sobre {tema}'.",
            "reflexion": "Debate: Impacto socioeconomico de {tema} en nuestra comunidad."
        }

# --- INTERFAZ ---
st.title("🍎 Generador de Planeacion ABCD")

with st.form("maestro_form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "1ro Multigrado")
        educador = st.text_input("Nombre del Educador")
        eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema = st.text_input("Tema de Interes", placeholder="Ej. El Ciclo del Agua")
        rincon = st.text_input("Rincon Asignado")
    
    st.markdown("---")
    st.subheader("Bloque Post-Receso (Desarrollo Completo)")
    m1_tit = st.text_input("Materia/Tema 1", "Suma de fracciones")
    m2_tit = st.text_input("Materia/Tema 2", "Vida Saludable")
    
    boton_gen = st.form_submit_button("🔨 GENERAR Y REVISAR PLANEACION")

if boton_gen:
    status = st.status("🚀 Redactando guia profesional...", expanded=True)
    time.sleep(1)
    
    din = obtener_dinamicas(nivel, tema)
    
    # --- CONSTRUCCIÓN DEL PDF ---
    pdf = PDF()
    pdf.add_page()
    
    # I. DATOS
    pdf.seccion_azul("I. DATOS DE IDENTIFICACION")
    pdf.tabla_datos({
        "Educador": educador, "ECA": eca, "Nivel y Grado": f"{nivel} - {grado}",
        "Comunidad": comunidad, "Fecha": str(fecha), "Rincon": rincon
    })

    # II. INICIO
    pdf.seccion_azul("II. MOMENTO DE INICIO Y BIENVENIDA")
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 7, "Materiales: Libros del rincon, gises, bitacora grupal.", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, f"1. Pase de Lista: {din['pase']}\n"
                         f"2. Regalo de Lectura: {din['regalo']}\n"
                         f"3. Reflexion del Cuento: {din['reflexion']}")
    pdf.ln(5)

    # III. ESTACIONES (4 CAMPOS)
    pdf.seccion_azul("III. ESTACIONES DE APRENDIZAJE INTEGRAL")
    est_list = [
        {"nom": "Estacion del Investigador", "inst": "Los alumnos analizan muestras y datos.", "mat": "Lupas, frascos, fichas de registro."},
        {"nom": "Estacion de la Palabra", "inst": "Creacion de un mural informativo.", "mat": "Cartulinas, recortes, pegamento."},
        {"nom": "Estacion del Ciudadano", "inst": "Simulacion de resolucion de problemas comunitarios.", "mat": "Hojas de colores, plumones."},
        {"nom": "Estacion Creativa", "inst": "Modelado de prototipos sobre el tema.", "mat": "Plastilina, materiales de reuso."}
    ]
    for e in est_list:
        pdf.set_font('Arial', 'B', 11); pdf.cell(0, 7, f"📌 {e['nom']}", 0, 1)
        pdf.set_font('Arial', 'I', 10); pdf.multi_cell(0, 5, f"Materiales: {e['mat']}")
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, f"Instrucciones: {e['inst']} Esta estacion integra actividades de Lenguajes, Saberes, Etica y lo Humano mediante la colaboracion y el registro visual.\n")
        pdf.ln(2)

    # IV. TEMA DE INTERÉS (EXTENSO)
    pdf.add_page()
    pdf.seccion_azul(f"IV. DESARROLLO DEL TEMA: {tema.upper()}")
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, f"El tema de {tema} es central para entender nuestra realidad. Segun la UNESCO, este tipo de aprendizajes "
                         f"fomenta la conciencia critica. \n\nInformacion Clave: Aqui se explica que {tema} funciona bajo principios de... \n"
                         f"Pregunta Detonante: ¿Como cambiaria tu vida si {tema} no existiera?\n"
                         f"Actividad: Realizar un mapa mental gigante en el suelo usando carbon o gises.")

    # V. POST-RECESO (TEORÍA Y EJERCICIOS)
    pdf.seccion_azul("V. BLOQUE POST-RECESO (2 HORAS)")
    for m in [m1_tit, m2_tit]:
        pdf.set_font('Arial', 'B', 11); pdf.cell(0, 7, f"TEMA: {m}", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, f"Teoria: Para entender {m} debemos aplicar el razonamiento logico. Por ejemplo, en el caso de {m}, "
                             "se procede a realizar el siguiente algoritmo... \n"
                             "Ejemplo Práctico: 2 + 2 = 4 aplicado a situaciones de la vida diaria.\n"
                             "Ejercicios: Realizar 5 practicas individuales y una puesta en comun grupal.\n"
                             "Materiales: Cuaderno, lapiz, regla, pizarron.")
        pdf.ln(3)

    # VI. FUENTES
    pdf.ln(5); pdf.seccion_azul("VI. FUENTES DE CONSULTA")
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, "1. SEP (2026) Plan de Estudios NEM. https://sep.gob.mx\n2. UNESCO - Guias de Aprendizaje Activo.\n3. Redalyc - Investigaciones Educativas.")

    # --- DESCARGA SEGURA ---
    # Limpiamos caracteres que no sean latin-1 para evitar errores
    pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
    status.update(label="✅ Planeacion completa generada exitosamente", state="complete")
    
    st.download_button(
        label="📥 DESCARGAR PLANEACION COMPLETA (PDF)",
        data=pdf_output,
        file_name=f"Planeacion_{tema}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
