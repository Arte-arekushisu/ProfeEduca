import streamlit as st
import requests
from io import BytesIO
from docx import Document

# 1. Configuración
st.set_page_config(page_title="Planeador y Bitácora ABCD", page_icon="🍎", layout="wide")
st.title("🍎 Gestión Pedagógica ABCD: Planeación + Reflexión")

# 2. Función para generar el documento Word
def crear_word(datos, contenido_ia):
    doc = Document()
    doc.add_heading('REPORTE DIARIO DE TUTORÍA - MODELO ABCD', 0)
    
    # Datos generales
    p = doc.add_paragraph()
    p.add_run(f"Comunidad: {datos['comunidad']} | Fecha: {datos['fecha']}\n").bold = True
    p.add_run(f"Educador: {datos['nombre_ec']} | ECA: {datos['eca']}")

    doc.add_heading('I. Planeación y Objetivos', level=1)
    doc.add_paragraph(contenido_ia.split("---")[0]) # Parte 1: Planeación

    if "---" in contenido_ia:
        doc.add_heading('II. Evaluación y Texto Reflexivo del Día', level=1)
        doc.add_paragraph(contenido_ia.split("---")[1]) # Parte 2: Reflexión

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 3. Función de IA: Genera Planeación + Reflexión a partir de notas breves
def llamar_ia_completo(datos, notas_aula):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    
    prompt = f"""
    Actúa como tutor experto CONAFE.
    DATOS DEL DÍA:
    - Tema: {datos['temas']}
    - Notas de lo que pasó en el aula: {notas_aula}
    
    GENERA:
    1. PLANEACIÓN: Objetivo, desafío y ruta para mañana.
    2. EVALUATORIO: Breve análisis del avance del alumno hoy.
    3. TEXTO REFLEXIVO: Redacta un texto reflexivo profesional de 2 párrafos basado en las notas del usuario, usando lenguaje del Modelo ABCD (diálogo, tutoría, aprendizaje autónomo).
    
    Separa la Planeación de la Reflexión con tres guiones (---).
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text'] if res.status_code == 200 else "Error"

# 4. Interfaz
with st.sidebar:
    st.header("📋 Datos de Control")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    fecha = st.date_input("Fecha")
    tiempos = st.text_input("Horario", "8:00 AM - 2:00 PM")

col1, col2 = st.columns(2)

with col1:
    temas = st.text_input("Tema central:")
    notas_aula = st.text_area("📝 ¿Qué pasó hoy con el alumno? (Notas breves):", 
                               placeholder="Ej: El alumno se distrajo con el dibujo pero logró explicar la meta con sus palabras.")

if st.button("🚀 Generar Planeación, Evaluación y Reflexión"):
    if temas and notas_aula:
        datos = {"comunidad": comunidad, "nombre_ec": nombre_ec, "eca": eca, "fecha": str(fecha), "temas": temas}
        with st.spinner("La IA está analizando tu práctica docente..."):
            resultado = llamar_ia_completo(datos, notas_aula)
            st.session_state.resultado = resultado
            st.session_state.datos = datos
    else:
        st.warning("Escribe el tema y las notas del día.")

# 5. Resultados y Descarga
if "resultado" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state.resultado)
    
    archivo = crear_word(st.session_state.datos, st.session_state.resultado)
    st.download_button(label="📥 Descargar Reporte Completo (Word)", 
                       data=archivo, 
                       file_name=f"Reporte_ABCD_{fecha}.docx")
