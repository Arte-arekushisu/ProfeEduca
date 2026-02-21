import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import time

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('•', '-')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class PlaneacionFinalPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 15, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(40, 40, 40)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color); self.set_text_color(255, 255, 255)
        self.cell(0, 8, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(2)

st.set_page_config(page_title="PLANEACION", layout="wide")
st.title("🛡️ Sistema de Planeacion de Contenido Extenso")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado/Grupo", "1")
        educador = st.text_input("Nombre del Educador", "AXEL REYES")
    with c2:
        eca = st.text_input("ECA", "reyes")
        comunidad = st.text_input("Comunidad", "CRUZ")
        tema = st.text_input("Tema de Interes", "LAS TORTUGAS MARINAS")
    with c3:
        fecha = st.date_input("Fecha", datetime.date.today())
        rincon = st.text_input("Rincon de Trabajo", "LECTURA/CIENCIAS")

    st.subheader("🗓️ Bloque Post-Receso (2 Horas Diarias)")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes")

    submit = st.form_submit_button("🔨 GENERAR PLANEACION CON CONTENIDO EXTENSO")

if submit:
    with st.spinner("⏳ Expandiendo informacion y redactando procedimientos..."):
        time.sleep(3)
        
        # --- MARCO TEÓRICO Y PREGUNTAS DETONANTES ---
        marco_teorico = f"""Las {tema} son fundamentales para el equilibrio de los ecosistemas. 
        En esta sesion exploraremos su ciclo de vida, los riesgos de la contaminacion por microplasticos 
        y la importancia de la preservacion en la comunidad de {comunidad}. 
        PREGUNTAS DETONANTES: 
        1. ¿Como influye la temperatura del nido en el genero de la especie?
        2. ¿Que adaptaciones biologicas les permiten navegar miles de kilometros?
        3. ¿Como afecta nuestra basura local a su ruta migratoria?
        4. ¿Por que se consideran 'arquitectas' de los arrecifes?
        5. ¿Cual es la responsabilidad etica de nuestra comunidad frente a su extincion?"""

        # --- ESTACIONES CON PROCEDIMIENTOS DETALLADOS ---
        estaciones = [
            {
                "campo": "Lenguajes (Estacion de Relatos)",
                "proc": "1. Investigacion: Leer fichas tecnicas. 2. Redaccion: Escribir una cronica en primera persona (Ej: 'Yo, la tortuga viajera'). 3. Produccion: Crear un audio-relato usando materiales de reciclaje para efectos de sonido.",
                "ejemplo": "Ejemplo: Un podcast de 1 minuto sobre el primer viaje al mar."
            },
            {
                "campo": "Saberes y P.C. (Laboratorio)",
                "proc": "1. Observacion: Analizar patrones en caparazones usando geometria. 2. Experimentacion: Simular la flotabilidad en agua salada vs dulce. 3. Registro: Tabular datos de crecimiento promedio segun la especie.",
                "ejemplo": "Ejemplo: Grafica de barras comparando tamaños de 3 especies distintas."
            },
            {
                "campo": "Etica, Nat. y Soc. (Guardianes)",
                "proc": "1. Diagnostico: Mapear puntos criticos de basura en la escuela. 2. Propuesta: Diseñar un contenedor especial 'Anti-Residuos Marinos'. 3. Accion: Redactar una carta formal a las autoridades locales.",
                "ejemplo": "Ejemplo: Maqueta de un nido protegido con malla reciclada."
            }
        ]

        # --- VISUALIZACION ---
        st.success("✅ Planeacion Extensa Generada")
        t1, t2, t3 = st.tabs(["📖 Marco Teorico", "🏫 Estaciones y Procedimientos", "🕒 Post-Receso (2 hrs)"])
        
        with t1:
            st.write(marco_teorico)
        with t2:
            for e in estaciones:
                st.markdown(f"**{e['campo']}**")
                st.write(f"*Procedimiento:* {e['proc']}")
                st.caption(e['ejemplo'])
        with t3:
            for d, m in mats_inputs.items():
                st.write(f"**{d}:** 60 min Materia A / 60 min Materia B. Total 120 min.")

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        pdf.barra("I. TEMA DE INTERES Y MARCO TEORICO")
        pdf.set_font('Helvetica', '', 9)
        pdf.multi_cell(0, 5, clean(marco_teorico))
        
        pdf.ln(5); pdf.barra("II. ESTACIONES: PROCEDIMIENTOS Y EJEMPLOS")
        for e in estaciones:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(e['campo']), 0, 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean(f"PROCEDIMIENTO: {e['proc']}\n{e['ejemplo']}\n"))

        pdf.add_page(); pdf.barra("III. POST-RECESO (BLOQUE DE 2 HORAS)")
        for d, m in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"{d}:"), 1, 1, 'L', True)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean(
                f"HORA 1 (60 min): {m} - Inicio: Recuperacion de saberes. Desarrollo: Actividad practica con ejemplo real. Cierre: Evaluacion grupal.\n"
                f"HORA 2 (60 min): Materia Complementaria - Proyecto transversal vinculado a {tema}.\n"
            ))

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.divider()
        st.download_button("📥 DESCARGAR PLANEACION COMPLETA", data=pdf_bytes, file_name="Planeacion_Extensa.pdf", mime="application/pdf", use_container_width=True)
