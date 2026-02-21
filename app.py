import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

# Estilo CSS para el fondo y las tarjetas
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); 
        background-size: 400% 400%; 
        animation: gradient 15s ease infinite; 
        color: white; 
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-card { 
        background: rgba(255, 255, 255, 0.1); 
        border-radius: 15px; padding: 15px; margin: 10px; border-left: 5px solid #00d4ff; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES TÉCNICAS
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_Estructurado(FPDF):
    def __init__(self, logo_izq=None, logo_der=None):
        super().__init__()
        self.logo_izq = logo_izq
        self.logo_der = logo_der

    def header(self):
        if self.logo_izq:
            self.image(self.logo_izq, 10, 8, 30)
        if self.logo_der:
            self.image(self.logo_der, 170, 8, 30)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Texto Reflexivo Trimestral', 0, 1, 'C')
        self.ln(10)

# 3. BASE DE DATOS DE SESIÓN
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": True, # Cambiado a True para facilitar tu prueba técnica
        "user": "Invitado",
        "user_data": {"Invitado": {"name": "Educador", "pic": ""}},
        "alumnos": {}
    }

# 4. INTERFAZ DE NAVEGACIÓN
menu = st.sidebar.radio("MENÚ", ["✍️ Diario Reflexivo", "📊 Evaluación Trimestral"])

# --- SECCIÓN: DIARIO REFLEXIVO ---
if menu == "✍️ Diario Reflexivo":
    st.header("Registro de Avances Diarios")
    nom = st.text_input("Nombre del Alumno").upper()
    texto = st.text_area("Descripción de lo aprendido hoy (Escrito Reflexivo)")
    
    if st.button("Guardar en Base de Datos"):
        if nom and texto:
            if nom not in st.session_state.db["alumnos"]:
                st.session_state.db["alumnos"][nom] = {"diario": []}
            st.session_state.db["alumnos"][nom]["diario"].append(texto)
            st.success(f"Registro guardado para {nom}")
        else:
            st.error("Por favor llena todos los campos.")

# --- SECCIÓN: EVALUACIÓN ESTRUCTURADA ---
elif menu == "📊 Evaluación Trimestral":
    st.header("Evaluación Trimestral Estructurada")
    
    with st.expander("🖼️ Configuración de Logos para PDF"):
        c1, c2 = st.columns(2)
        l_izq = c1.file_uploader("Logo Izquierdo (CONAFE)", type=["png", "jpg"])
        l_der = c2.file_uploader("Logo Derecho (Project Mercy)", type=["png", "jpg"])

    busqueda = st.text_input("Buscar Alumno por Nombre").upper()
    
    if busqueda in st.session_state.db["alumnos"]:
        # Recopilar historial para sintetizar
        historial = " ".join(st.session_state.db["alumnos"][busqueda]["diario"])
        
        col1, col2, col3 = st.columns(3)
        escuela = col1.text_input("Nombre de la Escuela", "San Nicolas")
        nivel = col2.text_input("Nivel / Grado", "4to Primaria")
        educador = col3.text_input("Nombre del Educador")

        st.subheader("Campos Formativos (Sintetizar de la Base de Datos)")
        f1 = st.text_area("L
