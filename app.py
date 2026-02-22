import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Planeación Semanal", layout="wide", page_icon="📝")

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 0, 0) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('PLANEACION SEMANAL Y ESCRITO REFLEXIVO'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, eca, comunidad, fecha, nivel, grado):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        w = 95
        h = 8
        self.cell(w, h, clean(f" NOMBRE EC: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" NOMBRE ECA: {eca}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {comunidad}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" FECHA/SEMANA: {fecha}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" NIVEL: {nivel}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO/MODALIDAD: {grado}"), 1, 1, 'L', True)
        self.ln(5)

    def seccion_dia(self, titulo):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(128, 0, 0)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f" {clean(titulo)}", 0, 1, 'L', True)
        self.ln(2)

# --- INTERFAZ ---
st.title("🛡️ PROFEEDUCA: Planeación y Reflexión")

with st.form("Formulario_Final"):
    st.subheader("📋 Información General")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_eca = st.text_input("Nombre del ECA")
    
    with c2:
        comunidad = st.text_input("Comunidad", "CRUZ")
        fecha_semana = st.date_input("Semana del:", datetime.date.today())
    
    with c3:
        nivel_edu = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        opciones = ["1", "2", "3", "4", "5", "6", "Multigrado"] if nivel_edu == "Primaria" else ["1", "2", "3", "Multigrado"]
        grado_edu = st.selectbox("Grado", opciones)

    st.divider()
    st.subheader("🍎 Jornada Post-Receso y Reflexión Diaria")
    
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    datos_semana = {}

    for dia in dias:
        with st.expander(f"📅 {dia.upper()}", expanded=(dia == "Lunes")):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Materia 1**")
                m1 = st.text_input(f"Nombre", key=f"m1_{dia}")
                p1 = st.text_area(f"Actividades", key=f"p1_{dia}", height=70)
            with col2:
                st.markdown("**Materia 2**")
                m2 = st.text_input(f"Nombre", key=f"m2_{dia}")
                p2 = st.text_area(f"Actividades", key=f"p2_{dia}", height=70)
            
            st.markdown("---")
            # NUEVO: Apartado de Escrito Reflexivo Diario
            reflexion = st.text_area(f"🖋️ Escrito Reflexivo Diario ({dia})", 
                                    placeholder="¿Qué aprendieron hoy? ¿Qué dificultades surgieron? ¿Cómo te sentiste como educador?",
                                    key=f"ref_{dia}", height=100)
            
            datos_semana[dia] = {"m1": m1, "p1": p1, "m2": m2, "p2": p2, "reflexion": reflexion}
    
    submit = st.form_submit_button("🔨 PLANEACIONES ABCD")

if submit:
    st.markdown("### 👁️ Vista Previa")
    
    pdf = PlaneacionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.tabla_datos(nombre_ec, nombre_eca, comunidad, str(fecha_semana), nivel_edu, grado_edu)

    for dia, info in datos_semana.items():
        if info['m1'] or info['m2'] or info['reflexion']:
            pdf.seccion_dia(dia.upper())
            
            # Materia 1 y 2
            for i in range(1, 3):
                m_key, p_key = f'm{i}', f'p{i}'
                if info[m_key]:
                    pdf.set_text_color(0,0,0)
                    pdf.set_font('Helvetica', 'B', 10)
                    pdf.cell(0, 6, clean(f"Materia {i}: {info[m_key]}"), 0, 1)
                    pdf.set_font('Helvetica', '', 10)
                    pdf.multi_cell(0, 5, clean(info[p_key]))
                    pdf.ln(2)
            
            # Escrito Reflexivo en el PDF
            if info['reflexion']:
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(128, 0, 0)
                pdf.cell(0, 6, clean("ESCRITO REFLEXIVO DIARIO:"), 0, 1)
                pdf.set_font('Helvetica', 'I', 10)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 5, clean(info['reflexion']))
                pdf.ln(5)
    
    pdf_output = pdf.output(dest='S')
    pdf_bytes = bytes(pdf_output) if not isinstance(pdf_output, str) else pdf_output.encode('latin-1')

    st.success("✅ Planeación y Reflexiones listas.")
    st.download_button(
        label="📥 DESCARGAR DOCUMENTO COMPLETO (PDF)",
        data=pdf_bytes,
        file_name=f"Planeacion_Reflexion_{comunidad}.pdf",
        mime="application/pdf"
    )
