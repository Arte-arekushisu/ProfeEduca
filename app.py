import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq
import io

# --- CONFIGURACIÓN ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="ProfeEduca ABCD Pro", page_icon="🍎", layout="wide")

# Estilos ProfeEduca
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGENCIA ---
def llamar_ia(prompt):
    # Intentar con Groq primero ya que es más estable para textos largos
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un experto en el modelo ABCD de CONAFE y la Nueva Escuela Mexicana."},
                      {"role": "user", "content": prompt}],
            temperature=0.7, max_tokens=3000
        )
        return completion.choices[0].message.content, "Groq"
    except:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            return res.json()['candidates'][0]['content']['parts'][0]['text'], "Gemini"
        except: return None, None

# --- FUNCIÓN PARA EL PDF ---
def generar_pdf_final(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"PLANEACIÓN ABCD - {datos['inst']}", ln=True, align='C')
    pdf.ln(5)
    
    # Tabla de Datos
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, txt=f"E.C.: {datos['ec']}", border=1)
    pdf.cell(95, 8, txt=f"E.C.A.: {datos['eca']}", border=1, ln=True)
    pdf.cell(95, 8, txt=f"Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(95, 8, txt=f"Nivel: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    pdf.cell(95, 8, txt=f"Rincón: {datos['rincon']}", border=1)
    pdf.cell(95, 8, txt=f"Fecha: {datos['fecha']}", border=1, ln=True)
    pdf.ln(10)
    
    # Cuerpo
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Desarrollo Pedagógico y Estaciones", ln=True)
    pdf.set_font("Arial", size=10)
    
    # Limpiar texto para FPDF
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, txt=texto_pdf_limpio := texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Pro ✏️</div>', unsafe_allow_html=True)

with st.form("planeador"):
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("E.C. (Abreviado)")
        eca = st.text_input("E.C.A. (Abreviado)")
        comu = st.text_input("Comunidad")
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria", "Multigrado"])
    with col2:
        grados = st.text_input("Grado(s)")
        inst = st.selectbox("Institución", ["CONAFE", "SEP", "Otros"])
        rinc = st.text_input("Rincón (Manual)")
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Tema de interés para Relación Tutora (Información extensa y fuentes)")
    
    st.markdown("### 🍎 Post-Receso")
    pr1 = st.text_input("Sesión 1")
    pr2 = st.text_input("Sesión 2")
    obs = st.text_area("Observaciones")

    enviar = st.form_submit_button("🚀 Planeaciones ABCD")

if enviar:
    if not tema_tutora or not ec:
        st.warning("Faltan campos obligatorios.")
    else:
        with st.spinner("Generando documento..."):
            prompt = f"""
            Genera una planeación ABCD profesional.
            1. RELACIÓN TUTORA: Información muy extensa sobre '{tema_tutora}'. Incluye fuentes confiables (Libros de texto SEP, Red de Tutoría) y bibliografía APA.
            2. 4 ESTACIONES INDEPENDIENTES: Crea 4 estaciones con nombres creativos. Cada estación debe estar ligada a UN CAMPO FORMATIVO diferente (Lenguajes, Saberes, Ética, De lo Humano). 
            3. ACTIVIDADES: Detalla instrucciones y procedimientos claros para el educador en cada estación.
            """
            
            resultado, motor = llamar_ia(prompt)
            
            if resultado:
                st.success(f"Generado con {motor}")
                st.markdown(resultado)
                
                # Generar y ofrecer descarga
                datos_pdf = {
                    "ec": ec, "eca": eca, "comunidad": comu, "inst": inst, 
                    "nivel": nivel, "grados": grados, "rincon": rinc, "fecha": fecha_hoy
                }
                pdf_bytes = generar_pdf_final(datos_pdf, resultado)
                st.download_button("📥 DESCARGAR PLANEACIÓN PDF", data=pdf_bytes, file_name=f"Planeacion_{ec}.pdf", mime="application/pdf")
            else:
                st.error("Servidores ocupados. Intenta de nuevo.")
