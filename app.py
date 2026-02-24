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

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGENCIA ---
def llamar_ia(prompt):
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un experto pedagogo especializado en el modelo ABCD (Aprendizaje Basado en la Colaboración y el Diálogo)."},
                      {"role": "user", "content": prompt}],
            temperature=0.7, max_tokens=3500
        )
        return completion.choices[0].message.content, "Groq"
    except:
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
    
    # Encabezado Profesional
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="PLANEACIÓN PROFESIONAL ABCD", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt=f"Institución: {datos['inst']}", ln=True, align='C')
    pdf.ln(5)
    
    # Cuadro de datos (Diseño Limpio B/N)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(95, 8, txt=f" E.C.: {datos['ec']}", border=1, fill=True)
    pdf.cell(95, 8, txt=f" E.C.A.: {datos['eca']}", border=1, fill=True, ln=True)
    pdf.cell(95, 8, txt=f" Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(95, 8, txt=f" Nivel: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    pdf.cell(95, 8, txt=f" Rincón: {datos['rincon']}", border=1)
    pdf.cell(95, 8, txt=f" Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.ln(10)

    # Contenido
    pdf.set_font("Arial", size=11)
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
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
        inst = st.selectbox("Institución", ["SEP", "CET", "Otros"])
        rincon = st.text_input("Rincón (Manual)")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Tema para Relación Tutora (Relación Tutora y Bibliografía)")
    st.markdown("---")
    st.write("### 🕒 Bloque Post-Receso")
    pr1 = st.text_input("Sesión 1 (Materia/Actividad)")
    pr2 = st.text_input("Sesión 2 (Materia/Actividad)")
    obs = st.text_area("Observaciones Finales")

    boton_generar = st.form_submit_button("🚀 Planeaciones ABCD")

if boton_generar:
    if not ec or not tema_tutora:
        st.error("Por favor completa los campos obligatorios.")
    else:
        with st.spinner("Diseñando actividades autónomas..."):
            prompt_maestro = f"""
            Genera una 'PLANEACIÓN PROFESIONAL ABCD' detallada.
            
            1. ACTIVIDADES INICIALES:
               - Pase de lista creativo.
               - Regalo de lectura (título sugerido y breve dinámica).
               - Bienvenida adaptada al nivel {nivel} y grado {grados}.
            
            2. DESARROLLO PEDAGÓGICO SEMANAL:
               - Organiza según tiempos pedagógicos (Relación tutora, trabajo autónomo, demostración).
               - Tema de Tutoría: '{tema_tutora}'. Incluye información académica, fuentes (APA) y 5 PREGUNTAS DETONANTES.
            
            3. 4 ESTACIONES INDEPENDIENTES (Uso de material reciclado):
               - Crea 4 estaciones con nombres llamativos.
               - Las estaciones NO deben tratar sobre '{tema_tutora}'.
               - Asigna una a cada Campo Formativo (Lenguajes, Saberes, Ética, De lo Humano).
               - Para cada una incluye: 'Pasos para el alumno (Trabajo autónomo)' e 'Instrucciones de desarrollo'.
            
            4. POST-RECESO:
               - Incluye espacio para {pr1} y {pr2}.
            
            Nota: No menciones la palabra 'CONAFE' en el texto.
            """
            
            respuesta_ia, motor = llamar_ia(prompt_maestro)
            
            if respuesta_ia:
                st.success(f"Generado exitosamente.")
                st.markdown(respuesta_ia)
                
                datos_doc = {"ec": ec, "eca": eca, "comunidad": comu, "nivel": nivel,
                             "grados": grados, "inst": inst, "rincon": rincon, "fecha": fecha_gen}
                
                pdf_output = generar_pdf(datos_doc, respuesta_ia)
                st.download_button(label="📥 Descargar Planeación PDF", data=pdf_output,
                                   file_name=f"Planeacion_ABCD_{ec}.pdf", mime="application/pdf")
