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
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'SISTEMA INTEGRAL DE PLANEACION', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, 'Contenido Pedagogico Extenso y Detallado', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(40, 40, 40)):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(*color); self.set_text_color(255, 255, 255)
        self.cell(0, 8, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(2)

st.set_page_config(page_title="PLANEACION PRO", layout="wide")
st.title("🛡️ Generador de Planeacion de Contenido Extenso")

with st.form("MasterForm"):
    c1, c2, c3 = st.columns(3)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
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
    st.info("Escribe dos materias por dia separadas por un salto de linea (Enter).")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nArtes", height=100)

    submit = st.form_submit_button("🔨 GENERAR DOCUMENTO COMPLETO")

if submit:
    with st.spinner("⏳ Generando contenido fluido y procedimientos detallados..."):
        time.sleep(2)
        
        # --- MARCO TEÓRICO EXTENSO ---
        marco_teorico = f"""El abordaje de {tema} promueve la investigacion activa en la comunidad de {comunidad}. 
        Desde el punto de vista cientifico, se analizan los ciclos de vida y la interdependencia del ecosistema local.
        PREGUNTAS DETONANTES PARA EL GRUPO: 
        1. ¿Como sabe una tortuga a que playa regresar despues de años?
        2. ¿Que pasaria si el plastico reemplaza la arena en los nidos?
        3. ¿Cual es la funcion del caparazon en su vida diaria?
        4. ¿Como afecta nuestra basura local a su ruta migratoria?
        5. ¿Cual es nuestra responsabilidad etica frente a su extincion?"""

        # --- ESTACIONES DIDÁCTICAS ---
        estaciones = [
            {"campo": "Lenguajes - Mural Literario", "proc": "1. Identificacion: Elegir 3 palabras clave del tema. 2. Produccion: Crear un cartel ilustrado con definicion propia. 3. Socializacion: Compartir el hallazgo oralmente."},
            {"campo": "Saberes y P.C. - Laboratorio", "proc": "1. Observacion: Analizar patrones geometricos en el tema. 2. Registro: Tabular datos en bitacora (pesos, medidas). 3. Analisis: Encontrar diferencias y similitudes."},
            {"campo": "Etica / Humano - Compromisos", "proc": "1. Diagnostico: Detectar un problema comunitario sobre el tema. 2. Propuesta: Redactar una solucion escrita. 3. Cierre: Firma de compromiso individual."}
        ]

        # --- LÓGICA DE ACTIVIDADES POR MATERIA ---
        def get_actividad_detalle(materia):
            m = materia.upper()
            if "MATEMATICAS" in m: return "Suma de fracciones y resolucion de problemas logicos."
            if "ARTES" in m: return "Tecnica de dibujo a carboncillo o practica de flauta dulce."
            if "FISICA" in m: return "Estiramiento corporal y circuitos de agilidad con balon."
            if "ESPANOL" in m: return "Analisis de tipos de texto y redaccion de cronicas."
            return "Actividad practica vinculada al proyecto transversal."

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        # I. IDENTIFICACION
        pdf.barra("I. IDENTIFICACION PROFESIONAL")
        pdf.set_font('Helvetica', '', 10)
        datos = [["Educador:", educador], ["ECA:", eca], ["Nivel/Grado:", f"{nivel}/{grado}"], 
                 ["Comunidad:", comunidad], ["Rincon:", rincon], ["Fecha:", str(fecha)]]
        for d in datos:
            pdf.cell(40, 7, clean(d[0]), 0)
            pdf.cell(0, 7, clean(d[1]), 0, 1)
        
        # II. MARCO TEORICO
        pdf.ln(5); pdf.barra("II. SUSTENTO TECNICO Y PREGUNTAS DETONANTES")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, clean(marco_teorico))

        # III. ESTACIONES
        pdf.ln(5); pdf.barra("III. ESTACIONES DE TRABAJO (AUTONOMIA)")
        for e in estaciones:
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(e['campo']), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(f"CONSIGNA: {e['proc']}\n"))

        # IV. POST-RECESO DIVIDIDO
        pdf.add_page(); pdf.barra("IV. BLOQUE POST-RECESO (DIVISION POR HORAS)")
        for d, m_text in mats_inputs.items():
            materias = m_text.split('\n')
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(f"DIA: {d}"), 1, 1, 'C', True)
            
            # HORA 1
            m1 = materias[0] if len(materias) > 0 else "Materia A"
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"HORA 1 (60 min): {m1}"), 0, 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean(f"Detalle: {get_actividad_detalle(m1)}\nInicio: Recuperacion de saberes. Desarrollo: Ejercicios aplicados. Cierre: Plenaria.\n"))
            
            # HORA 2
            m2 = materias[1] if len(materias) > 1 else "Materia B"
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"HORA 2 (60 min): {m2}"), 0, 1)
            pdf.set_font('Helvetica', '', 9); pdf.multi_cell(0, 5, clean(f"Detalle: {get_actividad_detalle(m2)}\nInicio: Dinamica grupal. Desarrollo: Produccion creativa. Cierre: Evaluacion.\n"))
            pdf.ln(2)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
        
        st.success("✅ Planeacion Generada")
        st.download_button("📥 DESCARGAR PDF FINAL", data=pdf_bytes, file_name="Planeacion_Consolidada.pdf", mime="application/pdf", use_container_width=True)
