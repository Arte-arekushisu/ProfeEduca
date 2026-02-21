import streamlit as st
from fpdf import FPDF
import datetime

# 1. ESTILO Y ANIMACIÓN
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

# 2. FUNCIONES TÉCNICAS
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
        "comentarios": [{"user": "Maestro_Gomez", "text": "¡El rincón de aprendizaje quedó genial!"}, {"user": "ECA_Lucía", "text": "Ahorro mucho tiempo en la evaluación trimestral."}]
    }

# 4. PÁGINA DE INICIO (REGISTRO Y COMUNIDAD)
if not st.session_state.db["auth"]:
    st.markdown("<h1>Planeación para el Maestro A B C D</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-style: italic;'>\"Inspirando el saber, transformando la comunidad: El eco de tu enseñanza es el futuro de todos.\"</p>", unsafe_allow_html=True)
    
    col_reg, col_com = st.columns([2, 1])
    
    with col_reg:
        st.subheader("📝 Registro de Usuario")
        with st.form("registro_maestro"):
            u_mail = st.text_input("Correo electrónico")
            u_user = st.text_input("Nombre de usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan_sel = st.radio("Suscripción Mensual", [
                "Plata ($200) - 2 Planeaciones / 2 Evaluaciones",
                "Oro ($400) - 12 Planeaciones / 12 Evaluaciones",
                "Platino ($600) - Acceso Ilimitado"
            ])
            if st.form_submit_button("REGISTRAR Y ENTRAR"):
                st.session_state.db.update({"auth": True, "user": u_user, "plan": plan_sel})
                st.rerun()

    with col_com:
        st.markdown("<div class='comment-sidebar'>", unsafe_allow_html=True)
        st.subheader("💬 Comunidad ABCD")
        for c in st.session_state.db["comentarios"]:
            st.markdown(f"<div class='comment-card'><b>{c['user']}:</b><br>{c['text']}</div>", unsafe_allow_html=True)
        with st.form("nuevo_com", clear_on_submit=True):
            n = st.text_input("Nombre")
            t = st.text_area("Comentario")
            if st.form_submit_button("Publicar"):
                st.session_state.db["comentarios"].append({"user": n, "text": t})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 5. PANEL DEL MAESTRO
else:
    st.sidebar.title("MAESTRO ABCD")
    seccion = st.sidebar.radio("MENÚ", ["📅 Planeación Semanal", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 SOS Corrección"])

    if seccion == "📅 Planeación Semanal":
        st.header("Generar Planeación ABCD")
        with st.expander("📍 Datos de Identificación", expanded=True):
            c1, c2, c3 = st.columns(3)
            comu = c1.text_input("Comunidad")
            eca_a = c2.text_input("ECA (Acompañamiento)")
            ec_nom = c3.text_input("EC (Educador Comunitario)")
            fecha = c1.date_input("Fecha de creación")

        st.subheader("Estructura Pedagógica")
        tema = st.text_input("Tema de Interés")
        estacion = st.text_input("Estación Permanente")
        rincon = st.text_input("Rincón")
        mat1 = st.text_input("Materia Post-Receso 1")
        mat2 = st.text_input("Materia Post-Receso 2")

        if st.button("Generar PDF"):
            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, limpiar(f"Comunidad: {comu} | Fecha: {fecha}"), 0, 1)
            pdf.cell(0, 8, limpiar(f"ECA: {eca_a} | EC: {ec_nom}"), 0, 1)
            pdf.ln(5)
            
            # Tabla de Tiempos Pedagógicos ABCD
            pdf.set_fill_color(0, 212, 255)
            pdf.cell(45, 10, "Momento", 1, 0, 'C', True)
            pdf.cell(100, 10, "Actividad / Desarrollo", 1, 0, 'C', True)
            pdf.cell(40, 10, "Tiempo", 1, 1, 'C', True)
            
            pdf.set_font("Arial", '', 9)
            tiempos = [
                ["Bienvenida", "Dinámica de integracion grupal", "15 min"],
                ["Regalo de Lectura", "Lectura sugerida por IA", "20 min"],
                ["Pase de Lista", "Asistencia creativa", "10 min"],
                ["Estaciones", f"Trabajo en {estacion}", "90 min"],
                ["Rincón", f"Trabajo en {rincon}", "45 min"],
                [limpiar(mat1), "Clase Post-Receso 1", "60 min"],
                [limpiar(mat2), "Clase Post-Receso 2", "60 min"]
            ]
            for f in tiempos:
                pdf.cell(45, 10, limpiar(f[0]), 1)
                pdf.cell(100, 10, limpiar(f[1]), 1)
                pdf.cell(40, 10, limpiar(f[2]), 1, 1)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación PDF", pdf_bytes, f"Planeacion_{tema}.pdf")

    elif seccion == "✍️ Diario Reflexivo":
        st.header("Escrito Diario del Alumno")
        nom_al = st.text_input("Nombre del Alumno").upper()
        txt_diario = st.text_area("Descripción de logros y actividades")
        if st.button("Guardar Escrito"):
            if nom_al not in st.session_state.db["alumnos"]: st.session_state.db["alumnos"][nom_al] = []
            st.session_state.db["alumnos"][nom_al].append(txt_diario)
            st.success("Guardado en historial trimestral.")

    elif seccion == "📊 Evaluación Trimestral":
        st.header("Evaluación Trimestral")
        busqueda = st.text_input("Buscar Alumno").upper()
        if busqueda in st.session_state.db["alumnos"]:
            st.info(f"Escritos acumulados: {len(st.session_state.db['alumnos'][busqueda])}")
            nivel = st.radio("Nivel", ["Preescolar", "Primaria"])
            
            if nivel == "Preescolar":
                st.text_area("Trayectorias (Manual)")
            else:
                st.subheader("Campos Formativos")
                c1, c2 = st.columns(2)
                c1.number_input("Lenguaje", 5, 10)
                c2.number_input("Pensamiento Científico", 5, 10)
                c1.number_input("Ética", 5, 10)
                c2.number_input("Naturaleza y Sociedades", 5, 10)
            
            st.selectbox("Nivel de Lectura/Escritura", ["Requiere apoyo", "En desarrollo", "Esperado"])
            st.text_area("Compromisos del Alumno")
            st.button("Generar Evaluación PDF")
        else:
            st.warning("Escribe el nombre registrado en el diario.")

    elif seccion == "🆘 SOS Corrección":
        st.header("SOS: Corrección IA")
        sos_t = st.text_area("Pega tu texto:")
        if st.button("Optimizar"):
            st.write("**Sugerencia:** " + limpiar(sos_t))

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
