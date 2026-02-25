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
            messages=[{"role": "system", "content": "Eres un experto pedagogo para educadores comunitarios. Generas planeaciones exhaustivas, sin asteriscos (*), con lenguaje formal y tablas de tiempo precisas."},
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
    
    # Encabezado con Estilo Corporativo
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(0, 0, 0) 
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, txt="GUÍA DE APRENDIZAJE Y PLANEACIÓN ABCD", ln=True, align='C', fill=True)
    pdf.ln(5)
    
    # Tabla de Datos de Identificación (Diseño Profesional)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    
    # Filas de la tabla
    col_width = 95
    pdf.cell(col_width, 8, txt=f" EDUCADO/A (E.C.): {datos['ec'].upper()}", border=1, fill=True)
    pdf.cell(col_width, 8, txt=f" ACOMPAÑANTE (E.C.A.): {datos['eca'].upper()}", border=1, fill=True, ln=True)
    
    pdf.set_fill_color(255, 255, 255)
    pdf.cell(col_width, 8, txt=f" COMUNIDAD: {datos['comunidad']}", border=1)
    pdf.cell(col_width, 8, txt=f" NIVEL / GRADO: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    
    pdf.cell(col_width, 8, txt=f" TEMA PRINCIPAL: {datos['rincon']}", border=1)
    pdf.cell(col_width, 8, txt=f" FECHA DE INICIO: {datos['fecha']}", border=1, ln=True)
    pdf.ln(10)

    # Cuerpo del Contenido
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="I. ESTRUCTURA DIDÁCTICA Y SECUENCIA", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", size=10)
    # Limpieza de caracteres para codificación PDF
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, txt=texto_limpio)
    
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
        grados = st.text_input("Grado(s) Específicos")
        duracion = st.selectbox("Duración de la Planeación", ["1 Día", "1 Semana Hábil", "2 Semanas Hábiles"])
        rincon = st.text_input("Rincón / Tema de Interés")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Desarrollo del Tema (Para Relación Tutora)")
    post_receso_req = st.text_area("Materias/Actividades para el bloque Post-Receso")

    boton_generar = st.form_submit_button("🚀 Generar Planeación Profesional")

if boton_generar:
    if not ec or not tema_tutora:
        st.error("Por favor completa los datos básicos y el tema de tutoría.")
    else:
        with st.spinner("Procesando pedagogía avanzada..."):
            prompt_maestro = f"""
            Genera una PLANEACIÓN PROFESIONAL ABCD para {duracion}. 
            REGLA DE ORO: NO USES ASTERISCOS (*). Usa títulos en MAYÚSCULAS.

            1. INICIO DE JORNADA (8:00 AM - 8:45 AM):
               - PASE DE LISTA CREATIVO: Una dinámica original adaptada a {nivel}.
               - REGALO DE LECTURA: Título sugerido, autor y una actividad de reflexión post-lectura.
               - BIENVENIDA: Mensaje motivador para los alumnos de {grados}.

            2. HORARIO Y TIEMPOS (DETALLADO):
               - Cronograma minuto a minuto de 8:00 AM a 2:00 PM cubriendo Tutoría, Receso, Estaciones y Cierre.

            3. TEMA DE INTERÉS (RELACIÓN TUTORA):
               - Desarrollo académico extenso sobre: {tema_tutora}.
               - Agrega 5 PREGUNTAS DETONANTES para iniciar el diálogo.
               - Incluye Bibliografía sugerida.

            4. 4 ESTACIONES AUTÓNOMAS (MATERIAL RECICLADO):
               - Estaciones: Lenguajes, Saberes, Ética, De lo Humano.
               - Para cada una: Nombre llamativo, PASOS A SEGUIR POR EL ALUMNO (1, 2, 3...) y descripción del material reciclado a usar.

            5. CRONOGRAMA POST-RECESO (LUNES A VIERNES):
               - Si es semanal, detalla una actividad diferente por cada día (Lunes a Viernes) basada en {post_receso_req}. 
               - Explica el procedimiento paso a paso de cada tarde.
            """
            
            respuesta_ia, motor = llamar_ia(prompt_maestro)
            
            if respuesta_ia:
                st.success("Planeación generada.")
                st.markdown(respuesta_ia)
                
                datos_doc = {"ec": ec, "eca": eca, "comunidad": comu, "nivel": nivel, 
                             "grados": grados, "duracion": duracion, "rincon": rincon, 
                             "fecha": fecha_gen}
                
                pdf_output = generar_pdf(datos_doc, respuesta_ia)
                st.download_button(label="📥 Descargar Planeación PDF (B/N Profesional)", 
                                   data=pdf_output,
                                   file_name=f"Planeacion_ABCD_{ec}.pdf", 
                                   mime="application/pdf")
