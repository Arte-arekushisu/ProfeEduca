import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE SEGURIDAD BLINDADO (SOLUCIÓN AL ERROR DE UNICODE) ---
def clean(txt):
    if not txt: return ""
    # 1. Quitar acentos y caracteres combinados
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    # 2. Reemplazos manuales obligatorios para fpdf
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    txt = txt.replace('•', '-').replace('“', '"').replace('”', '"').replace('¿', '?').replace('¡', '!')
    # 3. Forzar codificación segura a latin-1 (ignora lo que fpdf no pueda leer sin colapsar)
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionFinal(FPDF):
    def header(self):
        # TÍTULO EXACTO SOLICITADO
        self.set_font('Helvetica', 'B', 25)
        self.set_text_color(30, 30, 30)
        self.cell(0, 20, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(40, 40, 40)):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(*color); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(2)

st.set_page_config(page_title="PLANEACION", layout="wide")
st.title("📑 Generador de Planeacion Semanal Definitivo")

with st.form("Form_Final_V18"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "1")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("Nombre del ECA", "reyes")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interes", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha de Inicio", datetime.date.today())
        rincon = st.text_input("Rincon", "LECTURA/CIENCIAS")

    st.subheader("🗓️ Configuracion de Materias Post-Receso (Lunes a Viernes)")
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias[i]] = col.text_area(f"Materias {dias[i]}", "Matematicas\nEd. Fisica")

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO COMPLETO")

if submit:
    pdf = PlaneacionFinal()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # I. IDENTIFICACIÓN
    pdf.barra("I. DATOS GENERALES")
    pdf.set_font('Helvetica', '', 10)
    info = [["Educador", educador], ["Nivel/Grado", f"{nivel}/{grado}"], ["ECA", eca], ["Comunidad", comunidad], ["Tema", tema], ["Fecha", str(fecha)]]
    for row in info:
        pdf.set_font('Helvetica', 'B', 10); pdf.cell(45, 8, f" {clean(row[0])}:", 1, 0, 'L', True)
        pdf.set_font('Helvetica', '', 10); pdf.cell(145, 8, f" {clean(row[1])}", 1, 1, 'L')
    pdf.ln(5)

    # II. INICIO DIARIO (TIEMPOS PEDAGÓGICOS)
    pdf.barra("II. MOMENTOS DE INICIO (25 MINUTOS)")
    pdf.set_font('Helvetica', '', 10)
    # Nota: Cambié la viñeta por
