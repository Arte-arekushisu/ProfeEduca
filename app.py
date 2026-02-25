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
            messages=[{"role": "system", "content": "Eres un experto creativo en el modelo ABCD de CONAFE. Generas planeaciones innovadoras, con nombres llamativos y contenido diversificado día por día, sin usar asteriscos (*)."},
                      {"role": "user", "content": prompt}],
            temperature=0.7, max_tokens=6000
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
    obs_extra = st.text_area("Materias específicas para Post-Receso (Opcional)")

    submit = st.form_submit_button("🚀 Generar Planeación Creativa")

if submit:
    with st.spinner("La IA está diseñando una semana creativa..."):
        prompt_final = f"""
        Genera una PLANEACIÓN PEDAGÓGICA ABCD PROFESIONAL para {duracion}.
        CONTEXTO: Aula multigrado con niveles: {', '.join(nivel)}.
        ENFOQUE: {estilo}.
        
        INSTRUCCIONES DE LIBERTAD CREATIVA:
        
        1. MOMENTOS INICIALES (LUNES A VIERNES):
           - Inventa dinámicas originales para el PASE DE LISTA, REGALO DE LECTURA y BIENVENIDA. Que cada día sea una experiencia distinta.

        2. RELACIÓN TUTORA:
           - Desarrolla el tema {tema_guia} con profundidad académica, 5 preguntas de alto nivel cognitivo y un producto final (RPA).

        3. 4 ESTACIONES AUTÓNOMAS (DIARIAS Y CREATIVAS):
           - Crea 4 estaciones con NOMBRES FANTÁSTICOS Y LLAMATIVOS (libre elección de la IA).
           - Propón 3 actividades por día para cada estación que NO tengan relación con {tema_guia}.
           - Enfócate en retos, juegos lógicos, expresión artística y experimentos.

        4. CRONOGRAMA POST-RECESO ACADÉMICO:
           - Secuencia diaria obligatoria: Lunes (Español), Martes (Mate), Miércoles (Ciencias), Jueves (Cívica), Viernes (Artes/Física).
           - Integra estos requerimientos si existen: {obs_extra}. Las actividades deben ser académicamente sólidas para {', '.join(nivel)}.

        5. PDA Y EVALUACIÓN:
           - Incluye los PDA correspondientes y una técnica de cierre reflexivo para el viernes.
           
        NO USES ASTERISCOS EN NINGUNA PARTE.
        """
        
        respuesta, motor = llamar_ia(prompt_final)
        
        if respuesta:
            st.markdown(respuesta)
            datos = {"ec": ec, "eca": eca, "comu": comu, "rincon": rincon, "fecha": fecha_hoy, "duracion": duracion}
            pdf_out = generar_pdf(datos, respuesta)
            st.download_button("📥 Descargar Planeación Ultra (PDF)", pdf_out, f"Planeacion_{ec}.pdf", "application/pdf")
