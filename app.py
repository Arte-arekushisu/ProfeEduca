import streamlit as st
from fpdf import FPDF
import datetime

# 1. ESTILO VISUAL MEJORADO
st.set_page_config(page_title="Planeación Maestro ABCD", page_icon="🍎", layout="wide")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 10s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-sidebar { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; text-shadow: 0 0 10px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE APOYO (PDF Y LIMPIEZA)
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'PLANEACION SEMANAL MAESTRO ABCD', 0, 1, 'C')
        self.ln(5)

# 3. BASE DE DATOS LOCAL
if 'db' not in st.session_state:
    st.session_state.db = {"auth": False, "user": "", "plan": "", "alumnos": {}, "comentarios": []}

# 4. LÓGICA DE ACCESO
if not st.session_state.db["auth"]:
    st.markdown("<h1>Planeación para el Maestro A B C D</h1>")
    col_reg, col_com = st.columns([2, 1])
    with col_reg:
        with st.form("registro"):
            u_name = st.text_input("Nombre de Usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan = st.radio("Plan", ["Plata ($200)", "Oro ($400)", "Platino ($600)"])
            if st.form_submit_button("INGRESAR"):
                st.session_state.db.update({"auth": True, "user": u_name, "plan": plan})
                st.rerun()
else:
    # 5. PANEL DE CONTROL
    st.sidebar.title(f"EC: {st.session_state.db['user']}")
    menu = st.sidebar.radio("MENÚ", ["📅 Planeación Semanal IA", "📊 Evaluación", "🆘 SOS"])

    if menu == "📅 Planeación Semanal IA":
        st.header("Generador de Investigación Extensa")
        c1, c2 = st.columns(2)
        comu = c1.text_input("Comunidad")
        eca = c2.text_input("ECA")
        tema = st.text_input("Tema de Investigación (Semanal)", placeholder="Ej: El Sistema Solar o Ciclo del Agua")
        estacion = st.text_input("Estación Permanente")
        mat1 = c1.text_input("Materia 1")
        mat2 = c2.text_input("Materia 2")

        if st.button("Generar Planeación y Fuentes de Investigación"):
            # LÓGICA DE GENERACIÓN EXTENSA (Simulada para el ejemplo)
            investigacion_extensa = f"Secuencia Didáctica: {tema}. \nLunes: Introducción. Martes: Desarrollo. Miércoles: Experimentación..."
            fuentes = [
                f"https://es.wikipedia.org/wiki/{tema.replace(' ', '_')}",
                f"https://escolares.net/buscar?q={tema.replace(' ', '+')}",
                "https://www.biografiasyvidas.com/"
            ]

            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, limpiar(f"Comunidad: {comu} | EC: {st.session_state.db['user']} | ECA: {eca}"), 0, 1)
            pdf.ln(5)

            # Tabla de Momentos (Mejorada para que no se encime)
            pdf.set_fill_color(0, 212, 255)
            pdf.cell(40, 10, "Momento", 1, 0, 'C', True)
            pdf.cell(110, 10, "Actividad de la Semana (IA)", 1, 0, 'C', True)
            pdf.cell(35, 10, "Tiempo", 1, 1, 'C', True)
            
            pdf.set_font("Arial", '', 9)
            rows = [
                ["Bienvenida", "Dinámica: El barco se hunde adaptado al tema.", "15 min/dia"],
                ["Regalo Lectura", f"Lecturas diarias sobre {tema} (Libros del rincon).", "20 min/dia"],
                [f"Estación: {estacion}", f"Investigacion profunda: {investigacion_extensa[:80]}...", "90 min/dia"],
                [mat1, f"Aplicacion matematica de {tema}.", "60 min/dia"],
                [mat2, f"Analisis de textos sobre {tema}.", "60 min/dia"]
            ]
            
            for r in rows:
                pdf.cell(40, 15, limpiar(r[0]), 1)
                # Multi_cell para que el texto largo no choque con la columna de tiempo
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.multi_cell(110, 5, limpiar(r[1]), border=1)
                pdf.set_xy(x + 110, y)
                pdf.cell(35, 15, limpiar(r[2]), 1, 1)

            # SECCIÓN DE ENLACES
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, "FUENTES DE INVESTIGACION (ENLACES):", 0, 1)
            pdf.set_font("Arial", '', 9)
            pdf.set_text_color(0, 0, 255) # Azul para links
            for link in fuentes:
                pdf.cell(0, 7, link, 0, 1)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación Extensa", pdf_bytes, f"Semana_{tema}.pdf")

    elif menu == "📊 Evaluación":
        st.write("Sección de Evaluación Trimestral")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
