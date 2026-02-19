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
    .glass-card { background: rgba(255, 255, 255, 0.07); border-radius: 20px; padding: 25px; border: 1px solid #00d4ff; box-shadow: 0 0 20px rgba(0,212,255,0.3); }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0 0 15px #00d4ff; }
    .slogan { text-align: center; font-style: italic; color: #e0e0e0; font-size: 20px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE SESIÓN Y LÍMITES
if 'db' not in st.session_state:
    st.session_state.db = {"auth": False, "plan": None, "user": "", "registros": 0, "reflexiones": {}}

# 3. GENERADOR DE PDF PROFESIONAL
class PDF(FPDF):
    def header_oficial(self, titulo, d, logos):
        if logos[0]: self.image(logos[0], 10, 8, 22)
        if logos[1]: self.image(logos[1], 178, 8, 22)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, titulo, 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, f"Comunidad: {d['comunidad']} | EC: {d['nombre']} | ECA: {d['eca']} | Nivel: {d['nivel']}", 0, 1, 'C')
        self.ln(10)

def crear_pdf_planeacion(d, tabla_ia, logos):
    pdf = PDF()
    pdf.add_page()
    pdf.header_oficial("PLANEACION SEMANAL DE TRABAJO", d, logos)
    # Encabezado Tabla
    pdf.set_fill_color(0, 150, 200)
    pdf.set_text_color(255)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(40, 10, "Momento/Materia", 1, 0, 'C', True)
    pdf.cell(100, 10, "Secuencia Didactica / Actividades", 1, 0, 'C', True)
    pdf.cell(50, 10, "Materiales y Enlaces", 1, 1, 'C', True)
    
    pdf.set_text_color(0)
    pdf.set_font('Arial', '', 8)
    for fila in tabla_ia:
        pdf.multi_cell(0, 7, f"{fila[0]} | {fila[1]} | {fila[2]}", border=1)
    
    pdf.ln(20)
    pdf.cell(95, 10, "Firma del Educador: ________________", 0)
    pdf.cell(95, 10, "Firma Padre/Representante APEC: ____________", 0)
    return pdf.output(dest='S').encode('latin-1')

# 4. INTERFAZ DE INICIO Y REGISTRO
if not st.session_state.db["auth"]:
    st.markdown("<h1>PROFE EDUCA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='slogan'>\"Inspirando el saber, transformando la comunidad: El eco de tu enseñanza es el futuro de todos.\"</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            email = st.text_input("Correo Electrónico para registro")
            plan = st.selectbox("Plan de Suscripción", ["Prueba 3 días (Gratis)", "Mensual ($649 MXN)", "Anual ($6,499 MXN)"])
            st.write("---")
            st.write("💳 **Pasarela de Pago Segura**")
            tarjeta = st.text_input("Número de Tarjeta", placeholder="0000 0000 0000 0000")
        with c2:
            st.info("🎯 Tu suscripción incluye:\n- Planeaciones con IA ilimitadas (Anual)\n- Reflexiones acumulativas para Evaluación\n- Soporte Técnico 24/7 con IA")
            if st.button("ACTIVAR MI CUENTA Y EMPEZAR"):
                st.session_state.db.update({"auth": True, "plan": plan, "user": email})
                st.balloons()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # PANEL DE CONTROL (NAVEGACIÓN)
    with st.sidebar:
        st.title("PROFE EDUCA")
        menu = st.radio("MENÚ", ["🏠 Inicio", "📅 Planeación", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral", "🆘 Soporte IA"])
        st.divider()
        st.write(f"Usuario: {st.session_state.db['user']}")
        if st.button("Cerrar Sesión"): st.session_state.db["auth"] = False; st.rerun()

    # --- SECCIÓN PLANEACIÓN ---
    if menu == "📅 Planeación":
        st.header("Gestor de Planeación Semanal")
        tema = st.text_input("Tema de Interés Principal")
        estacion = st.text_input("Nombre de Estación Permanente")
        m1 = st.text_input("Materia Post-Receso 1")
        m2 = st.text_input("Materia Post-Receso 2")
        
        if st.button("Generar Planeación PDF"):
            # Aquí se procesa con la IA (Simulación de tabla estructural)
            tabla_ejemplo = [
                ["Bienvenida/Lectura", "Regalo de lectura: 'Cuentos de la selva'. Actividad de bienvenida: Juego de roles.", "Libro SEP / 30m"],
                ["Pase de Lista", "Dinámica: Menciona un animal que empiece con la inicial de tu nombre.", "Lista EC / 10m"],
                ["Estación Permanente", f"Trabajo en la estación: {estacion}. Actividades de refuerzo autónomo.", "Material didáctico / 90m"],
                [f"{m1} / {m2}", "Desarrollo de contenidos técnicos y ejercicios prácticos.", "Cuadernos / 120m"]
            ]
            pdf_out = crear_pdf_planeacion({"comunidad":"X","nombre":"Y","eca":"Z","nivel":"Primaria"}, tabla_ejemplo, [None, None])
            st.download_button("📥 DESCARGAR PLANEACIÓN (PDF)", pdf_out, "Planeacion_ProfeEduca.pdf")

    # --- SECCIÓN REFLEXIÓN ---
    elif menu == "✍️ Reflexión Diaria":
        st.header("Diario Reflexivo por Alumno")
        alumno = st.text_input("Nombre del Alumno")
        temas_int = st.text_input("Temas de interés observados")
        notas = st.text_area("Descripción breve de actividades y logros del día")
        if st.button("Guardar en Memoria Trimestral"):
            if alumno not in st.session_state.db["reflexiones"]: st.session_state.db["reflexiones"][alumno] = []
            st.session_state.db["reflexiones"][alumno].append({"fecha": str(datetime.date.today()), "nota": notas, "interes": temas_int})
            st.success(f"Registro guardado. Juan Pérez tiene {len(st.session_state.db['reflexiones'][alumno])} reflexiones este trimestre.")

    # --- SECCIÓN EVALUACIÓN ---
    elif menu == "📊 Evaluación Trimestral":
        st.header("Generador de Evaluación Trimestral")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        alumno_sel = st.selectbox("Seleccionar Alumno", list(st.session_state.db["reflexiones"].keys()))
        
        if nivel == "Primaria":
            st.write("### Campos Formativos (Calificación Manual)")
            col1, col2 = st.columns(2)
            with col1: st.number_input("Lenguajes", 5, 10); st.number_input("Ética, Nat. y Soc.", 5, 10)
            with col2: st.number_input("Saberes y PC", 5, 10); st.number_input("De lo Humano", 5, 10)
        elif nivel == "Secundaria":
            st.write("### Calificaciones por Asignatura")
            st.text_input("Español"); st.text_input("Matemáticas"); st.text_input("Ciencias")

        if st.button("Generar Evaluación PDF"):
            st.info("Analizando reflexiones trimestrales para redactar escrito evaluatorio...")
            # Aquí la IA redacta basado en las 'notas' guardadas anteriormente.
