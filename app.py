import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq
import io

# --- 1. CONFIGURACIÓN ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="ProfeEduca ABCD Ultra", page_icon="🍎", layout="wide")

# --- 2. LÓGICA DE INTELIGENCIA ---
def llamar_ia(prompt):
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un experto en el modelo ABCD y la Nueva Escuela Mexicana. Generas planeaciones pedagógicas ultra detalladas, sin asteriscos (*), enfocadas en el contexto comunitario y multigrado."},
                      {"role": "user", "content": prompt}],
            temperature=0.4, max_tokens=5500
        )
        texto = completion.choices[0].message.content
        return texto.replace("*", ""), "Groq"
    except:
        return "Error en la conexión con la IA. Inténtalo de nuevo.", None

# --- 3. GENERACIÓN DE PDF ---
def generar_pdf(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado Tipo Registro Oficial
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(40, 40, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, txt="REGISTRO DE PLANEACIÓN PEDAGÓGICA - MODELO ABCD", ln=True, align='C', fill=True)
    pdf.ln(5)
    
    # Tabla de Datos
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 8)
    pdf.set_fill_color(245, 245, 245)
    
    # Filas
    pdf.cell(95, 8, txt=f" E.C.: {datos['ec'].upper()}", border=1, fill=True)
    pdf.cell(95, 8, txt=f" E.C.A.: {datos['eca'].upper()}", border=1, fill=True, ln=True)
    pdf.cell(95, 8, txt=f" COMUNIDAD: {datos['comu']}", border=1)
    pdf.cell(95, 8, txt=f" FECHA: {datos['fecha']}", border=1, ln=True)
    pdf.cell(190, 8, txt=f" UNIDAD DE APRENDIZAJE / RINCÓN: {datos['rincon']}", border=1, ln=True)
    pdf.ln(8)

    # Contenido
    pdf.set_font("Arial", size=10)
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
st.markdown('<h1 style="color:#38bdf8; text-align:center;">📏 ProfeEduca ABCD Ultra ✏️</h1>', unsafe_allow_html=True)

with st.form("form_ultra"):
    col1, col2 = st.columns(2)
    with col1:
        ec = st.text_input("Nombre del E.C.")
        eca = st.text_input("Nombre del E.C.A.")
        comu = st.text_input("Nombre de la Comunidad")
        nivel = st.multiselect("Nivel(es) en el aula", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"], default=["Primaria Alta"])
    with col2:
        rincon = st.text_input("Tema de la Unidad (Rincón)")
        duracion = st.selectbox("Temporalidad", ["1 Semana", "2 Semanas"])
        estilo = st.radio("Enfoque prioritario", ["Académico", "Comunitario/Práctico", "Artes y Creatividad"])
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    tema_guia = st.text_area("Desarrollo de la Relación Tutora (Contenido base para el diálogo)")
    obs_extra = st.text_area("PDA específicos o materiales locales disponibles")

    submit = st.form_submit_button("🚀 Generar Guía Completa")

if submit:
    with st.spinner("Construyendo la arquitectura pedagógica..."):
        prompt_final = f"""
        Genera una PLANEACIÓN PEDAGÓGICA ABCD PROFESIONAL para {duracion}.
        CONTEXTO: Aula multigrado con niveles: {', '.join(nivel)}.
        ENFOQUE: {estilo}.
        
        REQUISITOS OBLIGATORIOS (SIN ASTERISCOS):
        
        1. IDENTIFICACIÓN DE PDA (Procesos de Desarrollo de Aprendizaje): 
           - Define al menos 2 PDA por nivel educativo presentes basado en el tema {tema_guia}.
        
        2. RUTA DE APRENDIZAJE DIARIA (8:00 AM - 2:00 PM):
           - Describe el 'Gobierno Escolar' (inicio), 'Tutoría entre pares', 'Receso' y 'Cierre reflexivo'.
        
        3. RELACIÓN TUTORA (EL CORAZÓN):
           - Una explicación profunda del tema {tema_guia}.
           - Incluye 5 PREGUNTAS DETONANTES que generen conflicto cognitivo.
           - Propón un 'Producto Final' de la tutoría (RPA).
        
        4. 4 ESTACIONES DE TRABAJO AUTÓNOMO (DIFERENCIADAS):
           - Estación 1 (Lenguajes): Pasos para el alumno y material reciclado.
           - Estación 2 (Saberes y P. Científico): Actividad de lógica o experimentación.
           - Estación 3 (Ética, Nat. y Soc.): Relación con el entorno de la comunidad.
           - Estación 4 (De lo Humano y lo Comu.): Habilidades socioemocionales.
           - Cada estación debe tener una instrucción clara de '¿Qué hacer si terminé rápido?'.
        
        5. CRONOGRAMA POST-RECESO:
           - Actividades detalladas día por día (Lunes a Viernes) para proyectos comunitarios o materias complementarias.
        """
        
        respuesta, motor = llamar_ia(prompt_final)
        
        if respuesta:
            st.markdown(respuesta)
            datos = {"ec": ec, "eca": eca, "comu": comu, "rincon": rincon, "fecha": fecha_hoy, "duracion": duracion}
            pdf_out = generar_pdf(datos, respuesta)
            st.download_button("📥 Descargar Planeación Ultra (PDF)", pdf_out, f"Planeacion_{ec}.pdf", "application/pdf")
