import streamlit as st
from fpdf import FPDF
import unicodedata
import datetime
import io
import time

# --- 1. CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="ProfeEduca | Sistema Integral", page_icon="🍎", layout="wide")

# Inicialización del "Cerebro" del sistema para no perder la fase actual
if "fase" not in st.session_state:
    st.session_state.fase = "LOGIN"
if "usuario" not in st.session_state:
    st.session_state.usuario = {"name": "Maestro Axel", "comunidad": "CRUZ"}

# --- 2. ESTILOS CSS (Fusión de todas las fases) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Tarjetas de la Fase 0.1 */
    .plan-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #38bdf8;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
    }
    
    /* Animación Gusanito Fase 0.2/0.3 */
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
    }
    .apple-container { font-size: 100px; text-align: center; position: relative; }
    .worm-icon { position: absolute; font-size: 40px; animation: worm-move 3s infinite ease-in-out; }
    
    /* Botón Cerrar Sesión Rojo */
    .stButton>button[kind="secondary"] { background-color: #ef4444 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES PDF (Fase 0.4 - 0.7) ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ProfePDF(FPDF):
    def header_institucional(self, titulo, color=(128, 0, 0)):
        self.set_fill_color(*color)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean(titulo), 0, 1, 'C')
        self.ln(10)

# --- 4. NAVEGACIÓN POR FASES (Lógica Real) ---

# --- FASE 0.1: EL LOGIN / SELECCIÓN ---
if st.session_state.fase == "LOGIN":
    st.markdown("<h1 style='text-align: center;'>🍎 BIENVENIDO A PROFEEDUCA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown('<div class="plan-card"><h3>Acceso al Sistema</h3><p>Introduce tus credenciales de Educador</p></div>', unsafe_allow_html=True)
        user = st.text_input("Usuario")
        if st.button("INGRESAR AL DASHBOARD", use_container_width=True):
            st.session_state.fase = "DASHBOARD"
            st.rerun()

# --- FASE 0.3: EL DASHBOARD PRINCIPAL ---
elif st.session_state.fase == "DASHBOARD":
    with st.sidebar:
        st.markdown("## ⚙️ Menú")
        if st.button("🏠 Inicio"): st.session_state.fase = "DASHBOARD"
        if st.button("📝 Planeaciones"): st.session_state.fase = "PLANEACION"
        if st.button("📊 Evaluaciones"): st.session_state.fase = "EVALUACION"
        st.divider()
        if st.button("🔒 CERRAR SESIÓN", type="secondary"):
            st.session_state.fase = "LOGIN"
            st.rerun()

    # Layout de la Fase 0.3 (Texto izq, Visual der)
    c_txt, c_vis = st.columns([1, 1])
    with c_txt:
        st.title(f"Panel de {st.session_state.usuario['name']}")
        st.write("Selecciona una herramienta para trabajar hoy.")
        # Tarjetas de estado
        st.info("✅ Tienes 3 planeaciones pendientes.")
        st.warning("⚠️ 1 evaluación requiere firma.")
        
    with c_vis:
        st.markdown('<div class="apple-container"><span class="worm-icon">🐛</span>🍎</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><i>'Transformando comunidades'</i></p>", unsafe_allow_html=True)

# --- FASE 0.5: PLANEACIÓN ---
elif st.session_state.fase == "PLANEACION":
    if st.sidebar.button("⬅️ Volver"): st.session_state.fase = "DASHBOARD"; st.rerun()
    st.header("📝 Módulo de Planeación ABCD")
    
    with st.form("form_p"):
        materia = st.text_input("Materia")
        plan = st.text_area("Desarrollo de la sesión")
        if st.form_submit_button("Generar PDF"):
            pdf = ProfePDF()
            pdf.add_page()
            pdf.header_institucional("PLANEACION SEMANAL")
            pdf.set_font("Helvetica", "", 12)
            pdf.multi_cell(0, 10, clean(f"Materia: {materia}\n\n{plan}"))
            st.download_button("Descargar", data=bytes(pdf.output()), file_name="Plan.pdf")

# --- FASE 0.7: EVALUACIÓN ---
elif st.session_state.fase == "EVALUACION":
    if st.sidebar.button("⬅️ Volver"): st.session_state.fase = "DASHBOARD"; st.rerun()
    st.header("📊 Evaluación Trimestral")
    # Aquí iría toda la lógica de los 4 campos formativos...
    st.write("Módulo de evaluación cargado correctamente.")
