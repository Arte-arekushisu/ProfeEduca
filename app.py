import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import io

# --- CONFIGURACIÓN DE IA (Modelo Lite para evitar bloqueos) ---
# Este modelo es ideal para textos largos y tiene mayor límite gratuito
IA_MODEL = "gemini-2.0-flash-lite" 
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"

# --- FUNCIÓN GENERADORA DE PDF ---
def crear_pdf_final(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado institucional
    pdf.set_font("Arial", 'B', 15)
    pdf.cell(200, 10, txt=f"PLANEACIÓN DOCENTE: {datos['inst']}", ln=True, align='C')
    pdf.ln(5)
    
    # Bloque de datos del E.C. y E.C.A.
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 8, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(95, 8, txt=f"Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(95, 8, txt=f"Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.cell(190, 8, txt=f"Rincón: {datos['rincon']}", border=1, ln=True)
    
    # Cuerpo de la planeación
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Propuesta Pedagógica: 4 Estaciones de Aprendizaje", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 7, txt=contenido_ia.encode('latin-1', 'ignore').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ STREAMLIT ---
st.title("📏 Planeaciones ABCD ✏️")

with st.form("form_planeacion"):
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("Nombre E.C.")
        eca = st.text_input("Nombre E.C.A.")
        comunidad = st.text_input("Comunidad")
    with col2:
        rincon = st.text_input("Rincón (Fijo)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        if inst == "Otros":
            nombre_o = st.text_input("Nombre de la Institución")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema = st.text_input("Tema de interés (Estaciones)")
    notas = st.text_area("Observaciones manuales")
    
    submit = st.form_submit_button("🚀 Planeaciones ABCD")

if submit:
    if tema and ec:
        with st.spinner("Redactando planeación completa..."):
            # Prompt optimizado para las 4 estaciones y campos formativos
            prompt_doc = f"""
            Redacta una planeación extensa para el tema '{tema}'.
            Formato: 4 Estaciones de aprendizaje.
            Cada estación debe tener 3 actividades claras para estos 4 campos:
            1. Lenguajes. 
            2. Saberes y Pensamiento Científico. 
            3. Ética, Naturaleza y Sociedades. 
            4. De lo Humano y lo Comunitario.
            Estilo de aprendizaje autónomo y comunitario.
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{IA_MODEL}:generateContent?key={GEMINI_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt_doc}]}]})
            
            if res.status_code == 200:
                contenido = res.json()['candidates'][0]['content']['parts'][0]['text']
                
                datos_pdf = {
                    "ec": ec, "eca": eca, "comunidad": comunidad,
                    "fecha": fecha_gen, "rincon": rincon, 
                    "inst": inst if inst != "Otros" else nombre_o,
                    "notas": notas
                }
                
                pdf_final = crear_pdf_final(datos_pdf, contenido)
                
                st.success("¡Documento listo!")
                st.markdown(contenido)
                st.download_button("📥 Descargar Planeación PDF", data=pdf_final, file_name=f"ABCD_{tema}.pdf")
            else:
                st.error("Límite temporal alcanzado en este modelo. Espera un momento.")
