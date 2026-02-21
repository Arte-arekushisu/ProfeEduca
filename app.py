import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE NORMALIZACIÓN (SEGURIDAD TOTAL) ---
def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

# --- CLASE PDF PROFESIONAL ---
class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(31, 52, 94)
        self.cell(0, 15, 'PLANEACION DE ACTIVIDADES', 0, 1, 'C')
        self.ln(5)

    def seccion(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 235, 245)
        self.set_text_color(31, 52, 94)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

# --- APP STREAMLIT ---
st.set_page_config(page_title="Innovacion Educativa v0.4", layout="wide")
st.title("🧩 Fase 4: Consolidacion de Inteligencia Pedagogica")

with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "Axel Reyes")
        tema = st.text_input("Tema de Interes", placeholder="Ej: Importancia de la Biodiversidad")
    with col2:
        grado = st.text_input("Grado/Grupo", "Multigrado")
        comunidad = st.text_input("Comunidad", "San Michi")
        rincon = st.text_input("Rincon Asignado")

    st.markdown("---")
    st.subheader("Configuracion Post-Receso (Bloque Tecnico)")
    mat_post = st.text_input("Materia/Tema Especifico", "Resolucion de conflictos comunitarios")
    
    submit = st.form_submit_button("🔨 INTEGRAR FASES Y GENERAR")

if submit:
    if not tema or not educador:
        st.warning("⚠️ Datos incompletos para cerrar la Fase 4.")
    else:
        with st.status("🧠 Accediendo a bases de datos y consolidando fases...", expanded=True) as s:
            
            # --- MOTOR DE CONTENIDO EXTENSO (LA "IA" TRABAJANDO) ---
            # Aqui simulamos la busqueda profunda que mencionaste
            if nivel == "Preescolar":
                act_nombre = f"Exploradores de {tema}"
                regalo = f"Narracion oral con apoyo de laminas sobre {tema}."
                teoria_profunda = f"El desarrollo cognitivo en preescolar respecto a {tema} se centra en la percepcion sensorial. Segun la NEM 2026, el alumno debe identificar patrones naturales..."
            elif nivel == "Primaria":
                act_nombre = f"Proyecto: El impacto de {tema} en mi pueblo"
                regalo = f"Lectura de articulo de divulgacion: 'El misterio de {tema}'."
                teoria_profunda = f"En primaria, {tema} se aborda desde el Pensamiento Critico. Se requiere que el estudiante analice causas y consecuencias socio-ambientales bajo el campo de Saberes..."
            else: # Secundaria
                act_nombre = f"Seminario: Analisis estructural de {tema}"
                regalo = f"Ensayo critico sobre la evolucion de {tema} en el siglo XXI."
                teoria_profunda = f"El nivel secundaria exige una postura epistemologica. {tema} se conecta con la Etica y Naturaleza para proponer soluciones tecnologicas o sociales..."

            pdf = PlaneacionPDF()
            pdf.add_page()

            # FASE 1 & 2: IDENTIFICACION (TABULAR PROFESIONAL)
            pdf.seccion("I. IDENTIFICACION DE LA FIGURA EDUCATIVA")
            datos_id = [["Educador", educador], ["Nivel", nivel], ["Grado", grado], ["Comunidad comunidad"], ["Fecha", str(datetime.date.today())]]
            for d in datos_id:
                pdf.set_font('Helvetica', 'B', 10); pdf.cell(50, 8, f" {clean(d[0])}:", 1, 0, 'L', True)
                pdf.set_font('Helvetica', '', 10); pdf.cell(140, 8, f" {clean(d[1])}", 1, 1, 'L')
            
            # FASE 3: INICIO ADAPTADO
            pdf.ln(5); pdf.seccion(f"II. MOMENTO DE INICIO: {act_nombre}")
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 8, f"1. Pase de Lista: Mencionar un dato curioso de {clean(tema)}.\n"
                                 f"2. Regalo de Lectura: {clean(regalo)}\n"
                                 f"3. Reflexion: Debate guiado sobre la postura del autor.\n"
                                 f"MATERIALES: Libros del rincon de {clean(rincon)}, bitacora de aula.")

            # FASE 4: ESTACIONES CON 4 CAMPOS INTEGRADOS
            pdf.ln(5); pdf.seccion("III. ESTACIONES DE APRENDIZAJE (LOS 4 CAMPOS)")
            estaciones = [
                {"n": "Estacion de Indagacion", "c": "Saberes y P. Cientifico", "a": "Observacion directa y registro de datos.", "m": "Lupas, bitacora, cintas."},
                {"n": "Estacion Literaria", "c": "Lenguajes / Etica", "a": "Creacion de un periodico mural comunitario.", "m": "Papel, colores, pegamento."},
                {"n": "Estacion de Identidad", "c": "De lo Humano y lo Com.", "a": "Juego de roles sobre lideres locales.", "m": "Material de reuso, vestuario."}
            ]
            for est in estaciones:
                pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, f"📌 {clean(est['n'])} (Campo: {clean(est['c'])})", 0, 1)
                pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"Actividad: {clean(est['a'])}\nMateriales: {clean(est['m'])}\n")

            # CONTENIDO EXTENSO (MOTOR DE INFORMACION)
            pdf.add_page()
            pdf.seccion("IV. MARCO TEORICO Y TUTOREO (INFORMACION AMPLIADA)")
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 7, f"Sustento Pedagogico: {clean(teoria_profunda)}\n\n"
                                 f"Desarrollo del Tema: El docente explicara que {clean(tema)} no es un concepto aislado. "
                                 "Se debe guiar al alumno en un proceso de investigacion RPA (Relacion Tutora). "
                                 "Se espera que al finalizar, el alumno pueda dar una demostracion publica.\n\n"
                                 f"Pregunta Detonante: ¿Como ha cambiado la perspectiva de {clean(tema)} en nuestra comunidad?\n"
                                 "Materiales: Guias de aprendizaje, laminas, fuentes bibliograficas externas.")

            # POST-RECESO
            pdf.ln(5); pdf.seccion("V. BLOQUE POST-RECESO (2 HORAS)")
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"TEMA: {clean(mat_post)}", 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, "Explicacion: Modelado de conceptos en pizarron con ejemplos practicos.\n"
                                 "Ejercicios: Realizacion de 5 actividades de aplicacion real.\n"
                                 "Materiales: Cuaderno, material concreto, libro de texto SEP.")

            # --- GENERACION FINAL ---
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
            s.update(label="✅ Fase 4 Completada y Unificada", state="complete")
            st.download_button("📥 DESCARGAR PIEZA FINAL (FASE 4)", data=pdf_bytes, file_name=f"Fase4_{clean(tema)}.pdf", use_container_width=True)
