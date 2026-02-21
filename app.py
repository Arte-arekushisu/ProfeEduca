import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 10s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-sidebar { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; }
    .comment-card { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #00d4ff; font-size: 0.85em; }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES TÉCNICAS
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PLANEACION INTEGRAL MAESTRO ABCD', 0, 1, 'C')
        self.ln(5)

# 3. PERSISTENCIA DE DATOS
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user": "", "plan": "", 
        "alumnos": {}, # Diccionario persistente de escritos
        "comentarios": [{"user": "Maestro_Gomez", "text": "¡Las estaciones generadas por IA son increíbles!"}]
    }

# 4. LOGIN / REGISTRO
if not st.session_state.db["auth"]:
    st.markdown("<h1>Profe Educa: Sistema ABCD</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("registro"):
            u_user = st.text_input("Nombre de usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan = st.radio("Plan de Suscripción", ["Plata ($200)", "Oro ($400)", "Platino ($600)"])
            if st.form_submit_button("INGRESAR"):
                st.session_state.db.update({"auth": True, "user": u_user, "plan": plan})
                st.rerun()
    with col2:
        st.markdown("<div class='comment-sidebar'><h3>Comunidad</h3>", unsafe_allow_html=True)
        for c in st.session_state.db["comentarios"]:
            st.markdown(f"<div class='comment-card'><b>{c['user']}:</b> {c['text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# 5. PANEL PRINCIPAL
else:
    st.sidebar.title(f"EC: {st.session_state.db['user']}")
    menu = st.sidebar.radio("MENÚ", ["📅 Planeación IA", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 SOS"])

    if menu == "📅 Planeación IA":
        st.header("Generar Planeación Semanal Extensa")
        
        # Niveles Educativos
        niveles = [
            "Preescolar (1°)", "Preescolar (2°)", "Preescolar (3°)",
            "Primaria (1°)", "Primaria (2°)", "Primaria (3°)", "Primaria (4°)", "Primaria (5°)", "Primaria (6°)", "Primaria Multigrado",
            "Secundaria (1°)", "Secundaria (2°)", "Secundaria (3°)", "Secundaria Multigrado"
        ]
        
        col_a, col_b = st.columns(2)
        nivel_sel = col_a.selectbox("Nivel Educativo", niveles)
        comu = col_b.text_input("Comunidad")
        eca = col_a.text_input("ECA")
        tema = st.text_input("Tema de Interés (Investigación Semanal)")
        estacion = st.text_input("Estación Permanente")
        
        if st.button("Generar Investigación y Planeación"):
            # Lógica de IA para contenido extenso y fuentes
            investigacion = f"Secuencia didáctica de 5 días sobre {tema}. Incluye experimentación, análisis de textos y cierre con producto final."
            fuentes = [f"https://es.wikipedia.org/wiki/{tema.replace(' ','_')}", "https://escolares.net/", "https://www.conafe.gob.mx/"]

            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, limpiar(f"Nivel: {nivel_sel} | Comunidad: {comu} | EC: {st.session_state.db['user']} | ECA: {eca}"), 0, 1)
            pdf.ln(5)

            # Tabla con ajuste de texto (MultiCell)
            pdf.set_fill_color(0, 212, 255)
            pdf.cell(40, 10, "Momento", 1, 0, 'C', 1)
            pdf.cell(110, 10, "Desarrollo Semanal IA", 1, 0, 'C', 1)
            pdf.cell(35, 10, "Tiempo", 1, 1, 'C', 1)

            pdf.set_font("Arial", '', 9)
            momentos = [
                ["Bienvenida", "Actividades grupales diarias de integración.", "15 min/dia"],
                ["Regalo Lectura", f"Lectura semanal enfocada en {tema}.", "20 min/dia"],
                [f"Estación: {estacion}", investigacion, "90 min/dia"],
                ["Cierre", "Evaluación de aprendizajes logrados.", "30 min/dia"]
            ]

            for m in momentos:
                h = 20 # Altura de celda para que quepa el texto
                pdf.cell(40, h, limpiar(m[0]), 1)
                x, y = pdf.get_x(), pdf.get_y()
                pdf.multi_cell(110, 5, limpiar(m[1]), 1)
                pdf.set_xy(x + 110, y)
                pdf.cell(35, h, limpiar(m[2]), 1, 1)

            # Apartado de Fuentes
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, "FUENTES DE CONSULTA:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for f in fuentes:
                pdf.cell(0, 6, f, 0, 1)

            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación Semanal", pdf_bytes, f"Planeacion_{tema}.pdf")

    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro de Escrito Diario")
        nom_al = st.text_input("Nombre del Alumno").upper()
        txt_diario = st.text_area("¿Qué descubrió el alumno hoy?")
        if st.button("Guardar en Memoria"):
            if nom_al not in st.session_state.db["alumnos"]:
                st.session_state.db["alumnos"][nom_al] = []
            st.session_state.db["alumnos"][nom_al].append(txt_diario)
            st.success(f"Registrado correctamente para {nom_al}")

    elif menu == "📊 Evaluación Trimestral":
        st.header("Buscador de Historial para Evaluación")
        busqueda = st.text_input("Escribe el nombre del alumno").upper()
        if busqueda in st.session_state.db["alumnos"]:
            escritos = st.session_state.db["alumnos"][busqueda]
            st.info(f"Se encontraron {len(escritos)} escritos diarios para {busqueda}.")
            for e in escritos:
                st.markdown(f"--- \n *{e}*")
            st.button("Generar Informe Trimestral IA")
        elif busqueda != "":
            st.warning("Alumno no encontrado. Asegúrate de haber guardado escritos en el 'Diario Reflexivo' primero.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
