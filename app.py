import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Pt

# 1. Configuración de Estilo y Modo Oscuro
st.set_page_config(page_title="Profe.Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .welcome-box {
        padding: 30px; border-radius: 15px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #00d4ff; margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; font-weight: bold; height: 3em;
    }
    .delete-btn>button { background: linear-gradient(45deg, #ff4b4b, #990000) !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de "Base de Datos" en Memoria (Session State)
if 'db_reflexiones' not in st.session_state:
    st.session_state.db_reflexiones = []

# 3. Funciones de Exportación a Word
def exportar_word(titulo, contenido, datos_extra=None):
    doc = Document()
    header = doc.add_heading(titulo, 0)
    
    if datos_extra:
        p = doc.add_paragraph()
        for k, v in datos_extra.items():
            p.add_run(f"{k}: ").bold = True
            p.add_run(f"{v}\n")
    
    doc.add_paragraph(contenido)
    
    # Sección de Firmas al final
    doc.add_paragraph("\n" + "_"*30 + "\t\t" + "_"*30)
    doc.add_paragraph("Firma del Educador\t\tFirma del Padre de Familia / APEC")
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 4. Navegación Lateral
with st.sidebar:
    st.title("🍎 Profe.Educa")
    opcion = st.radio("MENÚ:", ["🏠 Inicio", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral"])
    st.divider()
    st.subheader("📍 Identificación General")
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador Comunitario")
    eca = st.text_input("ECA")
    nivel = st.selectbox("Nivel Educativo:", [
        "Preescolar 1º", "Preescolar 2º", "Preescolar 3º",
        "Primaria 1º", "Primaria 2º", "Primaria 3º", "Primaria 4º", "Primaria 5º", "Primaria 6º", "Primaria Multigrado",
        "Secundaria 1º", "Secundaria 2º", "Secundaria 3º", "Secundaria Multigrado"
    ])

# 5. Función de IA
def llamar_ia(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 4096}}
    res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- SECCIONES ---

if opcion == "🏠 Inicio":
    st.markdown(f"""
    <div class="welcome-box">
        <h1>¡Bienvenido a tu Centro de Planeación Inteligente! 🚀</h1>
        <p style="font-size: 1.2em;">
            Diseñado para que tu labor sea impecable. Este sistema coordina con precisión el <b>Regalo de Lectura</b>, 
            el <b>Pase de Lista</b> y la <b>Relación Tutora</b>. Aquí, cada segundo en el aula está optimizado 
            para que te enfoques en lo que importa: el aprendizaje de tus alumnos. 
            <b>Confía en el proceso, nosotros cuidamos la estructura.</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

elif opcion == "📅 Planeación Semanal":
    st.header("🗓️ Planeación Semanal con Tiempos Pedagógicos")
    obj_general = st.text_area("Objetivo General de la Semana:")
    tema_p = st.text_input("Tema Principal:")
    
    if st.button("Generar Planeación en Word"):
        prompt = f"Genera planeación para {nivel} en {comunidad}. Objetivo: {obj_general}. Tema: {tema_p}. Incluye horarios desde 8:00 AM con Regalo de Lectura, Pase de Lista, bloques de Tutoría antes y después del receso, y temas de reserva."
        res = llamar_ia(prompt)
        st.markdown(res)
        st.download_button("Descargar Word", exportar_word("Planeación Semanal", res), "Planeacion.docx")

elif opcion == "✍️ Reflexión Diaria":
    st.header("✍️ Bitácora Individual por Alumno")
    nombre_alumno = st.text_input("Nombre del Alumno:")
    campo = st.selectbox("Campo Formativo:", ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"])
    notas = st.text_area("Notas del aprendizaje observado hoy:")
    
    if st.button("Guardar y Redactar Reflexión"):
        prompt = f"Redacta texto reflexivo extenso para {nombre_alumno} ({nivel}) en el campo {campo}. Notas: {notas}."
        res = llamar_ia(prompt)
        st.session_state.db_reflexiones.append({"alumno": nombre_alumno, "campo": campo, "fecha": str(st.date_input), "texto": res})
        st.success("Guardado en la base de datos.")
        st.markdown(res)
        st.download_button("Descargar Word", exportar_word(f"Reflexión - {nombre_alumno}", res), "Reflexion.docx")
    
    st.divider()
    st.subheader("🗑️ Gestionar Registros")
    if st.session_state.db_reflexiones:
        for i, ref in enumerate(st.session_state.db_reflexiones):
            st.write(f"{ref['alumno']} - {ref['campo']}")
            if st.button(f"Eliminar registro {i}", key=f"del_{i}"):
                st.session_state.db_reflexiones.pop(i)
                st.rerun()

elif opcion == "📊 Evaluación Trimestral":
    st.header("📊 Texto Reflexivo Trimestral")
    alumno_evaluar = st.text_input("Nombre del Alumno a Evaluar:")
    
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.number_input("Calif. Lenguajes", 0, 10)
        c2 = st.number_input("Calif. Saberes", 0, 10)
    with col2:
        c3 = st.number_input("Calif. Ética", 0, 10)
        c4 = st.number_input("Calif. Humano/Comunitario", 0, 10)

    if st.button("Generar Evaluación Trimestral"):
        # Filtramos reflexiones del alumno
        reflexiones_alumno = [r['texto'] for r in st.session_state.db_reflexiones if r['alumno'] == alumno_evaluar]
        contexto = "\n".join(reflexiones_alumno)
        
        prompt = f"""Genera Texto Reflexivo Trimestral extenso (máx 3 hojas) para {alumno_evaluar}. 
        Campos: Lenguajes ({c1}), Saberes ({c2}), Ética ({c3}), Humano ({c4}).
        Basado en estas reflexiones previas: {contexto}. 
        Incluye temas dominados, aprendizajes significativos y un espacio final para 'Compromisos del Alumno'."""
        
        res = llamar_ia(prompt)
        st.markdown(res)
        st.download_button("Descargar Evaluación Word", exportar_word(f"Evaluación Trimestral - {alumno_evaluar}", res), "Evaluacion.docx")
