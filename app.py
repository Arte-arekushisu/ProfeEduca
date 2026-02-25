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

# Estilos Visuales - FONDO OSCURO
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); 
        color: #f8fafc; 
    }
    .brand-header { 
        font-size: 2.5rem; 
        font-weight: 900; 
        color: #38bdf8; 
        text-align: center; 
        padding: 20px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        background-color: #1e293b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGENCIA ---
def llamar_ia(prompt):
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un experto en el modelo ABCD y la Nueva Escuela Mexicana. Generas planeaciones detalladas por día, sin asteriscos (*), enfocadas en el contexto comunitario y materias académicas específicas."},
                      {"role": "user", "content": prompt}],
            temperature=0.4, max_tokens=6000
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
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(40, 40, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, txt="REGISTRO DE PLANEACIÓN PEDAGÓGICA - MODELO ABCD", ln=True, align='C', fill=True)
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 8)
    pdf.set_fill_color(245, 245, 245)
    
    pdf.cell(95, 8, txt=f" E.C.: {datos['ec'].upper()}", border=1, fill=True)
    pdf.cell(95, 8, txt=f" E.C.A.: {datos['eca'].upper()}", border=1, fill=True, ln=True)
    pdf.cell(95, 8, txt=f" COMUNIDAD: {datos['comu']}", border=1)
    pdf.cell(95, 8, txt=f" FECHA: {datos['fecha']}", border=1, ln=True)
    pdf.cell(190, 8, txt=f" UNIDAD DE APRENDIZAJE / RINCÓN: {datos['rincon']}", border=1, ln=True)
    pdf.ln(8)

    pdf.set_font("Arial", size=10)
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Ultra ✏️</div>', unsafe_allow_html=True)

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
    obs_extra = st.text_area("Materias específicas para Post-Receso (Ej: Fracciones, Tipos de texto, etc.)")

    submit = st.form_submit_button("🚀 Generar Guía Completa")

if submit:
    with st.spinner("Construyendo la arquitectura pedagógica semanal..."):
        prompt_final = f"""
        Genera una PLANEACIÓN PEDAGÓGICA ABCD PROFESIONAL para {duracion}.
        CONTEXTO: Aula multigrado con niveles: {', '.join(nivel)}.
        ENFOQUE: {estilo}.
        
        REQUISITOS OBLIGATORIOS (SIN ASTERISCOS):
        
        1. MOMENTOS INICIALES SEMANALES:
           - Diseña una tabla o lista que contenga para cada día (Lunes a Viernes): Un PASE DE LISTA diferente, un REGALO DE LECTURA distinto y una DINÁMICA DE BIENVENIDA única.

        2. RELACIÓN TUTORA (EL CORAZÓN):
           - Una explicación académica profunda del tema {tema_guia}.
           - Incluye 5 PREGUNTAS DETONANTES que generen conflicto cognitivo.
           - Propón un RPA (Registro de Proceso de Aprendizaje).

        3. 4 ESTACIONES AUTÓNOMAS (DIFERENTES CADA DÍA):
           - Genera actividades para 4 estaciones (Lenguajes, Saberes, Ética, De lo Humano).
           - IMPORTANTE: Las actividades de las estaciones NO deben estar relacionadas con {tema_guia}. Deben ser temas generales de cultura o habilidades.
           - Provee 3 actividades breves por estación para cada día de la semana.

        4. CRONOGRAMA ACADÉMICO POST-RECESO (INDEPENDIENTE):
           - Crea una secuencia diaria (Lunes a Viernes) enfocada exclusivamente en materias:
             * Lunes: Español / Lenguajes.
             * Martes: Matemáticas / Saberes.
             * Miércoles: Ciencias / Naturaleza.
             * Jueves: Formación Cívica / Ética.
             * Viernes: Educación Física o Artes / De lo Humano.
           - Utiliza como base estos requerimientos: {obs_extra}. Las actividades deben ser detalladas y adecuadas al grado/nivel {', '.join(nivel)}.

        5. IDENTIFICACIÓN DE PDA:
           - Define al menos 2 PDA por nivel educativo basados en el programa sintético actual.
        """
        
        respuesta, motor = llamar_ia(prompt_final)
        
        if respuesta:
            st.markdown(respuesta)
            datos = {"ec": ec, "eca": eca, "comu": comu, "rincon": rincon, "fecha": fecha_hoy, "duracion": duracion}
            pdf_out = generar_pdf(datos, respuesta)
            st.download_button("📥 Descargar Planeación Ultra (PDF)", pdf_out, f"Planeacion_{ec}.pdf", "application/pdf")
