import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import io

# Configuración del modelo Lite para evitar errores de cuota según tu tabla
IA_MODEL = "gemini-2.0-flash-lite" 
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

st.set_page_config(page_title="ProfeEduca | Planeación", page_icon="🍎", layout="wide")

# Estilos CSS corregidos (comillas cerradas)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 2.5rem; font-weight: 900; color: #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# Función para el PDF profesional
def generar_pdf_oficial(datos, contenido):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"PLANEACIÓN ABCD - {datos['inst']}", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.cell(95, 10, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 10, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(190, 10, txt=f"Comunidad: {datos['comunidad']} | Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="4 Estaciones de Aprendizaje", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=contenido.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# Interfaz de usuario
st.markdown('<div class="brand-header">📏 ProfeEduca ✏️</div>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("E.C. (Abreviado)")
        eca = st.text_input("E.C.A. (Abreviado)")
        comunidad = st.text_input("Nombre de la Comunidad")
    with col2:
        rincon = st.text_input("Rincón (Permanente)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

tema = st.text_input("Tema de interés para las estaciones:")
notas = st.text_area("Observaciones adicionales:")

if st.button("🚀 Planeaciones ABCD"):
    if tema and ec:
        with st.spinner("La IA está redactando las 4 estaciones..."):
            prompt = f"Genera una planeación ABCD extensa sobre {tema} con 4 estaciones y 3 actividades por cada uno de los 4 campos formativos."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{IA_MODEL}:generateContent?key={GEMINI_KEY}"
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if res.status_code == 200:
                    plan_ia = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(plan_ia)
                    
                    datos_pdf = {"ec": ec, "eca": eca, "comunidad": comunidad, "inst": inst, "fecha": fecha_hoy}
                    pdf_bytes = generar_pdf_oficial(datos_pdf, plan_ia)
                    
                    st.download_button("📥 Descargar Planeación PDF", data=pdf_bytes, file_name=f"Planeacion_{tema}.pdf")
                else:
                    st.error(f"Error de cuota (Código {res.status_code}). Espera un minuto.")
            except:
                st.error("Error de conexión con la IA.")
