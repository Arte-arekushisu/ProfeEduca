import streamlit as st
from fpdf import FPDF
import time
import unicodedata

# --- FUNCION PARA LIMPIAR TEXTO (ELIMINA TILDES Y ENES) ---
def limpiar_texto(texto):
    if not texto:
        return ""
    # Normaliza y elimina acentos para que fpdf no explote
    texto_limpio = ''.join(c for c in unicodedata.normalize('NFD', texto)
                           if unicodedata.category(c) != 'Mn')
    return texto_limpio.replace('ñ', 'n').replace('Ñ', 'N')

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(page_title="ProfeEduca V8.0", page_icon="🛡️", layout="wide")

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def seccion_azul(self, texto):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(31, 52, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {limpiar_texto(texto)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- INTERFAZ ---
st.title("🛡️ Generador de Planeacion (Version Blindada)")
st.info("Esta version limpia acentos automaticamente para evitar errores de descarga.")

with st.form("form_seguro"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        educador = st.text_input("Educador", "Axel Reyes")
        tema = st.text_input("Tema", "Tortugas Marinas")
    with c2:
        comunidad = st.text_input("Comunidad", "San Michi")
        fecha = st.date_input("Fecha")
        rincon = st.text_input("Rincon", "Lectura")

    st.subheader("Materiales y Post-Receso")
    mat_list = st.text_area("Lista de Materiales (uno por linea)", "Hojas\nColores\nLupas")
    materia_post = st.text_input("Materia Post-Receso", "Suma de fracciones")
    
    boton = st.form_submit_button("🔨 GENERAR PDF SIN ERRORES")

if boton:
    try:
        status = st.status("Validando caracteres y generando PDF...")
        
        pdf = PDF()
        pdf.add_page()
        
        # Seccion de Datos
        pdf.seccion_azul("I. DATOS GENERALES")
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 10, f"Educador: {limpiar_texto(educador)} | Comunidad: {limpiar_texto(comunidad)}", 0, 1)
        pdf.cell(0, 10, f"Nivel: {nivel} | Tema: {limpiar_texto(tema)}", 0, 1)
        
        # Seccion de Materiales (Tu peticion especial)
        pdf.ln(5)
        pdf.seccion_azul("II. MATERIALES NECESARIOS")
        pdf.set_font('Helvetica', '', 11)
        for item in mat_list.split('\n'):
            if item.strip():
                pdf.cell(0, 8, f"- {limpiar_texto(item)}", 0, 1)

        # Seccion de Estaciones y Campos
        pdf.ln(5)
        pdf.seccion_azul("III. ESTACIONES Y CAMPOS FORMATIVOS")
        pdf.multi_cell(0, 8, f"En esta sesion de {nivel}, los alumnos trabajaran en estaciones de "
                             "Saberes, Lenguajes, Etica y lo Humano. Cada estacion usara los "
                             "materiales listados arriba para fomentar la autonomia.")

        # Post Receso
        pdf.add_page()
        pdf.seccion_azul("IV. BLOQUE POST-RECESO (DESARROLLO)")
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, f"Materia: {limpiar_texto(materia_post)}", 0, 1)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 8, "Teoria: Explicacion detallada del concepto en el pizarron.\n"
                             "Ejemplos: Aplicacion en situaciones cotidianas de la comunidad.\n"
                             "Actividad: Resolucion de 5 ejercicios en el cuaderno y plenaria grupal.")

        # --- EL PASO CRITICO PARA EVITAR EL ERROR ---
        # Usamos 'replace' para que si algo falla, no detenga el proceso
        pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
        
        status.update(label="✅ PDF generado correctamente", state="complete")
        
        st.download_button(
            label="📥 Descargar Planeacion Segura",
            data=pdf_output,
            file_name=f"Planeacion_{limpiar_texto(tema)}.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Hubo un problema inesperado: {e}")
