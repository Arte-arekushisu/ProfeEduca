import streamlit as st
from fpdf import FPDF

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 10s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; text-shadow: 0 0 15px #00d4ff; }
    .stTextInput, .stTextArea, .stSelectbox { background-color: rgba(255,255,255,0.05) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES TÉCNICAS
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'SISTEMA INTEGRAL DE EVALUACION Y PLANEACION ABCD', 0, 1, 'C')
        self.ln(5)

# 3. BASE DE DATOS PERSISTENTE
if 'db' not in st.session_state:
    st.session_state.db = {"auth": False, "user": "", "alumnos": {}}

# 4. LÓGICA DE ACCESO
if not st.session_state.db["auth"]:
    st.markdown("<h1>Profe Educa: Modelo ABCD</h1>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Usuario (EC)")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("ENTRAR"):
            st.session_state.db.update({"auth": True, "user": u})
            st.rerun()
else:
    st.sidebar.title(f"EC: {st.session_state.db['user']}")
    menu = st.sidebar.radio("MENÚ", ["📅 Planeación ABCD (IA)", "✍️ Diario Reflexivo", "📊 Evaluación y Calificaciones"])

    # --- SECCIÓN 1: PLANEACIÓN CON CONTENIDO PEDAGÓGICO ---
    if menu == "📅 Planeación ABCD (IA)":
        st.header("Generador de Secuencia Didáctica ABCD")
        niveles = ["Preescolar", "Primaria 1°-3°", "Primaria 4°-6°", "Secundaria"]
        col1, col2 = st.columns(2)
        nivel = col1.selectbox("Nivel", niveles)
        tema = col2.text_input("Tema de Interés")
        
        if st.button("Generar Planeación con Contenido Educativo"):
            # Simulación de IA con estructura CONAFE
            secuencia = {
                "Inicio": f"Activación de conocimientos previos sobre {tema}. Planteamiento de reto inicial.",
                "Desarrollo": f"Indagación guiada en la estación. Uso de materiales concretos para resolver: ¿Cómo influye {tema} en la comunidad?",
                "Cierre": "Demostración de lo aprendido (RPA) y reflexión sobre el proceso personal.",
                "Fuentes": ["https://www.redalyc.org", "https://books.google.com", "https://www.scielo.org"]
            }
            
            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, limpiar(f"Planeación: {tema} - {nivel}"), 0, 1)
            
            for fase, cont in secuencia.items():
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 8, f"{fase}:", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, limpiar(cont))
                pdf.ln(2)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación PDF", pdf_bytes, f"Planeacion_{tema}.pdf")

    # --- SECCIÓN 2: DIARIO REFLEXIVO ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro de Escrito Diario")
        nom = st.text_input("Nombre del Alumno").upper()
        escrito = st.text_area("¿Qué descubrió hoy?")
        if st.button("Guardar Registro"):
            if nom not in st.session_state.db["alumnos"]: st.session_state.db["alumnos"][nom] = {"diario": [], "notas": {}}
            st.session_state.db["alumnos"][nom]["diario"].append(escrito)
            st.success("Guardado exitosamente.")

    # --- SECCIÓN 3: EVALUACIÓN Y CALIFICACIONES ---
    elif menu == "📊 Evaluación y Calificaciones":
        st.header("Evaluación Trimestral e Informe")
        busqueda = st.text_input("Nombre del Alumno para Evaluar").upper()
        
        if busqueda in st.session_state.db["alumnos"]:
            st.info(f"Historial: {len(st.session_state.db['alumnos'][busqueda]['diario'])} escritos.")
            
            nivel_edu = st.selectbox("Grado del Alumno", ["Preescolar", "Primaria", "Secundaria 1°", "Secundaria 2°", "Secundaria 3°"])
            
            c1, c2, c3, c4 = st.columns(4)
            if nivel_edu == "Preescolar":
                traye = c1.text_input("Trayectoria (ej. T205)")
                desc_traye = st.text_area("Descripción de Trayectoria")
            elif "Primaria" in nivel_edu:
                len_g = c1.number_input("Lenguajes", 5, 10)
                sab_p = c2.number_input("Saberes y P.C.", 5, 10)
                etica = c3.number_input("Etica, Nat. y Soc.", 5, 10)
                del_c = c4.number_input("De lo Hum. y Com.", 5, 10)
            else:
                esp = c1.number_input("Español", 5, 10)
                mat = c2.number_input("Matemáticas", 5, 10)
                cien = c3.number_input("Ciencias (Biol/Fis/Quim)", 5, 10)
                soc = c4.number_input("Sociedad", 5, 10)

            # Lectura y Escritura Manual
            st.divider()
            le_col1, le_col2 = st.columns(2)
            esc_val = le_col1.text_input("Escritura (ej. A7)")
            lec_val = le_col2.text_input("Lectura (ej. B7 o 7)")

            if st.button("Generar Informe Trimestral IA + PDF"):
                # La IA genera el resumen basado en el diario
                resumen_ia = " ".join(st.session_state.db["alumnos"][busqueda]["diario"][-3:])
                analisis_ia = f"El alumno demuestra avance en: {resumen_ia}. Se observa autorregulación y compromiso en las estaciones."
                
                pdf = PDF_ABCD()
                pdf.add_page()
                pdf.cell(0, 10, limpiar(f"INFORME TRIMESTRAL: {busqueda}"), 0, 1, 'C')
                
                # Datos de Calificación
                pdf.set_font("
