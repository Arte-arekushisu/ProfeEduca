import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE SEGURIDAD CONTRA ERRORES ---
def clean(txt):
    if not txt: return ""
    # Soluciona el UnicodeEncodeError eliminando acentos
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

class ProfeEducaSaaS(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(20, 40, 80)
        self.cell(0, 10, 'SISTEMA INTEGRAL DE PLANEACION - FASE 0.4', 0, 1, 'C')
        self.ln(5)

    def seccion_azul(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(3)

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="ProfeEduca Fase 0.4", layout="wide")
st.title("🧩 SaaS Educativo: Integracion Final de Fase 0.4")

with st.form("Master_SaaS_Form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Proyecto / Tema", "LAS TORTUGAS MARINAS")
        nombre_eca = st.text_input("Nombre del ECA", "reyes")
    with c2:
        grado = st.text_input("Grado y Grupo", "1")
        comunidad = st.text_input("Comunidad", "CRUZ")
        rincon = st.text_input("Rincon Asignado", "RICON DE LECTURA")
        materia_post = st.text_input("Tema Post-Receso", "MATEMATICAS")

    submit = st.form_submit_button("🔨 GENERAR PIEZA MAESTRA")

if submit:
    # --- LOGICA DE CONTENIDO POR NIVEL (FASES PREVIAS) ---
    niveles_config = {
        "Preescolar": {"pase": "Imitar un sonido natural", "regalo": "Cuento narrado con titeres"},
        "Primaria": {"pase": "Mencionar palabra clave del tema", "regalo": "Leyenda local o regional"},
        "Secundaria": {"pase": "Cita de autor relevante", "regalo": "Articulo cientifico breve"}
    }
    conf = niveles_config[nivel]

    pdf = ProfeEducaSaaS()
    pdf.add_page()
    
    # I. IDENTIFICACION (Correccion de IndexError)
    pdf.seccion_azul("I. IDENTIFICACION PROFESIONAL")
    datos_id = [
        ["Educador", educador], ["ECA", nombre_eca],
        ["Nivel/Grado", f"{nivel}/{grado}"], ["Comunidad", comunidad],
        ["Rincon", rincon], ["Fecha", str(datetime.date.today())]
    ]
    for d in datos_id:
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(50, 8, f" {clean(d[0])}:", 1, 0, 'L', True)
        pdf.set_font('Helvetica', '', 10); pdf.cell(140, 8, f" {clean(d[1])}", 1, 1, 'L')
    pdf.ln(5)

    # II. BIENVENIDA DINAMICA
    pdf.seccion_azul("II. MOMENTO DE INICIO")
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, f"- Pase de lista: {clean(conf['pase'])}\n"
                         f"- Regalo de lectura: {clean(conf['regalo'])}\n"
                         f"- Reflexion inicial sobre: {clean(tema)}")
    pdf.ln(5)

    # III. ESTACIONES AUTONOMAS (INSTRUCCIONES DE 3 PASOS)
    pdf.seccion_azul("III. ESTACIONES DE TRABAJO (AUTONOMIA DEL ALUMNO)")
    estaciones_data = [
        {"c": "Lenguajes", "n": "Mural Literario", "i": "1. Elige 3 palabras del tema.\n2. Crea un cartel ilustrado.\n3. Comparte tu definicion."},
        {"c": "Saberes y P.C.", "n": "Laboratorio Cientifico", "i": "1. Mide 3 objetos del rincon.\n2. Registra pesos en bitacora.\n3. Encuentra diferencias."},
        {"c": "Etica / Humano", "n": "Acuerdos Comunitarios", "i": "1. Detecta un problema del tema.\n2. Propon una solucion escrita.\n3. Firma tu compromiso."}
    ]
    for e in estaciones_data:
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Campo: {clean(e['c'])} - {clean(e['n'])}", 0, 1)
        pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"CONSIGNA:\n{clean(e['i'])}\n")

    # IV. MOTOR PEDAGOGICO (INFORMACION EXTENSA)
    pdf.add_page()
    pdf.seccion_azul("IV. SUSTENTO TECNICO Y PEDAGOGICO")
    pdf.set_font('Helvetica', '', 11)
    sustento = (f"El abordaje de {tema} en {nivel} se centra en la investigacion activa. "
                "Cientificamente, se analizan los ciclos y la interdependencia natural. "
                "El alumno lidera el proceso mediante la Relacion Tutora (RPA) y el uso de materiales locales.")
    pdf.multi_cell(0, 8, clean(sustento))

    # V. POST-RECESO (TRABAJO TECNICO)
    pdf.ln(5); pdf.seccion_azul("V. BLOQUE POST-RECESO")
    pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Materia: {clean(materia_post)}", 0, 1)
    pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 7, "1. Explicacion teorica.\n2. Ejercicios de aplicacion (10 reactivos).\n3. Plenaria de resultados.")

    # --- GENERACION FINAL ---
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 DESCARGAR PLANEACION COMPLETA F0.4", data=pdf_bytes, file_name="ProfeEduca_F04_Consolidado.pdf", use_container_width=True)
