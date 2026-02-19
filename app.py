import streamlit as st
import requests
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import datetime

# 1. ESTILO VISUAL DINÁMICO (MOVIMIENTO Y NEÓN)
st.set_page_config(page_title="Profe Educa", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp {
        background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505);
        background-size: 400% 400%;
        animation: move 12s ease infinite;
        color: white;
    }
    .glass-card { background: rgba(255, 255, 255, 0.07); border-radius: 20px; padding: 25px; border: 1px solid #00d4ff; }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Impact'; font-size: 60px; text-shadow: 0 0 20px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE USUARIOS Y PLANES (BASE DE DATOS SIMULADA)
if 'db' not in st.session_state:
    st.session_state.db = {"auth": False, "plan": None, "registros": 0, "notas": {}}

# 3. GENERADOR DE PDF PROFESIONAL (PDF INALTERABLE)
class PDF(FPDF):
    def header_oficial(self, titulo, d, logos=None):
        if logos and logos[0]: self.image(logos[0], 10, 8, 25)
        if logos and logos[1]: self.image(logos[1], 175, 8, 25)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, titulo, 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f"Comunidad: {d['comunidad']} | EC: {d['nombre']} | Nivel: {d['nivel']}", 0, 1, 'C')
        self.ln(10)

def crear_pdf_planeacion(d, contenido_ia, logos):
    pdf = PDF()
    pdf.add_page()
    pdf.header_oficial("PLANEACION SEMANAL", d, logos)
    # Estructura de Tabla
    pdf.set_fill_color(0, 212, 255)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(45, 10, "Momento", 1, 0, 'C', True)
    pdf.cell(90, 10, "Desarrollo y Actividades", 1, 0, 'C', True)
    pdf.cell(55, 10, "Materiales / Tiempo", 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 9)
    # Lógica de filas (Bienvenida, Pase Lista, Regalo Lectura, Estación, Materias)
    for linea in contenido_ia.split('\n'):
        if '|' in linea:
            p = linea.split('|')
            pdf.multi_cell(0, 8, f"{p[0]} | {p[1]} | {p[2]}", border=1)
    
    pdf.ln(10)
    pdf.cell(95, 10, "Firma Educador: ________________", 0)
    pdf.cell(95, 10, "Firma Padre/APEC: _______________", 0)
    return pdf.output(dest='S').encode('latin-1')

# 4. INTERFAZ DE REGISTRO Y PAGOS
if not st.session_state.db["auth"]:
    st.markdown("<h1>PROFE EDUCA</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Correo Electrónico")
            plan = st.selectbox("Selecciona tu Plan", ["Prueba 3 días ($0)", "Mensual ($649)", "Anual ($6,499)"])
        with col2:
            st.write("### Método de Pago")
            st.text_input("Número de Tarjeta (16 dígitos)")
            st.button("PAGAR Y ACTIVAR CUENTA", on_click=lambda: st.session_state.db.update({"auth": True, "plan": plan}))
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # PANEL PRINCIPAL
    with st.sidebar:
        st.title("PROFE EDUCA")
        seccion = st.radio("NAVEGACIÓN", ["🏠 Inicio", "📅 Planeación", "✍️ Reflexión Diaria", "📊 Evaluación", "🆘 Ayuda"])
        st.divider()
        if st.button("Cerrar Sesión"): st.session_state.db["auth"] = False; st.rerun()

    if seccion == "📅 Planeación":
        st.header("Gestor de Planeación Semanal")
        tema = st.text_input("Tema de Interés")
        estacion = st.text_input("Estación Permanente")
        m1 = st.text_input("Materia Post-Receso 1")
        m2 = st.text_input("Materia Post-Receso 2")
        
        if st.button("Generar Planeación con IA"):
            # Lógica de límites por plan
            prompt = f"Genera tabla para {tema} con bienvenida, pase lista, regalo lectura, estación {estacion} y materias {m1}, {m2}."
            res = "Bienvenida | Dinámica lúdica | 10m\nPase de Lista | Temática creativa | 5m\nRegalo Lectura | Texto sugerido | 15m\nEstación | Actividades IA | 90m\nMaterias | Ejercicios IA | 60m"
            st.markdown(res)
            st.download_button("📥 Descargar PDF para Imprimir", crear_pdf_planeacion({"comunidad":"X","nombre":"Y","nivel":"Z"}, res, [None, None]), "Planeacion.pdf")

    elif seccion == "✍️ Reflexión Diaria":
        st.header("Bitácora del Alumno")
        nombre_al = st.text_input("Nombre del Alumno")
        actividades = st.text_area("Descripción de actividades y temas aprendidos")
        if st.button("Guardar Registro"):
            if nombre_al not in st.session_state.db["notas"]: st.session_state.db["notas"][nombre_al] = []
            st.session_state.db["notas"][nombre_al].append(actividades)
            st.success("Guardado en el historial trimestral.")

    elif seccion == "📊 Evaluación":
        st.header("Evaluación Trimestral")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        alumno = st.selectbox("Seleccionar Alumno", list(st.session_state.db["notas"].keys()))
        
        if nivel == "Primaria":
            col1, col2 = st.columns(2)
            with col1: st.number_input("Lenguajes", 5, 10); st.number_input("Ética, Nat y Soc", 5, 10)
            with col2: st.number_input("Saberes y PC", 5, 10); st.number_input("De lo Humano", 5, 10)
        elif nivel == "Secundaria":
            st.write("Calificaciones por Materia (Español, Matemáticas, Ciencias, etc.)")
            st.number_input("Matemáticas", 5, 10)
        
        st.button("Generar Evaluación PDF con IA")
