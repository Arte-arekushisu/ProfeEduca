import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Planeación Maestro ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 12s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-sidebar { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; min-height: 600px; }
    .comment-card { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #00d4ff; font-size: 0.85em; }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES TÉCNICAS Y LÓGICA DE IA
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PLANEACION PARA EL MAESTRO A B C D', 0, 1, 'C')
        self.ln(5)

# 3. BASE DE DATOS DE SESIÓN
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user": "", "plan": "", 
        "alumnos": {}, 
        "comentarios": [{"user": "Maestro_Gomez", "text": "¡Las actividades de las estaciones son muy creativas!"}, {"user": "ECA_Lucía", "text": "La IA realmente entiende el modelo CONAFE."}]
    }

# 4. PÁGINA DE INICIO
if not st.session_state.db["auth"]:
    st.markdown("<h1>Planeación para el Maestro A B C D</h1>", unsafe_allow_html=True)
    col_reg, col_com = st.columns([2, 1])
    
    with col_reg:
        st.subheader("📝 Registro de Usuario")
        with st.form("registro_maestro"):
            u_mail = st.text_input("Correo electrónico")
            u_user = st.text_input("Nombre de usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan_sel = st.radio("Suscripción Mensual", ["Plata ($200)", "Oro ($400)", "Platino ($600)"])
            if st.form_submit_button("REGISTRAR Y ENTRAR"):
                st.session_state.db.update({"auth": True, "user": u_user, "plan": plan_sel})
                st.rerun()

    with col_com:
        st.markdown("<div class='comment-sidebar'>", unsafe_allow_html=True)
        st.subheader("💬 Comunidad ABCD")
        for c in st.session_state.db["comentarios"]:
            st.markdown(f"<div class='comment-card'><b>{c['user']}:</b><br>{c['text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# 5. PANEL DEL MAESTRO
else:
    st.sidebar.title("MAESTRO ABCD")
    seccion = st.sidebar.radio("MENÚ", ["📅 Planeación Semanal", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 SOS"])

    if seccion == "📅 Planeación Semanal":
        st.header("Generar Planeación con IA")
        c1, c2, c3 = st.columns(3)
        comu = c1.text_input("Comunidad")
        eca_a = c2.text_input("ECA (Acompañamiento)")
        ec_nom = c3.text_input("EC (Educador Comunitario)")
        
        tema = st.text_input("Tema de Interés (Ej. Las Plantas)")
        estacion_nom = st.text_input("Nombre de tu Estación Permanente")
        mat1 = st.text_input("Materia Post-Receso 1")
        mat2 = st.text_input("Materia Post-Receso 2")

        if st.button("Generar Planeación Completa con IA"):
            # SIMULACIÓN DE GENERACIÓN DE IA PARA ESTACIONES
            act_estacion = f"Investigación guiada sobre {tema} usando material concreto en la estación {estacion_nom}."
            act_rincon = f"Creación de un mural colectivo sobre {tema} integrando saberes previos."
            
            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, limpiar(f"Comunidad: {comu} | EC: {ec_nom} | ECA: {eca_a}"), 0, 1)
            pdf.ln(5)
            
            tiempos = [
                ["Momento", "Actividad Sugerida por IA", "Tiempo"],
                ["Bienvenida", "Dinámica de confianza relacionada al tema", "15 min"],
                ["Regalo Lectura", f"Lectura de un cuento sobre {tema}", "20 min"],
                ["Pase de Lista", "Pregunta detonadora del dia", "10 min"],
                [f"Estación: {estacion_nom}", act_estacion, "90 min"],
                ["Rincón", act_rincon, "45 min"],
                [mat1, f"Ejercicios prácticos de {mat1}", "60 min"],
                [mat2, f"Resolución de problemas de {mat2}", "60 min"]
            ]
            
            for f in tiempos:
                pdf.cell(45, 10, limpiar(f[0]), 1)
                pdf.cell(100, 10, limpiar(f[1]), 1)
                pdf.cell(40, 10, limpiar(f[2]), 1, 1)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación PDF", pdf_bytes, f"Planeacion_{tema}.pdf")

    # Resto de secciones (Diario, Evaluación, SOS) se mantienen igual...
    elif seccion == "✍️ Diario Reflexivo":
        st.header("Diario Reflexivo")
        nom_al = st.text_input("Nombre del Alumno").upper()
        txt_diario = st.text_area("¿Qué aprendió hoy?")
        if st.button("Guardar"):
            if nom_al not in st.session_state.db["alumnos"]: st.session_state.db["alumnos"][nom_al] = []
            st.session_state.db["alumnos"][nom_al].append(txt_diario)
            st.success("Guardado.")

    elif seccion == "📊 Evaluación Trimestral":
        st.header("Evaluación Trimestral")
        busqueda = st.text_input("Buscar Alumno").upper()
        if busqueda in st.session_state.db["alumnos"]:
            st.info(f"Escritos registrados: {len(st.session_state.db['alumnos'][busqueda])}")
            st.button("Redactar Evaluación Trimestral con IA")
        else:
            st.warning("Alumno no encontrado.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
