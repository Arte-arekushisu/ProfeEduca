import streamlit as st
from fpdf import FPDF
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V1.6", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE CONTENIDO (ESTRUCTURA ABCD) ---
def generar_datos_plan(tema):
    return [
        {"campo": "Lenguajes", "nombre": "Estación 1: Aprendamos a Comer", 
         "mat": "Revistas, pegamento, tijeras, papel bond.",
         "ins": "Identificar alimentos y comunicarlos gráficamente.",
         "acts": ["1. Elaborar el Plato del Bien Comer con recortes.", "2. Clasificar 4 alimentos saludables y 4 no saludables.", "3. Explicar en el cuaderno por qué unos son mejores que otros."]},
        {"campo": "Saberes y Pensamiento Científico", "nombre": "Estación 2: Explorando la Nutrición", 
         "mat": "Balanza, frutas reales, semillas, cinta métrica.",
         "ins": "Analizar proporciones y medidas de los alimentos.",
         "acts": ["1. Pesar diferentes frutas y registrar los gramos.", "2. Medir el diámetro de 3 verduras distintas.", "3. Crear una gráfica de barras con los pesos obtenidos."]},
        {"campo": "Ética, Naturaleza y Sociedades", "nombre": "Estación 3: Guardianes del Entorno", 
         "mat": "Cartulina, gises, botes de basura etiquetados.",
         "ins": "Reflexionar sobre el impacto ambiental de lo que consumimos.",
         "acts": ["1. Separar residuos de alimentos en orgánicos e inorgánicos.", "2. Dibujar el ciclo de vida de una fruta local.", "3. Escribir un compromiso para no desperdiciar comida."]},
        {"campo": "De lo Humano y lo Comunitario", "nombre": "Estación 4: Cocina en Comunidad", 
         "mat": "Utensilios de plástico, ingredientes locales, música.",
         "ins": "Fomentar el trabajo en equipo y la identidad cultural.",
         "acts": ["1. Diseñar una receta comunitaria usando ingredientes de la zona.", "2. Juego de roles: 'El mercado del pueblo'.", "3. Compartir una historia familiar sobre su comida favorita."]}
    ]

# --- 3. CLASE PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16); self.cell(0, 10, 'PLANEACIÓN', 0, 1, 'C'); self.ln(5)
    def chapter(self, title):
        self.set_font('Arial', 'B', 11); self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', True); self.ln(2)

# --- 4. INTERFAZ ---
st.header("📋 Generador de Planeación ABCD")

with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", value="1")
        nombre_ed = st.text_input("Educador")
        nombre_eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema = st.text_input("Tema de Interés", placeholder="Ej. Tortugas Marinas")
        rincon = st.text_input("Rincón asignado")
    
    st.markdown("---")
    m1 = st.text_input("Materia Post-Receso 1", value="Educación Física")
    m2 = st.text_input("Materia Post-Receso 2", value="Suma de fracciones")
    
    btn_generar = st.form_submit_button("🔨 GENERAR Y REVISAR PLANEACIÓN")

if btn_generar:
    if not tema or not nombre_ed:
        st.error("⚠️ Falta el nombre del Educador o el Tema.")
    else:
        # --- CUENTA REGRESIVA ---
        placeholder = st.empty()
        for i in range(3, 0, -1):
            placeholder.metric("⏳ Procesando planeación extensa...", f"{i}s")
            time.sleep(1)
        placeholder.empty()

        estaciones = generar_datos_plan(tema)

        # --- VISTA PREVIA (SCREEN) ---
        st.success("### ✅ Planeación Generada")
        st.markdown(f"**Tema:** {tema.upper()} | **ECA:** {nombre_eca}")
        
        for est in estaciones:
            with st.expander(f"📍 {est['nombre']} ({est['campo']})", expanded=True):
                st.write(f"**Instrucciones:** {est['ins']}")
                st.write(f"**Materiales:** {est['mat']}")
                for a in est['acts']: st.write(f"  - {a}")

        # --- GENERACIÓN PDF ---
        pdf = PDF()
        pdf.add_page()
        pdf.chapter("I. DATOS DE IDENTIFICACIÓN")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 7, f"Educador: {nombre_ed} | ECA: {nombre_eca} | Nivel: {nivel} | Grado: {grado}", 0, 1)
        pdf.cell(0, 7, f"Comunidad: {comunidad} | Fecha: {fecha} | Rincón: {rincon}", 0, 1)

        pdf.chapter("II. ESTACIONES DE TRABAJO (4 CAMPOS)")
        for est in estaciones:
            pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, est['nombre'], 0, 1)
            pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, f"Instrucciones: {est['ins']}\nMateriales: {est['mat']}")
            for a in est['acts']: pdf.cell(5); pdf.cell(0, 5, a, 0, 1)
            pdf.ln(2)

        pdf.chapter(f"III. TUTOREO: {tema.upper()}")
        tutoreo_txt = (f"Tutor: '¿Sabías que existen dos tipos de tortugas: la marina y la terrestre?'\n"
                       f"Alumno: 'No profe...'\n"
                       f"Tutor: '¡Sí! Pero hoy nos enfocaremos en la MARINA. ¿Sabías que en México hay 7 especies?'\n"
                       f"(Nota: Dejamos la terrestre como misterio para fomentar la autonomía de investigación del niño).")
        pdf.multi_cell(0, 5, tutoreo_txt)

        pdf.chapter("IV. POST-RECESO")
        pdf.multi_cell(0, 6, f"1. {m1}\n2. {m2}")

        # --- BOTÓN DE DESCARGA ---
        pdf_out = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="📥 DESCARGAR PLANEACIÓN EN PDF",
            data=pdf_out,
            file_name=f"Planeacion_{tema}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
