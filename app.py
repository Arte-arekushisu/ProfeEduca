import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF

# --- 1. CONFIGURACIÓN Y MOTORES ---
# Intentaremos con el modelo más ligero y rápido disponible en tu tier
MODELO_PRINCIPAL = "gemini-2.0-flash-lite"
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

st.set_page_config(page_title="ProfeEduca | Planeación Semanal", page_icon="🍎", layout="wide")

# --- 2. ESTILOS CSS (Fondo ProfeEduca) ---
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    .brand-header {
        display: flex; align-items: center; justify-content: center;
        gap: 10px; font-size: 2.5rem; font-weight: 900; color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES CORE ---
def generar_con_ia(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO_PRINCIPAL}:generateContent?key={GEMINI_KEY}"
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return None
    except:
        return None

def crear_pdf(datos, contenido):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"PLANEACIÓN SEMANAL - {datos['inst']}", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.cell(95, 8, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 8, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(190, 8, txt=f"Comunidad: {datos['comunidad']} | Tema: {datos['tema']}", border=1, ln=True)
    pdf.ln(10)
    # Limpieza de texto para evitar errores de codificación en FPDF
    pdf.multi_cell(0, 8, txt=contenido.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
st.markdown("<div class='brand-header'>📏 ProfeEduca ✏️</div>", unsafe_allow_html=True)

with st.sidebar:
    st.title("Menú Maestro")
    opcion = st.radio("Ir a:", ["Inicio", "Planeaciones ABCD"])

if opcion == "Planeaciones ABCD":
    st.subheader("🗓️ Generador de Planeación Semanal")
    
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("Nombre del E.C.")
        eca = st.text_input("Nombre del E.C.A.")
    with col2:
        comunidad = st.text_input("Nombre de la Comunidad")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
    
    tema = st.text_input("Tema de interés (Duración: 1 semana)")
    rincon = st.text_input("Rincón (Fijo)")
    notas = st.text_area("Notas u observaciones")

    if st.button("🚀 Generar Planeaciones ABCD"):
        if tema and ec:
            with st.spinner("Conectando con el motor pedagógico..."):
                prompt_semanal = f"""
                Genera una planeación pedagógica ABCD para UNA SEMANA completa sobre '{tema}'.
                Distribuye las actividades de Lunes a Viernes.
                Organiza en 4 ESTACIONES, cada una con 3 actividades enfocadas en los campos:
                1. Lenguajes. 2. Saberes y Pensamiento Científico. 3. Ética, Naturaleza y Sociedades. 4. De lo Humano y lo Comunitario.
                Incluye materiales y evaluación para el viernes.
                """
                
                resultado = generar_con_ia(prompt_semanal)
                
                if resultado:
                    st.success("¡Planeación generada exitosamente!")
                    st.markdown(resultado)
                    
                    # Generación de PDF
                    datos_doc = {"ec": ec, "eca": eca, "comunidad": comunidad, "inst": inst, "tema": tema}
                    pdf_bytes = crear_pdf(datos_doc, resultado)
                    
                    st.download_button("📥 Descargar PDF Semanal", data=pdf_bytes, file_name=f"Planeacion_{tema}.pdf")
                else:
                    st.error("⚠️ Los servidores están saturados. ¿Quieres que intentemos con una IA alternativa de respaldo?")
        else:
            st.warning("Por favor completa el nombre del E.C. y el tema.")
else:
    st.write("Bienvenido. Tu labor es la luz de la comunidad.")
