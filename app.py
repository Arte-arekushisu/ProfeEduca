import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

# Inicialización de estados
if "autenticado" not in st.session_state:
    st.session_state.autenticado = True
if "p" not in st.session_state:
    st.session_state.p = "inicio"

# --- 2. UTILIDADES Y PDF ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class MaestroPDF(FPDF):
    def header_estilo(self, titulo, color=(128, 0, 0)):
        self.set_fill_color(*color)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, datos):
        self.set_text_color(0, 0, 0); self.set_font('Helvetica', 'B', 10); self.set_fill_color(240, 240, 240)
        for i, (k, v) in enumerate(datos.items()):
            self.cell(95, 8, clean(f" {k}: {v}"), 1, (i % 2), 'L', True)
        self.ln(10)

# --- 3. ESTILOS CSS (FASE 0.1, 0.2 y 0.3) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Animación del Gusanito (Fase 0.2/0.3) */
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
    }
    .apple-container { font-size: 100px; text-align: center; position: relative; }
    .worm-icon { position: absolute; font-size: 40px; animation: worm-move 3s infinite ease-in-out; }
    
    .brand-header { font-size: 3rem; font-weight: 800; color: #38bdf8; text-shadow: 0 0 15px rgba(56,189,248,0.5); }
    .slogan-final { font-style: italic; color: #94a3b8; margin-top: 20px; font-size: 1.1rem; }
    
    /* Botón Cerrar Sesión Rojo */
    .stButton>button[kind="secondary"] { background-color: #ef4444 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Lógica de Seguridad
if not st.session_state.autenticado:
    st.error("🔒 Sesión Cerrada.")
    if st.button("Reingresar"):
        st.session_state.autenticado = True
        st.rerun()
    st.stop()

# --- 4. BARRA LATERAL (NAVEGACIÓN) ---
with st.sidebar:
    st.markdown("### 🍎 Panel ProfeEduca")
    nombre_ec = st.text_input("EC", "AXEL REYES")
    comunidad = st.text_input("Comunidad", "CRUZ")
    
    st.divider()
    # Botones de navegación (Estilo Fase 0.3)
    if st.button("🏠 Inicio", use_container_width=True): st.session_state.p = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.p = "planeacion"
    if st.button("👤 Escrito Reflexivo", use_container_width=True): st.session_state.p = "reflexivo"
    if st.button("📊 Evaluación", use_container_width=True): st.session_state.p = "evaluacion"
    if st.button("🧾 Facturación", use_container_width=True): st.session_state.p = "facturacion"
    
    st.divider()
    if st.button("🔒 CERRAR SESIÓN", type="secondary", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# --- 5. CONTENIDO DINÁMICO (LA FASE 0.3 EN ACCIÓN) ---

if st.session_state.p == "inicio":
    # Layout de la Fase 0.3: Visual a la derecha, Bienvenida a la izquierda
    col_txt, col_vis = st.columns([1, 1])
    
    with col_txt:
        st.markdown(f"<div class='brand-header'>📏 ProfeEduca ✏️</div>", unsafe_allow_html=True)
        st.subheader(f"Bienvenido, Maestro {nombre_ec}")
        st.write("Sistema integral para el registro de planeaciones, evaluaciones y seguimiento de alumnos en comunidades ABCD.")
        st.info("Utiliza el menú lateral para acceder a los módulos.")

    with col_vis:
        st.markdown("""
            <div class="apple-container">
                <span class="worm-icon">🐛</span>🍎
            </div>
            <div class="slogan-final">
                "Guía de luz en las comunidades más remotas, transformando cada desafío en una oportunidad para el México del mañana."
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.p == "planeacion":
    st.header("📝 Planeación Semanal ABCD")
    # Lógica de la Fase 0.5 integrada
    fecha = st.date_input("Semana del:", datetime.date.today())
    materia = st.text_input("Materia Principal")
    actividad = st.text_area("Descripción de la Actividad")
    
    if st.button("🔨 Generar PDF"):
        pdf = MaestroPDF()
        pdf.add_page()
        pdf.header_estilo("PLANEACION SEMANAL")
        pdf.tabla_datos({"EC": nombre_ec, "COMUNIDAD": comunidad, "FECHA": str(fecha)})
        pdf.set_font("Helvetica", "B", 12); pdf.cell(0, 10, clean(materia), 0, 1)
        pdf.set_font("Helvetica", "", 11); pdf.multi_cell(0, 6, clean(actividad))
        st.download_button("📥 Descargar", data=bytes(pdf.output()), file_name="Planeacion.pdf")

elif st.session_state.p == "reflexivo":
    st.header("👤 Escrito Reflexivo (Fase 0.4)")
    alumno = st.text_input("Nombre del Alumno")
    obs = st.text_area("Observaciones del día")
    if st.button("💾 Guardar Registro"):
        st.success(f"Registro guardado para {alumno}")

elif st.session_state.p == "evaluacion":
    st.header("📊 Evaluación Trimestral (Fase 0.7)")
    # Integración de campos formativos
    c1, c2 = st.columns(2)
    l_avance = c1.text_area("Lenguajes")
    s_avance = c2.text_area("Saberes y P.C.")
    
    if st.button("🚀 Generar Reporte"):
        pdf = MaestroPDF()
        pdf.add_page()
        pdf.header_estilo("REPORTE DE EVALUACION", (0, 51, 102))
        pdf.tabla_datos({"ALUMNO": "Estudiante", "EC": nombre_ec})
        pdf.set_font("Helvetica", "B", 11); pdf.cell(0, 8, "LENGUAJES", 1, 1, 'L', True)
        pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 5, clean(l_avance), 1)
        st.download_button("📥 Descargar Reporte", data=bytes(pdf.output()), file_name="Evaluacion.pdf")
