import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE NORMALIZACIÓN (V11: Cero errores de caracteres) ---
def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

class ProfeEducaSaaS(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(20, 40, 80)
        self.cell(0, 10, 'SISTEMA PROFESIONAL DE PLANEACION - PROFEEDUCA', 0, 1, 'C')
        self.ln(5)

    def seccion_premium(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(3)

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="ProfeEduca Master v0.4", layout="wide")
st.title("🛡️ Consolidación Final: Inteligencia Pedagógica")

with st.form("Master_SaaS_Form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Educador Responsable", "AXEL REYES")
        tema = st.text_input("Proyecto / Tema de Interés", "LAS TORTUGAS MARINAS")
        nombre_eca = st.text_input("Nombre del ECA", "reyes")
    with c2:
        grado = st.text_input("Grado y Grupo", "1")
        comunidad = st.text_input("Comunidad", "CRUZ")
        rincon = st.text_input("Rincón de Trabajo", "RICON DE LECTURA")
        materia_post = st.text_input("Materia Post-Receso", "MATEMATICAS")

    submit = st.form_submit_button("🔨 GENERAR PIEZA MAESTRA INTEGRAL")

if submit:
    # --- MOTOR DE CONTENIDO EXTENSO (BIBLIOTECA) ---
    config_v = {
        "Preescolar": {"pase": "Imitar un sonido de la naturaleza", "regalo": "Cuento narrado con titeres"},
        "Primaria": {"pase": "Mencionar un dato curioso del tema", "regalo": "Leyenda o mito regional"},
        "Secundaria": {"pase": "Cita de un autor relevante", "regalo": "Articulo cientifico breve"}
    }
    info_n = config_v[nivel]

    pdf = ProfeEducaSaaS()
    pdf.add_page()
    
    # I. IDENTIFICACIÓN (Recuperado de V10/V11 con seguridad)
    pdf.seccion_premium("I. DATOS DE IDENTIFICACION PROFESIONAL")
    datos_id = [
        ["Educador", educador], ["ECA", nombre_eca],
        ["Nivel/Grado", f"{nivel}/{grado}"], ["Comunidad", comunidad],
        ["Rincon", rincon], ["Fecha", str(datetime.date.today())]
    ]
    for d in datos_id:
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(50, 8, f" {clean(d[0])}:", 1, 0, 'L', True)
        pdf.set_font('Helvetica', '', 10); pdf.cell(140, 8, f" {clean(d[1])}", 1, 1, 'L')
    pdf.ln(5)

    # II. BIENVENIDA DINÁMICA
    pdf.seccion_premium("II. MOMENTO DE INICIO")
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, f"- Pase de lista dinámico: {clean(info_n['pase'])}\n"
                         f"- Regalo de lectura: {clean(info_n['regalo'])}\n"
                         f"- Reflexión inicial: Diálogo guiado sobre el impacto de {clean(tema)} en la comunidad.")
    pdf.ln(5)

    # III. ESTACIONES DE AUTONOMÍA (Consignas de 3 pasos)
    pdf.seccion_premium("III. ESTACIONES DE APRENDIZAJE AUTONOMO")
    estaciones_final = [
        {"c": "Lenguajes", "n": "Mural Literario", "i": "1. Investiga en los libros 3 palabras clave.\n2. Diseña un cartel con imagenes representativas.\n3. Presenta tu definicion a un compañero."},
        {"c": "Saberes y P.C.", "n": "Laboratorio Cientifico", "i": "1. Mide y pesa 3 objetos del rincon.\n2. Registra los hallazgos en tu bitacora.\n3. Encuentra un patron o diferencia entre ellos."},
        {"c": "Ética / Humano", "n": "Acuerdos Comunitarios", "i": "1. Identifica un problema relacionado con el tema.\n2. Propon una accion concreta de mejora.\n3. Firma tu compromiso en el mural colectivo."}
    ]
    for e in estaciones_final:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Campo: {clean(e['c'])} - {clean(e['n'])}", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"CONSIGNA DE TRABAJO:\n{clean(e['i'])}\n")

    # IV. MOTOR DE INFORMACIÓN (BIBLIOTECA TÉCNICA)
    pdf.add_page()
    pdf.seccion_premium("IV. SUSTENTO TECNICO Y PEDAGOGICO (PROFUNDIZACION)")
    pdf.set_font('Helvetica', '', 11)
    # Bloque de información extendida real
    biblioteca = (f"El estudio de {tema} en el nivel {nivel} representa un eje transformador. "
                  "Desde una perspectiva cientifica, se analizan los ciclos biológicos y la interdependencia ecológica. "
                  "Esta planeación fomenta la Relacion Tutora (RPA), permitiendo que el alumno lidere su propio "
                  "descubrimiento a través del uso de materiales concretos y fuentes bibliográficas locales.")
    pdf.multi_cell(0, 8, clean(biblioteca))

    # V. POST-RECESO (Estructura V11)
    pdf.ln(5); pdf.seccion_premium("V. BLOQUE POST-RECESO (DESARROLLO TECNICO)")
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Materia / Tema: {clean(materia_post)}", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 7, "1. Explicación teórica en plenaria.\n2. Práctica individual: Resolución de 10 reactivos contextualizados.\n3. Cierre pedagógico: Plenaria de resultados y dudas.")

    # --- GENERACIÓN FINAL ---
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PIEZA MAESTRA F0.4 CONSOLIDADA", data=pdf_bytes, file_name="ProfeEduca_Master_V11.pdf", use_container_width=True)
