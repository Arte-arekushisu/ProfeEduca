import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq
import io
import re

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
            messages=[{"role": "system", "content": "Eres un experto en el modelo ABCD y la Nueva Escuela Mexicana. Generas planeaciones detalladas, profesionales, SIN ASTERISCOS (*) y con enfoque en Campos Formativos."},
                      {"role": "user", "content": prompt}],
            temperature=0.5, max_tokens=5000
        )
        texto = completion.choices[0].message.content
        return texto.replace("*", ""), "Groq"
    except:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
            texto = res.json()['candidates'][0]['content']['parts'][0]['text']
            return texto.replace("*", ""), "Gemini"
        except: return None, None

# --- 3. GENERACIÓN DE PDF ---
def generar_pdf(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado Oficial
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(0, 0, 0) 
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, txt="PLANEACIÓN PEDAGÓGICA COMUNITARIA ABCD", ln=True, align='C', fill=True)
    pdf.ln(5)
    
    # Tabla de Identificación
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    
    pdf.cell(95, 8, txt=f" EDUCADO/A (E.C.): {datos['ec'].upper()}", border=1, fill=True)
    pdf.cell(95, 8, txt=f" ACOMPAÑANTE (E.C.A.): {datos['eca'].upper()}", border=1, fill=True, ln=True)
    
    pdf.set_fill_color(255, 255, 255)
    pdf.cell(95, 8, txt=f" COMUNIDAD: {datos['comunidad']}", border=1)
    pdf.cell(95, 8, txt=f" NIVEL / GRADO: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    
    pdf.cell(95, 8, txt=f" RINCÓN DE INTERÉS: {datos['rincon']}", border=1)
    pdf.cell(95, 8, txt=f" PERIODO: {datos['duracion']}", border=1, ln=True)
    pdf.ln(10)

    # Cuerpo del Contenido
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="SECUENCIA DIDÁCTICA SEMANAL", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", size=10)
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Pro ✏️</div>', unsafe_allow_html=True)

with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        ec = st.text_input("Nombre del Educador (E.C.)")
        eca = st.text_input("Acompañante (E.C.A.)")
        comu = st.text_input("Comunidad")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria", "Multigrado"])
    with c2:
        grados = st.text_input("Grado(s) o Etapas")
        duracion = st.selectbox("Duración", ["1 Día", "1 Semana Hábil", "2 Semanas Hábiles"])
        rincon = st.text_input("Rincón o Unidad de Aprendizaje")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Tema de la Relación Tutora (Desarrollo del contenido)")
    post_receso_req = st.text_area("Proyectos o materias para la tarde (Post-Receso)")

    boton_generar = st.form_submit_button("🚀 Generar Planeación Pro")

if boton_generar:
    if not ec or not tema_tutora:
        st.error("Datos incompletos.")
    else:
        with st.spinner("Optimizando para contexto comunitario..."):
            prompt_maestro = f"""
            Genera una PLANEACIÓN PROFESIONAL ABCD para {duracion}.
            NO USES ASTERISCOS (*). Usa títulos en MAYÚSCULAS.

            1. MOMENTOS INICIALES: 
               - Crea un Pase de Lista Temático y un Regalo de Lectura relacionado con {rincon}.
            
            2. HORARIO (8:00 AM - 2:00 PM): 
               - Detalla bloques para: Inicio, Desarrollo de Relación Tutora, Trabajo en Estaciones, Receso, Bloque de Proyectos Post-Receso y Cierre/Evaluación.

            3. RELACIÓN TUTORA: 
               - Contenido profundo sobre {tema_tutora}. 
               - Incluye 5 PREGUNTAS DETONANTES que no se respondan con 'si' o 'no'.
               - Vincula con el Campo Formativo correspondiente.

            4. 4 ESTACIONES INDEPENDIENTES (ENFOQUE NEM):
               - Estación 1: Lenguajes (Lecto-escritura o comunicación).
               - Estación 2: Saberes y Pensamiento Científico (Lógica/Matemáticas).
               - Estación 3: Ética, Naturaleza y Sociedades.
               - Estación 4: De lo Humano y lo Comunitario.
               - Para cada una: Nombre creativo, materiales reciclados y PASOS DETALLADOS para que el alumno aprenda por sí mismo.

            5. CRONOGRAMA POST-RECESO (LUNES A VIERNES):
               - Variedad diaria de actividades basadas en {post_receso_req}.
               - Incluye procedimientos para que el EC sepa cómo guiar la actividad.
            """
            
            respuesta_ia, motor = llamar_ia(prompt_maestro)
            
            if respuesta_ia:
                st.success("Planeación generada correctamente.")
                st.markdown(respuesta_ia)
                
                datos_doc = {"ec": ec, "eca": eca, "comunidad": comu, "nivel": nivel, 
                             "grados": grados, "duracion": duracion, "rincon": rincon, 
                             "fecha": fecha_gen}
                
                pdf_output = generar_pdf(datos_doc, respuesta_ia)
                st.download_button(label="📥 Descargar PDF para Comunidad", 
                                   data=pdf_output,
                                   file_name=f"Planeacion_Comunitaria_{ec}.pdf", 
                                   mime="application/pdf")
