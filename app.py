import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 12s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-sidebar { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; min-height: 600px; }
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

# 3. BASE DE DATOS DE SESIÓN (PERSISTENTE)
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user": "", "plan": "", 
        "alumnos": {}, 
        "comentarios": [{"user": "Maestro_Gomez", "text": "¡Las estaciones de IA son geniales!"}]
    }

# 4. PÁGINA DE INICIO (REGISTRO)
if not st.session_state.db["auth"]:
    st.markdown("<h1>Profe Educa: Sistema ABCD</h1>", unsafe_allow_html=True)
    col_reg, col_com = st.columns([2, 1])
    with col_reg:
        with st.form("registro"):
            u_user = st.text_input("Nombre de Usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan_sel = st.radio("Suscripción", ["Plata ($200)", "Oro ($400)", "Platino ($600)"])
            if st.form_submit_button("REGISTRAR Y ENTRAR"):
                st.session_state.db.update({"auth": True, "user": u_user, "plan": plan_sel})
                st.rerun()
    with col_com:
        st.markdown("<div class='comment-sidebar'><h3>Comunidad</h3>", unsafe_allow_html=True)
        for c in st.session_state.db["comentarios"]:
            st.markdown(f"<div class='comment-card'><b>{c['user']}:</b> {c['text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# 5. PANEL DEL MAESTRO
else:
    st.sidebar.title(f"Maestro: {st.session_state.db['user']}")
    seccion = st.sidebar.radio("MENÚ", ["📅 Planeación Semanal IA", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 SOS"])

    if seccion == "📅 Planeación Semanal IA":
        st.header("Generar Planeación y Consulta")
        
        niveles = [
            "Preescolar (1°)", "Preescolar (2°)", "Preescolar (3°)",
            "Primaria (1°)", "Primaria (2°)", "Primaria (3°)", "Primaria (4°)", "Primaria (5°)", "Primaria (6°)", "Primaria Multigrado",
            "Secundaria (1°)", "Secundaria (2°)", "Secundaria (3°)", "Secundaria Multigrado"
        ]
        
        c1, c2, c3 = st.columns(3)
        nivel_sel = c1.selectbox("Nivel Educativo", niveles)
        comu = c2.text_input("Comunidad")
        eca_a = c3.text_input("ECA")
        ec_nom = c1.text_input("Nombre del EC (Educador)")
        
        tema = st.text_input("Tema de Interés (Ej. Ciclo del Agua)")
        estacion_nom = st.text_input("Nombre de Estación Permanente")
        mat1 = c2.text_input("Materia 1")
        mat2 = c3.text_input("Materia 2")

        if st.button("Generar Planeación Completa"):
            # IA genera investigación y fuentes
            invest_ia = f"Investigación semanal profunda sobre {tema}: Se analizarán propiedades, importancia y aplicaciones mediante el modelo ABCD."
            fuentes = [f"https://es.wikipedia.org/wiki/{tema.replace(' ','_')}", "https://escolares.net/", "https://libros.conaliteg.gob.mx/"]

            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, limpiar(f"Nivel: {nivel_sel} | Comunidad: {comu} | EC: {ec_nom} | ECA: {eca_a}"), 0, 1)
            pdf.ln(5)
            
            # Tabla con ajuste automático
            pdf.set_fill_color(0, 212, 255)
            pdf.cell(40, 10, "Momento", 1, 0, 'C', 1)
            pdf.cell(110, 10, "Desarrollo Semanal (IA)", 1, 0, 'C', 1)
            pdf.cell(35, 10, "Tiempo", 1, 1, 'C', 1)
            
            pdf.set_font("Arial", '', 9)
            items = [
                ["Bienvenida", "Actividades grupales diarias de integración.", "15 min/dia"],
                ["Regalo Lectura", f"Lectura semanal enfocada en {tema}.", "20 min/dia"],
                [f"Estación: {estacion_nom}", invest_ia, "90 min/dia"],
                [mat1, f"Aplicación práctica de {mat1}.", "60 min/dia"],
                [mat2, f"Ejercicios de {mat2}.", "60 min/dia"]
            ]
            
            for i in items:
                h = 15 # Altura base
                pdf.cell(40, h, limpiar(i[0]), 1)
                x, y = pdf.get_x(), pdf.get_y()
                pdf.multi_cell(110, 5, limpiar(i[1]), 1)
                pdf.set_xy(x + 110, y)
                pdf.cell(35, h, limpiar(i[2]), 1, 1)

            pdf.ln(10)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, "FUENTES DE CONSULTA:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for f in fuentes: pdf.cell(0, 7, f, 0, 1)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación Semanal", pdf_bytes, f"Planeacion_{tema}.pdf")

    elif seccion == "✍️ Diario Reflexivo":
        st.header("Diario Reflexivo")
        nom_al = st.text_input("Nombre del Alumno").upper()
        txt_diario = st.text_area("Escrito diario (Aprendizajes)")
        if st.button("Guardar Escrito"):
            if nom_al not in st.session_state.db["alumnos"]: st.session_state.db["alumnos"][nom_al] = []
            st.session_state.db["alumnos"][nom_al].append(txt_diario)
            st.success(f"Guardado. Ahora puedes buscar a {nom_al} en Evaluaciones.")

    elif seccion == "📊 Evaluación Trimestral":
        st.header("Buscador de Alumnos")
        busqueda = st.text_input("Buscar Alumno por Nombre").upper()
        if busqueda in st.session_state.db["alumnos"]:
            st.info(f"Historial encontrado: {len(st.session_state.db['alumnos'][busqueda])} escritos.")
            for e in st.session_state.db["alumnos"][busqueda]:
                st.write(f"- {e}")
            st.button("Generar Informe con IA")
        else:
            st.warning("Alumno no encontrado. Registra un escrito en el Diario primero.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
