import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import base64

# --- 1. CONFIGURACIÓN Y CEREBRO ---
IA_MODEL = "gemini-1.5-flash" 
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

st.set_page_config(page_title="ProfeEduca | Planeaciones", page_icon="📝")

# --- 2. FUNCIÓN PARA GENERAR PDF ---
def crear_pdf(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Encabezado
    pdf.cell(200, 10, txt=f"Planeación de Actividades - {datos['institucion']}", ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    
    # Tabla de datos generales
    pdf.cell(100, 10, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(90, 10, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(100, 10, txt=f"Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(90, 10, txt=f"Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.cell(100, 10, txt=f"Rincón: {datos['rincon']}", border=1, ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Desarrollo de Estaciones y Campos Formativos", ln=True)
    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=contenido_ia)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 3. INTERFAZ ---
st.title("📝 Planeaciones ABCD")
st.markdown("---")

with st.expander("🛠️ Datos del Educador y Comunidad", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("Nombre del E.C. (Abreviado)")
        eca = st.text_input("Nombre del E.C.A. (Abreviado)")
        comunidad = st.text_input("Comunidad")
    with col2:
        fecha = st.date_today()
        rincon = st.text_input("Rincón (Permanente)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        if inst == "Otros":
            otra_inst = st.text_input("Nombre de la Institución")
            logo_subido = st.file_uploader("Subir Logo")

tema_interes = st.text_input("Tema de interés para las estaciones", placeholder="Ej. El cuidado del medio ambiente")
notas = st.text_area("Observaciones o notas adicionales")

if st.button("🚀 Generar Planeaciones ABCD"):
    if not tema_interes or not ec:
        st.error("Por favor rellena los campos obligatorios.")
    else:
        with st.spinner("La IA está diseñando las 4 estaciones..."):
            # Prompt optimizado para evitar el error de cuota
            prompt = f"""Genera una planeación pedagógica extensa para {tema_interes}. 
            Nivel: Comunitario. 
            Estructura: 4 estaciones de aprendizaje. 
            Cada estación debe tener 3 actividades detalladas enfocadas en:
            1. Lenguajes. 2. Saberes y Pensamiento Científico. 3. Ética, Naturaleza y Sociedades. 4. De lo Humano y lo Comunitario.
            Estilo: Aprendizaje autónomo (Relación Tutora)."""
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{IA_MODEL}:generateContent?key={GEMINI_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            res = requests.post(url, json=payload)
            
            if res.status_code == 200:
                contenido = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.success("¡Planeación generada con éxito!")
                
                # Datos para el PDF
                datos_doc = {
                    "ec": ec, "eca": eca, "comunidad": comunidad,
                    "fecha": str(fecha), "rincon": rincon, "institucion": inst
                }
                
                pdf_bytes = crear_pdf(datos_doc, contenido)
                
                st.download_button(
                    label="📥 Descargar Planeación en PDF",
                    data=pdf_bytes,
                    file_name=f"Planeacion_{tema_interes}.pdf",
                    mime="application/pdf"
                )
                
                st.markdown("### Previsualización del Contenido")
                st.write(contenido)
            else:
                st.error("Límite de cuota excedido. Por favor espera 60 segundos.")
