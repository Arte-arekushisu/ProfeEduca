import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
st.set_page_config(page_title="Planeación Maestro ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-section { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; }
    .comment-box { background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE SESIÓN Y DATOS
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user_data = {}
    st.session_state.comments = [
        {"user": "Educador_Comunitario", "text": "El modelo ABCD ahora es mucho más fácil de organizar."},
        {"user": "Profe_Axel", "text": "Las estaciones permanentes quedan muy bien estructuradas."}
    ]

# 3. INTERFAZ DE REGISTRO Y LOGIN
if not st.session_state.auth:
    st.markdown("<h1>Planeación para el Maestro A B C D</h1>", unsafe_allow_html=True)
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("📝 Registro y Suscripción")
        with st.form("registro_maestro"):
            u_email = st.text_input("Correo Electrónico")
            u_name = st.text_input("Nombre de Usuario")
            u_pass = st.text_input("Contraseña", type="password")
            u_plan = st.radio("Elige tu Plan Mensual:", [
                "Plata ($200) - 2 Planeaciones/Escritos",
                "Oro ($400) - 12 Planeaciones/Escritos",
                "Platino ($600) - Acceso Ilimitado"
            ])
            if st.form_submit_button("Registrar y Activar"):
                st.session_state.auth = True
                st.session_state.user_data = {"name": u_name, "plan": u_plan}
                st.rerun()

    with col_side:
        st.markdown("<div class='comment-section'>", unsafe_allow_html=True)
        st.subheader("💬 Comunidad ABCD")
        for c in st.session_state.comments:
            st.markdown(f"<div class='comment-box'><b>{c['user']}:</b><br>{c['text']}</div>", unsafe_allow_html=True)
        
        st.write("---")
        st.write("¿Tienes un comentario?")
        with st.form("nuevo_comentario", clear_on_submit=True):
            n_name = st.text_input("Tu nombre")
            n_text = st.text_area("Tu experiencia")
            if st.form_submit_button("Publicar"):
                st.session_state.comments.append({"user": n_name, "text": n_text})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 4. PANEL DE CONTROL (MODELO ABCD)
else:
    st.sidebar.title("MENU ABCD")
    opcion = st.sidebar.radio("Ir a:", ["📅 Planeación ABCD", "📊 Evaluaciones Trimestrales", "✍️ Diario Reflexivo", "🆘 SOS Corrección"])
    
    if opcion == "📅 Planeación ABCD":
        st.header("Generación de Planeación Semanal (Modelo ABCD)")
        c1, c2 = st.columns(2)
        with c1:
            tema = st.text_input("Tema de Interés", value="Tortugas Marinas")
            estacion = st.text_input("Estación Permanente")
            rincon = st.text_input("Rincón")
        with c2:
            m1 = st.text_input("Materia Post-Receso (Hora 1)")
            m2 = st.text_input("Materia Post-Receso (Hora 2)")
        
        if st.button("Generar Planeación PDF"):
            st.info("La IA está estructurando: Bienvenida, Regalo de lectura, Pase de lista y Estaciones...")
            st.success("Planeación generada siguiendo los tiempos pedagógicos de CONAFE.")
            st.download_button("📥 Descargar PDF Inalterable", "CONTENIDO_PDF", f"Planeacion_{tema}.pdf")

    elif opcion == "📊 Evaluaciones Trimestrales":
        st.header("Evaluación Trimestral por Campos Formativos")
        nivel = st.selectbox("Selecciona Nivel", ["Preescolar (Trayectorias)", "Primaria (4 Campos Formativos)", "Secundaria"])
        
        if nivel == "Primaria (4 Campos Formativos)":
            st.write("### Datos de Alumno")
            st.text_input("Nombre del Alumno")
            st.selectbox("Nivel de Lectura", ["Requiere apoyo", "En desarrollo", "Nivel esperado"])
            st.selectbox("Nivel de Escritura", ["Silábico", "Silábico-Alfabético", "Alfabético"])
            st.text_area("Compromisos del Alumno")
        
        st.button("Generar Informe Trimestral")

    elif opcion == "🆘 SOS Corrección":
        st.header("Centro de Ayuda y Corrección")
        texto_sos = st.text_area("Pega aquí el texto que deseas que la IA corrija:")
        if st.button("Corregir Errores"):
            st.write("**Sugerencia de la IA:** Texto corregido y alineado al modelo pedagógico.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.auth = False
        st.rerun()
