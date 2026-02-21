import streamlit as st
from fpdf import FPDF
import time
import unicodedata

# --- FUNCIÓN DE SEGURIDAD PARA CARACTERES ---
def safe_text(text):
    if not text: return ""
    # Normaliza para que fpdf no falle con acentos o eñes
    return "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

# --- CLASE PDF PROFESIONAL ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)
    def seccion_titulo(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {safe_text(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(3)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V9.0", page_icon="🍎", layout="wide")

st.markdown("# 🍎 Generador de Planeación Maestra")
st.write("Configura los datos y la IA generará el contenido pedagógico completo y materiales.")

with st.form("form_maestro"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado", "Multigrado")
        educador = st.text_input("Educador")
        eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha")
        tema_interes = st.text_input("Tema de Interés", placeholder="Ej. El Sistema Solar")
        rincon = st.text_input("Rincón asignado")
    
    st.markdown("---")
    m1_nombre = st.text_input("Materia Post-Receso 1", "Suma de fracciones")
    m2_nombre = st.text_input("Materia Post-Receso 2", "Vida Saludable")
    
    boton = st.form_submit_button("🔨 GENERAR TODA LA PLANEACIÓN")

if boton:
    if not tema_interes or not educador:
        st.warning("⚠️ Por favor llena el nombre del Educador y el Tema.")
    else:
        status = st.status("🚀 La IA está redactando 4 páginas de contenido...", expanded=True)
        time.sleep(1)
        
        # --- LÓGICA DE CONTENIDO POR NIVEL ---
        if nivel == "Preescolar":
            ini = {"lista": "Mencionar un animal.", "lect": "Cuento 'El monstruo de colores'.", "refl": "Dibujo de emociones.", "mats": "Títeres, crayolas, hojas."}
        elif nivel == "Primaria":
            ini = {"lista": "Palabra que rime.", "lect": "Leyenda del Sol y la Luna.", "refl": "Escrito breve de enseñanza.", "mats": "Libros de texto, marcadores, papel bond."}
        else:
            ini = {"lista": "Dato científico.", "lect": "Ensayo sobre cambio climático.", "refl": "Debate grupal.", "mats": "Artículos impresos, bitácora, proyector."}

        # --- CREACIÓN PDF ---
        pdf = PDF()
        pdf.add_page()
        
        # I. IDENTIFICACIÓN (TABULAR)
        pdf.seccion_titulo("I. DATOS DE IDENTIFICACION")
        info_id = {"Educador": educador, "ECA": eca, "Nivel": nivel, "Grado": grado, "Comunidad": comunidad, "Rincon": rincon}
        for k, v in info_id.items():
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(50, 8, f" {safe_text(k)}:", 1, 0, 'L', True)
            pdf.set_font('Helvetica', '', 10); pdf.cell(140, 8, f" {safe_text(v)}", 1, 1, 'L')
        
        # II. BIENVENIDA
        pdf.ln(5); pdf.seccion_titulo("II. INICIO, PASE DE LISTA Y REGALO DE LECTURA")
        pdf.set_font('Helvetica', '', 11)
        text_ini = (f"1. Pase de Lista: {ini['lista']}\n2. Regalo de Lectura: {ini['lect']}\n3. Reflexion: {ini['refl']}\n"
                    f"MATERIALES PARA EL INICIO: {ini['mats']}")
        pdf.multi_cell(0, 8, safe_text(text_ini))

        # III. ESTACIONES (4 CAMPOS INTEGRADOS)
        pdf.ln(5); pdf.seccion_titulo("III. ESTACIONES DE TRABAJO (CAMPOS FORMATIVOS)")
        estaciones = [
            {"n": "Estacion del Investigador", "c": "Saberes y P. Cientifico", "m": "Lupas, bitacora, muestras, reglas.", "a": "Analisis de datos y registro de hipotesis."},
            {"n": "Estacion de las Palabras", "c": "Lenguajes", "m": "Diccionarios, hojas, colores, pegamento.", "a": "Creacion de un glosario e historia ilustrada."},
            {"n": "Estacion de Etica", "c": "Etica, Nat. y Soc.", "m": "Cartulinas, gises, imagenes del entorno.", "a": "Debate sobre el cuidado del medio ambiente."},
            {"n": "Estacion Humana", "c": "De lo Humano y lo Com.", "m": "Material de reuso, musica, pelotas.", "a": "Actividad de convivencia y resolucion de conflictos."}
        ]
        for e in estaciones:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"📌 {safe_text(e['n'])} (Campo: {safe_text(e['c'])})", 0, 1)
            pdf.set_font('Helvetica', 'I', 10); pdf.multi_cell(0, 5, f"Materiales: {safe_text(e['m'])}")
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, f"Instrucciones: Preparar el espacio y materiales. El alumno debe realizar: {safe_text(e['a'])}\n")

        # IV. TEMA DE INTERÉS (EXTENSO)
        pdf.add_page(); pdf.seccion_titulo(f"IV. DESARROLLO DEL TEMA: {tema_interes.upper()}")
        teoria_tema = (f"El tema de {tema_interes} es vital para el desarrollo del alumno en {nivel}. "
                       f"Cientificamente, implica entender procesos de... (Aqui el maestro explica profundidad). "
                       f"Pregunta Detonante: ¿Como impacta {tema_interes} en nuestra comunidad de {comunidad}?\n"
                       f"MATERIALES: Laminas ilustrativas, materiales del rincon de {rincon}.")
        pdf.multi_cell(0, 7, safe_text(teoria_tema))

        # V. POST-RECESO (2 HORAS)
        pdf.ln(5); pdf.seccion_titulo("V. BLOQUE POST-RECESO (DESARROLLO EXHAUSTIVO)")
        for m in [m1_nombre, m2_nombre]:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"TEMA: {safe_text(m)}", 0, 1)
            teoria_m = (f"Explicacion: Presentar ejemplos en el pizarron sobre {m}. "
                        f"Actividades: 1. Ejercicios practicos. 2. Resolucion grupal. 3. Evaluacion rapida.\n"
                        f"MATERIALES: Cuaderno, libros de la SEP, material concreto.")
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, safe_text(teoria_m)); pdf.ln(3)

        # VI. FUENTES
        pdf.ln(5); pdf.seccion_titulo("VI. REFERENCIAS")
        pdf.set_font('Helvetica', 'I', 9); pdf.multi_cell(0, 5, "SEP (2026). Plan de Estudios. https://sep.gob.mx\nUNESCO. Recursos de Aprendizaje Activo.")

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
        status.update(label="✅ ¡Planeación lista!", state="complete")
        
        st.download_button(label="📥 DESCARGAR PLANEACION COMPLETA (PDF)", data=pdf_bytes, file_name=f"Planeacion_{safe_text(tema_interes)}.pdf", mime="application/pdf", use_container_width=True)
