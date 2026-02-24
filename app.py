import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import io

# --- CONFIGURACIÓN DE RESPALDO (Multi-Modelo) ---
# Usaremos una lista para que si uno falla, el otro entre al rescate
MODELOS_DISPONIBLES = ["gemini-2.0-flash-lite", "gemini-1.5-flash", "gemma-3-27b"]
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

st.set_page_config(page_title="ProfeEduca | Planeación", page_icon="🍎", layout="wide")

# Función para intentar generar con varios modelos si uno falla
def llamar_ia_con_respaldo(prompt):
    for modelo in MODELOS_DISPONIBLES:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={GEMINI_KEY}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text'], modelo
        except:
            continue
    return None, None

# Función PDF (Sin cambios, es estable)
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
    pdf.set_font("Arial", size=10)
    # Limpieza de caracteres para evitar errores en PDF
    texto_limpio = contenido.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texto_limpio)
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ ---
st.title("🚀 Generador ProfeEduca")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("E.C. (Abreviado)")
        eca = st.text_input("E.C.A. (Abreviado)")
        comunidad = st.text_input("Comunidad")
    with col2:
        rincon = st.text_input("Rincón (Permanente)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        fecha_hoy = datetime.now().strftime("%d/%m/%Y") # Corrección de error previo

tema = st.text_input("Tema de interés para las estaciones:")
notas = st.text_area("Observaciones adicionales:")

if st.button("🚀 Planeaciones ABCD"):
    if tema and ec:
        with st.spinner("Buscando una IA disponible para redactar..."):
            prompt = f"Genera una planeación ABCD extensa sobre {tema} con 4 estaciones y 3 actividades por cada uno de los 4 campos formativos."
            
            plan_ia, modelo_usado = llamar_ia_con_respaldo(prompt)
            
            if plan_ia:
                st.caption(f"Generado exitosamente con: {modelo_usado}")
                st.markdown(plan_ia)
                
                datos_pdf = {"ec": ec, "eca": eca, "comunidad": comunidad, "inst": inst, "fecha": fecha_hoy}
                pdf_bytes = generar_pdf_oficial(datos_pdf, plan_ia)
                
                st.download_button("📥 Descargar Planeación PDF", data=pdf_bytes, file_name=f"Planeacion_{tema}.pdf")
            else:
                st.error("🚨 Todos los modelos gratuitos están saturados en este momento. Por favor, espera 2 minutos para que se libere la cuota.")
    else:
        st.warning("Escribe el nombre del E.C. y el tema para comenzar.")
