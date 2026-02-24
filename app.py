import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import io

# --- 1. CONFIGURACIÓN Y CEREBRO ---
# Usamos 1.5-flash para evitar el error de límite de cuota
IA_MODEL = "gemini-1.5-flash" 
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

st.set_page_config(page_title="ProfeEduca | Planeación ABCD", page_icon="🍎", layout="wide")

# --- 2. FUNCIÓN PARA GENERAR EL PDF ---
def generar_pdf_abcd(datos, plan_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Encabezado con Institución
    pdf.cell(200, 10, txt=f"PLANEACIÓN ABCD - {datos['inst']}", ln=True, align='C')
    pdf.ln(5)
    
    # Datos Generales
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 10, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 10, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(95, 10, txt=f"Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(95, 10, txt=f"Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.cell(190, 10, txt=f"Rincón: {datos['rincon']}", border=1, ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Propuesta Pedagógica (4 Estaciones / 4 Campos Formativos)", ln=True)
    
    # Contenido de la IA
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=plan_ia.encode('latin-1', 'ignore').decode('latin-1'))
    
    # Notas
    if datos['notas']:
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 10, txt=f"Observaciones: {datos['notas']}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. INTERFAZ VISUAL ---
st.title("📏 Planeaciones ABCD ✏️")

with st.expander("📋 Datos de Identificación", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        ec = st.text_input("Nombre del E.C. (Abreviado)")
        eca = st.text_input("Nombre del E.C.A. (Abreviado)")
        comunidad = st.text_input("Nombre de la Comunidad")
    with c2:
        # CORRECCIÓN: La función correcta es date.today() de datetime o st.date_input
        fecha_auto = datetime.now().strftime("%d/%m/%Y")
        st.write(f"**Fecha:** {fecha_auto}")
        rincon = st.text_input("Rincón (Manual)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        if inst == "Otros":
            otra_inst = st.text_input("Escribe el nombre de la institución")
            logo_subido = st.file_uploader("Sube el logo correspondiente")

tema_interes = st.text_input("Tema de interés para las estaciones:", placeholder="Ej. El ciclo de la vida")
notas_manuales = st.text_area("Observaciones o notas adicionales:")

# --- 4. LÓGICA DE GENERACIÓN ---
if st.button("🚀 Planeaciones ABCD"):
    if not tema_interes or not ec:
        st.error("Por favor, ingresa al menos el nombre del E.C. y el tema de interés.")
    else:
        with st.spinner("La IA está diseñando las 4 estaciones de aprendizaje..."):
            prompt = f"""
            Genera una planeación detallada basada en el modelo de aprendizaje autónomo para el tema: {tema_interes}.
            Debes organizar el contenido en 4 ESTACIONES DE APRENDIZAJE.
            Cada estación debe incluir 3 actividades específicas enfocadas en los 4 campos formativos:
            1. Lenguajes.
            2. Saberes y Pensamiento Científico.
            3. Ética, Naturaleza y Sociedades.
            4. De lo Humano y lo Comunitario.
            
            Usa un tono pedagógico y profesional. No menciones marcas de IA.
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{IA_MODEL}:generateContent?key={GEMINI_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                res = requests.post(url, json=payload)
                plan_texto = res.json()['candidates'][0]['content']['parts'][0]['text']
                
                # Guardar datos para el PDF
                datos_para_pdf = {
                    "ec": ec, "eca": eca, "comunidad": comunidad,
                    "fecha": fecha_auto, "rincon": rincon, 
                    "inst": inst if inst != "Otros" else otra_inst,
                    "notas": notas_manuales
                }
                
                # Generar PDF
                pdf_output = generar_pdf_abcd(datos_para_pdf, plan_texto)
                
                st.success("¡Planeación generada con éxito!")
                st.markdown(plan_texto)
                
                st.download_button(
                    label="📥 Descargar Planeación en PDF",
                    data=pdf_output,
                    file_name=f"Planeacion_ABCD_{tema_interes}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error("Límite de la IA alcanzado o error de conexión. Intenta de nuevo en un minuto.")
