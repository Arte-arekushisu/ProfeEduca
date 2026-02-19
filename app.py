import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Configuración de Estilo Dark y Página
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .welcome-box {
        padding: 30px; border-radius: 15px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #00d4ff; margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; font-weight: bold; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Función de Exportación a Word (Corregida con JUSTIFY)
def generar_word(titulo, contenido, d):
    doc = Document()
    # Título centrado
    h = doc.add_heading(titulo, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Encabezado con datos del educador
    table = doc.add_table(rows=3, cols=2)
    table.cell(0, 0).text = f"Comunidad: {d['comunidad']}"
    table.cell(0, 1).text = f"Fecha: {d['fecha']}"
    table.cell(1, 0).text = f"Educador: {d['nombre']}"
    table.cell(1, 1).text = f"Nivel: {d['nivel']}"
    table.cell(2, 0).text = f"ECA: {d['eca']}"
    
    doc.add_paragraph("\n" + "="*50 + "\n")
    
    # Contenido con alineación justificada
    para = doc.add_paragraph(contenido)
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # Espacio para firmas
    doc.add_paragraph("\n\n\n")
    f_table = doc.add_table(rows=1, cols=2)
    f_table.cell(0, 0).text = "__________________________\nFirma del Educador"
    f_table.cell(0, 1).text = "__________________________\nFirma Padre/APEC"
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Sidebar: Identificación y Menú
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    st.divider()
    comunidad = st.text_input("Comunidad", "PARAJES DEL VALLE")
    nombre_ec = st.text_input("Educador Comunitario", "AXEL REYES")
    eca = st.text_input("ECA", "MOISES ROSAS")
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar 1º", "Preescolar 2º", "Preescolar 3º",
        "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º",
        "Primaria Multigrado",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º",
        "Secundaria Multigrado"
    ])
    fecha_hoy = st.date_input("Fecha")

# Datos para el encabezado del Word
datos_id = {
    "comunidad": comunidad, 
    "nombre": nombre_ec, 
    "eca": eca, 
    "nivel": nivel, 
    "fecha": str(fecha_hoy)
}

# 4. Función de Inteligencia Artificial
def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}], 
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    }
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error al conectar con la IA. Verifica tu API Key."

# --- SECCIONES DE LA APP ---

if opcion == "🏠 Inicio":
    st.markdown(f"""
    <div class="welcome-box">
        <h1>¡Bienvenido a tu Espacio de Confianza, Profe! 🍎</h1>
        <p style="font-size: 1.2em;">
            Aquí tienes la seguridad de que tu labor docente está respaldada por tecnología de vanguardia. 
            Este sistema coordina con precisión el <b>Regalo de Lectura</b>, la <b>Dinámica de Bienvenida</b>, 
            el <b>Pase de Lista</b> y la <b>Relación Tutora</b> en tus estaciones de trabajo. 
            Confía en el proceso: estamos aquí para que tu planeación sea impecable, pedagógicamente sólida y sin errores.
        </p>
        <hr style="border-color: #00d4ff;">
        <p style="font-style: italic; color: #00d4ff;">
            "La educación es el arma más poderosa para cambiar el mundo." — ¡Vamos a planear con excelencia!
        </p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header(f"🗓️ Planeación: {nivel}")
    obj_general = st.text_area("Objetivo General de la Semana:")
    tema_p = st.text_input("Tema Principal:")
    
    if st.button("🚀 Generar Planeación Semanal Completa"):
        with st.spinner("Diseñando jornada pedagógica..."):
            prompt = f"""
            Actúa como experto pedagogo CONAFE para {nivel}. 
            Genera una planeación semanal detallada (Lunes a Viernes) para el tema '{tema_p}'.
            Objetivo: {obj_general}.
            INCLUYE PARA CADA DÍA:
            1. Dinámica de bienvenida y Pase de lista.
            2. Regalo de Lectura (Sugerencia de libro y actividad).
            3. Creación de Estaciones de Trabajo temporales dentro de los Rincones permanentes.
            4. Tiempos para Relación Tutora antes y después del receso.
            5. Dos temas de reserva y enlaces de estudio (YouTube/Google).
            Estructura todo por horarios detallados.
            """
            resultado = llamar_ia(prompt)
            st.markdown(resultado)
            st.download_button(
                label="📥 Descargar Planeación para Imprimir (Word)", 
                data=generar_word("PLANEACIÓN SEMANAL", resultado, datos_id), 
                file_name=f"Planeacion_{comunidad}.docx"
            )

elif opcion == "✍️ Reflexión Diaria":
    st.header(f"✍️ Reflexión Diaria: {nivel}")
    nombre_alumno = st.text_input("Nombre del Alumno:")
    notas = st.text_area("Notas del aprendizaje observado hoy (Relación tutora/Estaciones):")
    
    if st.button("🪄 Redactar Reflexión Profunda"):
        with st.spinner("Redactando texto reflexivo..."):
            prompt = f"""
            Redacta un texto reflexivo diario MUY EXTENSO (mínimo 2 páginas) para el alumno {nombre_alumno} de {nivel}.
            Contexto: {comunidad}. Notas observadas: {notas}.
            Usa terminología del Modelo ABCD: relación tutora, diálogo, aprendizaje autónomo y metacognición.
            """
            resultado = llamar_ia(prompt)
            st.markdown(resultado)
            st.download_button(
                label="📥 Descargar Reflexión (Word)", 
                data=generar_word(f"REFLEXIÓN DIARIA - {nombre_alumno}", resultado, datos_id), 
                file_name=f"Reflexion_{nombre_alumno}.docx"
            )

elif opcion == "📊 Evaluación Trimestral":
    st.header(f"📊 Evaluación Trimestral por Alumno")
    alumno_ev = st.text_input("Nombre del Alumno a Evaluar:")
    resumen_notas = st.text_area("Pega aquí las notas o reflexiones acumuladas del trimestre:")
    
    if st.button("📈 Generar Evaluación y Compromisos"):
        with st.spinner("Analizando proceso trimestral..."):
            prompt = f"""
            Genera un Texto Reflexivo Trimestral formal y extenso para {alumno_ev} en {nivel}.
            Basado en estos datos: {resumen_notas}.
            Analiza los avances por Campos Formatvivos (Lenguajes, Saberes, Ética, Humano).
            Menciona temas dominados y aprendizajes significativos observados.
            Incluye un apartado final de 'Compromisos del Alumno' para escribir a mano.
            """
            resultado = llamar_ia(prompt)
            st.markdown(resultado)
            st.download_button(
                label="📥 Descargar Evaluación Trimestral (Word)", 
                data=generar_word(f"EVALUACIÓN TRIMESTRAL - {alumno_ev}", resultado, datos_id), 
                file_name=f"Evaluacion_{alumno_ev}.docx"
            )
