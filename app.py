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
            messages=[{"role": "system", "content": "Eres un experto pedagogo. Generas planeaciones detalladas para educadores, sin usar asteriscos (*), con lenguaje formal y horarios precisos."},
                      {"role": "user", "content": prompt}],
            temperature=0.6, max_tokens=4500
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

# --- 3. GENERACIÓN DE PDF (DISEÑO PROFESIONAL B/N) ---
def generar_pdf(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado con Estilo
    pdf.set_font("Arial", 'B', 18)
    pdf.set_fill_color(30, 30, 30) # Gris muy oscuro para el header
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, txt="PLANEACIÓN PROFESIONAL ABCD", ln=True, align='C', fill=True)
    pdf.ln(5)
    
    # Cuadro de datos con bordes reforzados
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    
    # Primera fila
    pdf.cell(95, 10, txt=f" EDUCADO/A (E.C.): {datos['ec'].upper()}", border=1, fill=True)
    pdf.cell(95, 10, txt=f" ACOMPAÑANTE (E.C.A.): {datos['eca'].upper()}", border=1, fill=True, ln=True)
    
    # Segunda fila
    pdf.set_fill_color(255, 255, 255)
    pdf.cell(95, 10, txt=f" COMUNIDAD: {datos['comunidad']}", border=1)
    pdf.cell(95, 10, txt=f" NIVEL: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    
    # Tercera fila
    pdf.cell(95, 10, txt=f" TEMA CENTRAL: {datos['rincon']}", border=1)
    pdf.cell(95, 10, txt=f" VIGENCIA: {datos['duracion']}", border=1, ln=True)
    pdf.ln(10)

    # Cuerpo del Contenido
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="DESARROLLO PEDAGÓGICO Y CRONOGRAMA", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Línea divisoria
    pdf.ln(2)
    
    pdf.set_font("Arial", size=10)
    # Limpiar caracteres no compatibles con latin-1
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Pro ✏️</div>', unsafe_allow_html=True)

with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        ec = st.text_input("Nombre del Educador (E.C.)")
        eca = st.text_input("Nombre del Acompañante (E.C.A.)")
        comu = st.text_input("Comunidad")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria", "Multigrado"])
    with c2:
        grados = st.text_input("Grado(s)")
        duracion = st.selectbox("Periodo de Planeación", ["1 Día", "1 Semana Hábil", "2 Semanas Hábiles"])
        rincon = st.text_input("Rincón o Tema Principal")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Desarrollo de la Relación Tutora (Contenido y Bibliografía)")
    post_receso_req = st.text_area("Notas para Post-Receso (Materias o proyectos específicos)")

    boton_generar = st.form_submit_button("🚀 Generar Planeación Completa")

if boton_generar:
    if not ec or not tema_tutora:
        st.error("Por favor completa los campos de Educador y Tema de Tutoría.")
    else:
        with st.spinner(f"Diseñando planeación detallada para {duracion}..."):
            prompt_maestro = f"""
            Genera una PLANEACIÓN PROFESIONAL ABCD para {duracion} sin mencionar instituciones específicas. 
            USA UN LENGUAJE FORMAL Y PROFESIONAL. NO USES ASTERISCOS (*).

            1. ACTIVIDADES INICIALES DIARIAS:
               - Diseña un PASE DE LISTA CREATIVO, un REGALO DE LECTURA (título y breve actividad) y una BIENVENIDA motivadora, todo adaptado al nivel {nivel} y grados {grados}.

            2. HORARIO DETALLADO (8:00 AM - 2:00 PM):
               - Estructura el tiempo con minutos exactos para cada fase del modelo ABCD (Inicio, Tutoría, Receso, Estaciones, Cierre).

            3. RELACIÓN TUTORA (EXTENSA):
               - Expande el tema {tema_tutora}. Incluye 5 PREGUNTAS DETONANTES que fomenten el pensamiento crítico y una sección de bibliografía consultada.

            4. 4 ESTACIONES AUTÓNOMAS CON MATERIAL RECICLADO:
               - Una estación por cada Campo Formativo (Lenguajes, Saberes, Ética, De lo Humano).
               - Para cada una, describe: NOMBRE LLAMATIVO, PASOS A SEGUIR PARA EL ALUMNO (que trabaje solo) e INSTRUCCIONES DE DESARROLLO.

            5. CRONOGRAMA SEMANAL POST-RECESO:
               - Crea una secuencia de actividades para el bloque post-receso que cambie cada día de la semana (Lunes a Viernes), incluyendo procedimientos detallados basados en: {post_receso_req}.
            """
            
            respuesta_ia, motor = llamar_ia(prompt_maestro)
            
            if respuesta_ia:
                st.success(f"Planeación generada con éxito.")
                st.write(respuesta_ia)
                
                datos_doc = {"ec": ec, "eca": eca, "comunidad": comu, "nivel": nivel, 
                             "grados": grados, "duracion": duracion, "rincon": rincon, 
                             "fecha": fecha_gen}
                
                pdf_output = generar_pdf(datos_doc, respuesta_ia)
                st.download_button(label="📥 Descargar Planeación PDF (B/N Profesional)", 
                                   data=pdf_output,
                                   file_name=f"Planeacion_ABCD_{ec}.pdf", 
                                   mime="application/pdf")
