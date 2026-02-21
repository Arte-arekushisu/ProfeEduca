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
        self.set_font('Helvetica', 'B', 25)
        self.cell(0, 20, 'PLANEACION', 0, 1, 'C')
        self.ln(5)

    def barra(self, titulo, color=(40, 40, 40)):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(*color); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {clean(titulo)}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0); self.ln(2)

st.set_page_config(page_title="PLANEACION", layout="wide")
st.title("🛡️ Sistema de Planeacion Integral Definitivo")

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

    st.subheader("🗓️ Bloque Post-Receso (Materias por dia)")
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    mats_inputs = {}
    cols = st.columns(5)
    for i, col in enumerate(cols):
        mats_inputs[dias_semana[i]] = col.text_area(f"{dias_semana[i]}", "Matematicas\nEd. Fisica")

    submit = st.form_submit_button("🔨 GENERAR PLANEACION COMPLETA")

if submit:
    with st.spinner("⏳ Estructurando pedagogia y estaciones..."):
        time.sleep(3)
        
        # --- LÓGICA DE MOMENTOS INICIALES ---
        regalo = "Lectura de cuentos con titeres" if nivel == "Preescolar" else "Lectura de articulos de investigacion"
        bienvenida = "Juego motriz: 'El nido'" if nivel == "Preescolar" else "Debate: 'Saberes de la comunidad'"

        # --- LÓGICA DE ESTACIONES (4 CAMPOS - 5 DÍAS CON ACTIVIDADES) ---
        estaciones = [
            {
                "campo": "Lenguajes (Estacion de Relatos)",
                "materiales": "Hojas, gises, grabadora, material reciclado.",
                "actividades": "Lunes: Dibujo de hipotesis. Martes: Collage de palabras clave. Miercoles: Grabacion de relatos orales. Jueves: Creacion de carteles de difusion. Viernes: Exposicion comunitaria."
            },
            {
                "campo": "Saberes y P.C. (Laboratorio)",
                "materiales": "Semillas, balanzas caseras, arena, botes.",
                "actividades": "Lunes: Conteo de nidos/objetos. Martes: Clasificacion por peso. Miercoles: Medicion de trayectorias en arena. Jueves: Registro de datos en tablas. Viernes: Elaboracion de graficas simples."
            },
            {
                "campo": "Etica, Nat. y Soc. (Guardianes)",
                "materiales": "Mapas, carton, basura limpia para maquetas.",
                "actividades": "Lunes: Identificacion de zonas de riesgo. Martes: Rastro de contaminacion local. Miercoles: Maqueta de refugio natural. Jueves: Redaccion de acuerdos de cuidado. Viernes: Firma del pacto comunitario."
            },
            {
                "campo": "De lo Humano y lo Com. (Circulo)",
                "materiales": "Telas, espejos, objetos de la comunidad.",
                "actividades": "Lunes: Juego de roles de cuidado. Martes: Sesion de tutoria entre pares. Miercoles: Expresion de emociones ante el tema. Jueves: Intercambio de saberes con adultos invitados. Viernes: Reflexion grupal final."
            }
        ]

        # --- VISUALIZACION EN PANTALLA ---
        st.success("✅ Planeacion Generada Correctamente")
        t1, t2, t3, t4 = st.tabs(["🌅 Momentos Iniciales", "🏫 Estaciones Semanales", "🕒 Post-Receso", "🏠 Tareas"])
        
        with t1:
            st.markdown(f"**Pase de Lista:** Actividad sobre {tema}")
            st.markdown(f"**Regalo de Lectura:** {regalo}")
            st.markdown(f"**Bienvenida:** {bienvenida}")
        
        with t2:
            for e in estaciones:
                with st.expander(f"📍 {e['campo']}"):
                    st.write(f"**Materiales:** {e['materiales']}")
                    st.write(f"**Secuencia de la semana:** {e['actividades']}")
        
        with t3:
            for d, m in mats_inputs.items():
                st.write(f"**{d}:** {m}")
        
        with t4:
            st.info(f"Tarea Diaria: Investigacion familiar sobre un aspecto de {tema}")
            st.warning("Proyecto Fin de Semana: Accion de limpieza o recoleccion en la comunidad.")

        # --- GENERACION PDF ---
        pdf = PlaneacionFinalPDF()
        pdf.add_page()
        
        pdf.barra("I. DATOS DE IDENTIFICACION")
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, clean(f"Educador: {educador}\nNivel/Grado: {nivel}/{grado}\nComunidad: {comunidad}\nTema: {tema}\nFecha: {fecha}"))
        
        pdf.ln(5); pdf.barra("II. MOMENTOS INICIALES (25 MIN)")
        pdf.multi_cell(0, 6, clean(f"- Pase de lista: Tematico sobre {tema}\n- Regalo de lectura: {regalo}\n- Bienvenida: {bienvenida}"))

        pdf.ln(5); pdf.barra("III. ESTACIONES DIDACTICAS (5 DIAS)")
        for e in estaciones:
            pdf.set_font('Helvetica', 'B', 11); pdf.cell(0, 8, clean(e['campo']), 0, 1)
            pdf.set_font('Helvetica', 'I', 9); pdf.cell(0, 6, clean(f"Materiales: {e['materiales']}"), 0, 1)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 5, clean(f"Plan Semanal: {e['actividades']}\n"))

        pdf.add_page(); pdf.barra("IV. MATERIAS POST-RECESO Y TAREAS")
        for d, m in mats_inputs.items():
            pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"{d}:"), 1, 1, 'L', True)
            pdf.set_font('Helvetica', '', 10); pdf.multi_cell(0, 6, clean(f"Materias: {m}\nTarea para casa: Vinculacion con {tema}.\n"))

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.divider()
        st.download_button("📥 DESCARGAR PLANEACION COMPLETA", data=pdf_bytes, file_name="Planeacion.pdf", mime="application/pdf", use_container_width=True)
