import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- MOTOR DE NORMALIZACIÓN ---
def clean(txt):
    if not txt: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(txt)) 
                  if unicodedata.category(c) != 'Mn').replace('ñ', 'n').replace('Ñ', 'N')

# --- CLASE PDF PROFESIONAL ---
class PlaneacionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(31, 52, 94)
        self.cell(0, 15, 'PLANEACION PEDAGOGICA INTEGRAL', 0, 1, 'C')
        self.ln(5)

    def seccion_barra(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- APP STREAMLIT ---
st.set_page_config(page_title="Innovacion Educativa v0.4", layout="wide", page_icon="🍎")
st.title("🧩 Rompecabezas: Consolidacion de Fase 4")

with st.form("SaaS_Form"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
        tema = st.text_input("Tema de Interés", "TORTUGAS MARINAS")
        nombre_eca = st.text_input("Nombre del ECA", "reyes")
    with c2:
        grado = st.text_input("Grado", "1")
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha = st.date_input("Fecha", datetime.date.today())
        rincon = st.text_input("Rincón asignado", "RICON DE LECTURA")

    st.markdown("---")
    st.subheader("Materia Post-Receso (Trabajo Profundo)")
    materia1 = st.text_input("Materia Post-Receso 1", "ETS")
    materia2 = st.text_input("Materia Post-Receso 2", "Suma de fracciones")
    
    boton = st.form_submit_button("🔨 GENERAR Y REVISAR PLANEACIÓN")

if boton:
    with st.status("🧠 Extrayendo información técnica y unificando fases...", expanded=True) as s:
        
        teoria_dic = {
            "Preescolar": "El enfoque se basa en la curiosidad natural. Se busca que el niño desarrolle nociones espaciales y de cuidado del entorno.",
            "Primaria": "Se implementa el Pensamiento Critico. El alumno debe analizar como el tema afecta su entorno inmediato y proponer soluciones.",
            "Secundaria": "Investigacion epistemologica profunda. Se requiere que el estudiante conecte el tema con problematicas globales y sintesis tecnica."
        }

        pdf = PlaneacionPDF()
        pdf.add_page()
        
        # I. IDENTIFICACIÓN
        pdf.seccion_barra("I. DATOS DE IDENTIFICACION")
        datos_tabla = [
            ["Educador", educador], ["ECA", nombre_eca],
            ["Nivel/Grado", f"{nivel} / {grado}"], ["Comunidad", comunidad],
            ["Fecha", str(fecha)], ["Rincon", rincon]
        ]
        for fila in datos_tabla:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(50, 8, f" {clean(fila[0])}:", 1, 0, 'L', True)
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(140, 8, f" {clean(fila[1])}", 1, 1, 'L')
        pdf.ln(5)

        # II. BIENVENIDA
        pdf.seccion_barra("II. INICIO Y BIENVENIDA")
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, f"Actividad: Enfoque en {clean(tema)}. Regalo de lectura adecuado al nivel. Reflexion grupal sobre el impacto local.")
        pdf.ln(5)

        # III. ESTACIONES (4 CAMPOS)
        pdf.seccion_barra("III. ESTACIONES POR CAMPOS FORMATIVOS")
        campos = [
            ["Lenguajes", "Creacion de un Codigo Comunitario. Materiales: Hojas, colores."],
            ["Saberes y P.C.", f"Analisis de formas relacionados con {clean(tema)}. Materiales: Reglas."],
            ["Etica y Nat.", "Dialogo sobre el impacto humano. Acuerdos de Convivencia."],
            ["De lo Humano", "Juego de roles aplicado al intercambio de saberes."]
        ]
        for c in campos:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 7, clean(c[0]), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, f"Instrucciones: {clean(c[1])}\n")
        
        # IV. TUTOREO (LÍNEA CORREGIDA)
        pdf.add_page()
        pdf.seccion_barra(f"IV. TUTOREO Y PROFUNDIZACION: {clean(tema)}")
        pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, "Marco Teorico de Investigacion:", 0, 1)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, f"{teoria_dic[nivel]} \n\nEstudio de {clean(tema)} bajo la guia del tutor.")

        # V. POST-RECESO
        pdf.ln(5); pdf.seccion_barra("V. BLOQUE POST-RECESO")
        for m in [materia1, materia2]:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, f"Materia: {clean(m)}", 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 6, "Explicacion: Concepto en pizarron. Actividad: Resolucion de ejercicios practicos.\n")

        # --- CIERRE ---
        pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
        s.update(label="✅ Fase 4 Completada", state="complete")
        st.download_button("📥 DESCARGAR PLANEACION", data=pdf_out, file_name=f"Fase4_{clean(tema)}.pdf", use_container_width=True)
