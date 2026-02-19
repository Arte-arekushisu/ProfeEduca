import streamlit as st
import requests
from io import BytesIO
from fpdf import FPDF # Necesitas instalar: pip install fpdf
from PIL import Image
import time

# 1. ESTÉTICA DINÁMICA (NEÓN Y MOVIMIENTO)
st.set_page_config(page_title="Profe.Educa SaaS", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #e2e8f0; }
    h1 { background: -webkit-linear-gradient(#00d4ff, #0055ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3em; text-align: center; font-weight: bold; }
    .card { background: rgba(255, 255, 255, 0.03); border-radius: 15px; padding: 20px; border: 1px solid #00d4ff; box-shadow: 0 0 15px rgba(0,212,255,0.2); }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGICA DE SUSCRIPCIONES Y USUARIOS
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"auth": False, "plan": "Ninguno", "registros": 0}

def check_limit(tipo_plan):
    if tipo_plan == "Gratis" and st.session_state.user_data["registros"] >= 1: return False
    if tipo_plan == "Mensual" and st.session_state.user_data["registros"] >= 10: return False
    return True

# 3. GENERADOR DE PDF PROFESIONAL
class PDF(FPDF):
    def header_oficial(self, titulo, d, l1=None, l2=None):
        if l1: self.image(l1, 10, 8, 25)
        if l2: self.image(l2, 175, 8, 25)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, titulo, 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f"Comunidad: {d['comunidad']} | EC: {d['nombre']} | Nivel: {d['nivel']}", 0, 1, 'C')
        self.ln(10)

def crear_pdf_planeacion(d, contenido_ia, logos):
    pdf = PDF()
    pdf.add_page()
    pdf.header_oficial("PLANEACIÓN SEMANAL", d, logos[0], logos[1])
    
    # Tabla de Tiempos Pedagógicos
    pdf.set_fill_color(0, 212, 255)
    pdf.set_text_color(255)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, "Actividad", 1, 0, 'C', True)
    pdf.cell(90, 10, "Desarrollo", 1, 0, 'C', True)
    pdf.cell(35, 10, "Materiales", 1, 0, 'C', True)
    pdf.cell(25, 10, "Tiempo", 1, 1, 'C', True)
    
    pdf.set_text_color(0)
    pdf.set_font('Arial', '', 9)
    # Lógica de procesamiento de IA para filas del PDF
    for fila in contenido_ia.split('\n'):
        if '|' in fila:
            p = fila.split('|')
            if len(p) >= 4:
                pdf.multi_cell(0, 10, f"{p[0][:20]} | {p[1][:50]}... | {p[2][:15]} | {p[3]}", border=1)
                
    pdf.ln(20)
    pdf.cell(90, 10, "Firma del Educador: ________________", 0)
    pdf.cell(90, 10, "Firma Padre/APEC: ________________", 0)
    return pdf.output(dest='S').encode('latin-1')

# 4. INTERFAZ DE REGISTRO Y PAGOS
with st.sidebar:
    st.title("🛡️ Profe.Educa SaaS")
    if not st.session_state.user_data["auth"]:
        st.subheader("Registrarse")
        email = st.text_input("Correo Electrónico")
        plan = st.radio("Plan:", ["Gratis (3 días)", "Mensual ($649)", "Anual ($6,499)"])
        if st.button("Pagar y Registrar"):
            st.session_state.user_data = {"auth": True, "plan": plan, "registros": 0}
            st.success("¡Bienvenido! Pago procesado.")
            st.rerun()
    else:
        st.write(f"Plan: **{st.session_state.user_data['plan']}**")
        seccion = st.radio("Gestión:", ["Inicio", "Planeación", "Reflexión", "Evaluación", "Asistencia IA"])

# 5. CONTENIDO POR SECCIONES
if st.session_state.user_data["auth"]:
    if seccion == "Planeación":
        st.header("📅 Nueva Planeación Semanal")
        tema = st.text_input("Tema de Interés")
        materias = st.multiselect("Materias Post-Receso (2 por hora)", ["Matemáticas", "Español", "Ciencias", "Historia", "Artes"])
        
        if st.button("Generar PDF"):
            if check_limit(st.session_state.user_data["plan"]):
                prompt = f"Crea planeación para {tema} con {materias}. Formato tabla '|'."
                # Aquí llamarías a la IA real. Simulación:
                res = "Bienvenida | Dinámica grupal | Música | 15m\nPase de Lista | Dinámica de nombres | Lista | 5m\nRegalo Lectura | Cuento clásico | Libro | 20m\nRelación Tutora | Estación de trabajo | Fichas | 90m"
                pdf_data = crear_pdf_planeacion({"comunidad": "X", "nombre": "Y", "nivel": "Primaria"}, res, [None, None])
                st.download_button("📥 Descargar PDF Oficial", pdf_data, "Planeacion.pdf")
                st.session_state.user_data["registros"] += 1
            else:
                st.error("Has alcanzado el límite de tu plan.")

    elif seccion == "Evaluación":
        st.header("📊 Evaluación Trimestral")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        
        if nivel == "Primaria":
            col1, col2 = st.columns(2)
            with col1: st.number_input("Lenguajes", 5, 10); st.number_input("Saberes", 5, 10)
            with col2: st.number_input("Ética", 5, 10); st.number_input("De lo Humano", 5, 10)
        elif nivel == "Secundaria":
            # Mostrar todas las materias individuales
            st.text_input("Calificación Español")
            st.text_input("Calificación Matemáticas")
        
        st.file_uploader("Subir Logos para el PDF")
        st.button("Generar Evaluación PDF")

    elif seccion == "Asistencia IA":
        st.header("🆘 Soporte Técnico Premium")
        if st.session_state.user_data["plan"] == "Anual ($6,499)":
            st.write("Soporte IA 24/7 disponible para ti.")
            duda = st.text_input("¿En qué te ayudo?")
            st.button("Consultar IA")
        else:
            st.warning("El soporte técnico por IA solo está disponible en el Plan Anual.")

# 6. PANEL DE CONTROL (SOLO PARA TI)
if st.sidebar.checkbox("Admin Panel"):
    st.subheader("Control Maestro")
    st.write("Aquí puedes ver las métricas de ventas y corregir documentos.")
    st.text_input("Clave Interbancaria de Destino", value="0123456789...")
