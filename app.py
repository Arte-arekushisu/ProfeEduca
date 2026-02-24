import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq
import io

# --- 1. CONFIGURACIÓN ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="ProfeEduca ABCD Pro", page_icon="🍎", layout="wide")

# Estilos Visuales
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGENCIA HÍBRIDA ---
def llamar_ia(prompt):
    # Intentar primero con Groq (Respaldo Robusto)
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un experto en el modelo ABCD y la NEM."},
                      {"role": "user", "content": prompt}],
            temperature=0.7, max_tokens=3000
        )
        return completion.choices[0].message.content, "Groq"
    except:
        # Intento con Gemini si Groq falla
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            return res.json()['candidates'][0]['content']['parts'][0]['text'], "Gemini"
        except: return None, None

# --- 3. GENERACIÓN DE PDF ---
def generar_pdf(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado e Institución
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"PLANEACIÓN PROFESIONAL - {datos['inst']}", ln=True, align='C')
    pdf.ln(5)
    
    # Datos del Formulario
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 8, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(95, 8, txt=f"Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(95, 8, txt=f"Nivel: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    pdf.cell(95, 8, txt=f"Rincón: {datos['rincon']}", border=1)
    pdf.cell(95, 8, txt=f"Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.ln(5)

    # Cuerpo de la Planeación
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Desarrollo Pedagógico Semanal", ln=True)
    pdf.set_font("Arial", size=10)
    
    # Limpieza de texto para evitar errores de codificación
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ DE USUARIO ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Pro ✏️</div>', unsafe_allow_html=True)

with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        ec = st.text_input("Nombre E.C. (Abreviado)")
        eca = st.text_input("Nombre E.C.A. (Abreviado)")
        comu = st.text_input("Comunidad")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria", "Multigrado"])
    with c2:
        grados = st.text_input("Grado(s)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        rincon = st.text_input("Rincón (Manual)")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Tema para Relación Tutora (Información extensa y bibliografía)")
    st.markdown("---")
    st.write("### 🕒 Bloque Post-Receso")
    pr1 = st.text_input("Sesión 1 (Materia/Actividad)")
    pr2 = st.text_input("Sesión 2 (Materia/Actividad)")
    obs = st.text_area("Observaciones Finales")

    boton_generar = st.form_submit_button("🚀 Planeaciones ABCD")

# --- 5. EJECUCIÓN ---
if boton_generar:
    if not ec or not tema_tutora:
        st.error("Por favor rellena el nombre del E.C. y el tema de tutoría.")
    else:
        with st.spinner("Construyendo planeación y estaciones..."):
            prompt_maestro = f"""
            Genera una planeación ABCD de alta calidad:
            1. TEMA TUTORÍA: Información detallada y académica sobre '{tema_tutora}'. Incluye fuentes confiables (SEP, bibliografía real) y referencias APA al final de esta sección.
            2. 4 ESTACIONES INDEPENDIENTES: Crea 4 estaciones con nombres atractivos y creativos. 
            IMPORTANTE: Las estaciones NO deben tratar sobre '{tema_tutora}'. 
            Cada estación debe corresponder obligatoriamente a uno de los 4 campos formativos:
            - Estación 1: Lenguajes.
            - Estación 2: Saberes y Pensamiento Científico.
            - Estación 3: Ética, Naturaleza y Sociedades.
            - Estación 4: De lo Humano y lo Comunitario.
            3. PROCEDIMIENTOS: Detalla paso a paso las instrucciones para el educador en cada estación.
            """
            
            respuesta_ia, motor_usado = llamar_ia(prompt_maestro)
            
            if respuesta_ia:
                st.success(f"¡Éxito! Generado mediante {motor_usado}")
                st.markdown(respuesta_ia)
                
                # Preparar datos para el PDF
                datos_doc = {
                    "ec": ec, "eca": eca, "comunidad": comu, "nivel": nivel,
                    "grados": grados, "inst": inst, "rincon": rincon, "fecha": fecha_gen
                }
                
                # Generar bytes del PDF
                pdf_output = generar_pdf(datos_doc, respuesta_ia)
                
                st.download_button(
                    label="📥 Descargar Planeación PDF",
                    data=pdf_output,
                    file_name=f"Planeacion_ABCD_{ec}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Límite de la IA alcanzado. Por favor, espera un minuto.")
