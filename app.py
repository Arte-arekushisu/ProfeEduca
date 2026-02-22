import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Escrito Reflexivo", layout="wide", page_icon="🖋️")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexionPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('ESCRITO REFLEXIVO DIARIO'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, eca, com, fec, niv, gra):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(245, 245, 245)
        w, h = 95, 7
        self.cell(w, h, clean(f" NOMBRE EC: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" NOMBRE ECA: {eca}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {com}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" FECHA: {fec}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" NIVEL: {niv}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO: {gra}"), 1, 1, 'L', True)
        self.ln(10)

# --- INTERFAZ ---
st.title("🖋️ PROFEEDUCA: Bitácora de Reflexión")
st.markdown("En este apartado, registra los sucesos más relevantes, los logros y los desafíos de tu práctica diaria.")

with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Nombre EC", "AXEL REYES")
    nombre_eca = st.text_input("Nombre ECA")
    comunidad = st.text_input("Comunidad", "CRUZ")
    fecha_hoy = st.date_input("Fecha", datetime.date.today())
    nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grados = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel == "Primaria" else ["1", "2", "3", "Multigrado"]
    grado = st.selectbox("Grado", grados)

# --- BLOQUE DE REFLEXIÓN SEMANAL ---
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
datos_reflexion = {}

st.subheader("📝 Registro de Reflexiones")
for dia in dias:
    with st.expander(f"📔 REFLEXIÓN: {dia.upper()}", expanded=(dia == "Lunes")):
        datos_reflexion[dia] = st.text_area(
            f"Escribe aquí lo ocurrido el {dia}:", 
            key=f"ref_{dia}", 
            height=200,
            placeholder="¿Qué aprendieron hoy? ¿Qué dificultades enfrentaste? ¿Cómo mejorará tu práctica mañana?"
        )

# --- GENERACIÓN DEL DOCUMENTO ---
st.divider()
if st.button("📝 GENERAR ESCRITO REFLEXIVO DIARIO", use_container_width=True):
    pdf = ReflexionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Encabezado y Tabla
    pdf.tabla_datos(nombre_ec, nombre_eca, comunidad, str(fecha_hoy), nivel, grado)

    # Contenido de reflexiones
    for dia, texto in datos_reflexion.items():
        if texto.strip():
            # Título del día con banda de color
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(128, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 9, clean(f" JORNADA DEL {dia.upper()}"), 0, 1, 'L', True)
            
            # Texto de la reflexión
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'I', 11)
            pdf.multi_cell(0, 6, clean(texto))
            pdf.ln(8)
            
    # Espacio para firmas al final
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 10)
    x = pdf.get_x()
    y = pdf.get_y()
    pdf.line(x + 10, y, x + 80, y)
    pdf.line(x + 110, y, x + 180, y)
    pdf.set_y(y + 2)
    pdf.cell(95, 5, clean("Firma del EC"), 0, 0, 'C')
    pdf.cell(95, 5, clean("Firma del ECA / Monitor"), 0, 1, 'C')

    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
    
    st.success("✅ Tu escrito reflexivo ha sido procesado.")
    st.download_button(
        label="📥 DESCARGAR BITÁCORA DE REFLEXIÓN",
        data=pdf_bytes,
        file_name=f"Escrito_Reflexivo_{comunidad}_{fecha_hoy}.pdf",
        mime="application/pdf"
    )
