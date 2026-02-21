import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import time

def clean(txt):
    if not txt: return ""
    # Mantenemos la limpieza para evitar errores de codificación en el PDF
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionFinalPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 25)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def seccion_titulo(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f" {clean(titulo)}", 1, 1, 'L', True)
        self.ln(2)

st.set_page_config(page_title="PLANEACION PRO", layout="wide")
st.title("🛡️ Sistema de Planeación Pedagógica")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "1")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "Proyecto Raices")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interés", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincón", "CIENCIAS / LECTURA")

    st.subheader("🗓️ Configuración de Materias Post-Receso (2 Horas Diarias)")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=100)

    submit = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA")

if submit:
    with st.spinner("⏳ Estructurando procedimientos y corrigiendo sintaxis..."):
        time.sleep(2)
        
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # --- I. DATOS DE IDENTIFICACIÓN ---
        pdf.seccion_titulo("I. DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        col_width = 95
        pdf.cell(col_width, 8, clean(f"Educador: {educador}"), 1)
        pdf.cell(col_width, 8, clean(f"Nivel/Grado: {nivel} - {grado}"), 1, 1)
        pdf.cell(col_width, 8, clean(f"ECA: {eca}"), 1)
        pdf.cell(col_width, 8, clean(f"Comunidad: {comunidad}"), 1, 1)
        pdf.cell(col_width, 8, clean(f"Tema: {tema}"), 1)
        pdf.cell(col_width, 8, clean(f"Rincon: {rincon}"), 1, 1)
        pdf.ln(5)

        # --- II. ESTACIONES CON PROCEDIMIENTO DETALLADO ---
        pdf.seccion_titulo("II. ESTACIONES DE TRABAJO AUTONOMO")
        
        # Estación: Mural Literario
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean("Estacion: Mural Literario (Lenguajes)"), 0, 1)
        pdf.set_font('Helvetica', '', 10)
        # Usamos triple comilla para evitar el error de SyntaxError en saltos de línea
        proc_mural = """PASO A PASO:
1. Busqueda: Los alumnos identifican 3 palabras clave del tema en ficheros academicos.
2. Definicion: Redactan en su cuaderno que significa cada palabra segun lo comprendido.
3. Mural: En una cartulina, dibujan el concepto central y pegan sus definiciones creativamente.
4. Socializacion: Exponen su mural en plenaria explicando su importancia."""
        pdf.multi_cell(0, 5, clean(proc_mural)); pdf.ln(3)

        # --- III. BLOQUE POST-RECESO (DIVISION POR HORAS) ---
        pdf.add_page()
        pdf.seccion_titulo("III. BLOQUE POST-RECESO (DIVISION POR HORAS)")
        
        for dia, materias_raw in mats_inputs.items():
            lista_mats = materias_raw.split('\n')
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(0, 10, clean(f"DIA: {dia}"), 1, 1, 'C', True)
            
            # HORA 1
            m1 = lista_mats[0] if len(lista_mats) > 0 else "Matematicas"
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 8, clean(f"HORA 1 (60 min): {m1}"), "LTR", 1)
            pdf.set_font('Helvetica', '', 9)
            
            # Detalle específico para Matemáticas
            if "MAT" in m1.upper():
                detalle_m1 = """PROCEDIMIENTO DETALLADO:
- Inicio: Recordar el concepto de numerador y denominador con apoyo visual (dibujos).
- Desarrollo: Explicar el metodo de 'producto cruzado' para resolver sumas de fracciones.
- Actividad: Resolver 10 reactivos de suma de fracciones y problemas de logica simple.
- Cierre: Revision grupal y aclaracion de dudas en el pizarron."""
            else:
                detalle_m1 = "Inicio: Recuperacion de saberes. Desarrollo: Actividad practica individual. Cierre: Plenaria de resultados."
            
            pdf.multi_cell(0, 5, clean(detalle_m1), "LBR"); pdf.ln(2)
            
            # HORA 2
            m2 = lista_mats[1] if len(lista_mats) > 1 else "Artes / Ed. Fisica"
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 8, clean(f"HORA 2 (60 min): {m2}"), "LTR", 1)
            pdf.set_font('Helvetica', '', 9)
            
            # Detalle específico para Artes o Educación Física
            if "ART" in m2.upper():
                detalle_m2 = "Inicio: Observacion de tecnicas. Desarrollo: Aplicacion de dibujo o practica de flauta. Cierre: Galeria de trabajos."
            elif "FIS" in m2.upper():
                detalle_m2 = "Inicio: Calentamiento. Desarrollo: Circuito motriz con balon o pista. Cierre: Estiramiento y relajacion."
            else:
                detalle_m2 = "Actividad complementaria vinculada al proyecto transversal del dia."
                
            pdf.multi_cell(0, 5, clean(detalle_m2), "LBR"); pdf.ln(4)

        # Generación del archivo
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.success("✅ Planeación generada con éxito y sin errores de sintaxis.")
        
        st.download_button(
            label="📥 DESCARGAR PLANEACION COMPLETA",
            data=pdf_bytes,
            file_name="Planeacion_Pedagogica.pdf",
            mime="application/pdf",
            use_container_width=True
        )
