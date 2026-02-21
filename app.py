import streamlit as st
import random
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ProfeEduca V0.5", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS (DISEÑO GLASSMISM Y BOTONES SUAVES) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Botones transparentes y relajantes */
    .stButton>button {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(248, 250, 252, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: #38bdf8;
        color: #38bdf8;
        transform: translateY(-2px);
    }

    /* Animación sutil de la manzana */
    @keyframes worm-peek {
        0%, 100% { transform: translate(40px, 0px) scale(0); opacity: 0; }
        50% { transform: translate(0px, -45px) rotate(15deg) scale(1.1); opacity: 1; }
    }
    .apple-stage { position: relative; font-size: 6rem; text-align: center; margin: 20px 0; }
    .worm-move { position: absolute; font-size: 2rem; animation: worm-peek 8s infinite; left: 47%; top: 15%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE NAVEGACIÓN ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"

# Definimos las columnas PRIMERO para evitar el NameError de tus fotos
col_menu, col_main = st.columns([1, 2.2])

# --- LADO IZQUIERDO: MENÚ ---
with col_menu:
    st.markdown("### 🚀 Menú Maestro")
    if st.button("🏠 Inicio / Comunidad", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"
    
    st.markdown("---")
    st.markdown("### 📏 ProfeEduca ✏️")

# --- LADO DERECHO: CONTENIDO DINÁMICO ---
with col_main:
    if st.session_state.seccion == "inicio":
        st.markdown("### 🍎 El Café del Maestro")
        st.markdown('<div class="apple-stage"><span class="worm-move">🐛</span>🍎</div>', unsafe_allow_html=True)
        st.info("Espacio de convivencia y amistad para educadores.")

    elif st.session_state.seccion == "plan":
        st.header("📋 Generador de Planeación ABCD")
        
        # Formulario de datos
        col1, col2 = st.columns(2)
        with col1:
            nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
            grado = st.text_input("Grado (ej. 3° Multigrado)")
            educador = st.text_input("Nombre del Educador")
        with col2:
            comunidad = st.text_input("Comunidad")
            tema = st.text_input("Tema de Interés")
            fecha = st.date_input("Fecha", datetime.now())

        st.markdown("---")
        # Aquí la IA generaría el PDF
        if st.button("🚀 GENERAR PLANEACIÓN EN PDF", use_container_width=True):
            with st.spinner("Construyendo pedagogía..."):
                # Simulación de generación de PDF (Lógica FPDF)
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"Planeación: {tema}", ln=True, align='C')
                pdf.set_font("Arial", '', 12)
                pdf.ln(10)
                pdf.multi_cell(0, 10, f"Educador: {educador}\nNivel: {nivel}\nComunidad: {comunidad}")
                
                # Convertir a bytes para descarga
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.success("¡Planeación lista!")
                st.download_button(
                    label="📥 Descargar mi PDF",
                    data=pdf_output,
                    file_name=f"Planeacion_{tema}.pdf",
                    mime="application/pdf"
                )
