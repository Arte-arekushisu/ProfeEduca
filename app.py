import streamlit as st
from fpdf import FPDF

# 1. CONFIGURACIÓN Y ESTILO ESTELAR
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 12s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .stTextInput, .stTextArea, .stSelectbox, .stNumberInput { background-color: rgba(255,255,255,0.1) !important; color: white !important; border: 1px solid #00d4ff !important; }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. UTILIDADES TÉCNICAS
def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'SISTEMA INTEGRAL ABCD - CONAFE', 0, 1, 'C')
        self.ln(5)

# 3. BASE DE DATOS EN SESIÓN
if 'db' not in st.session_state:
    st.session_state.db = {"auth": False, "user": "", "alumnos": {}}

# 4. ACCESO AL SISTEMA
if not st.session_state.db["auth"]:
    st.markdown("<h1>Profe Educa: Modelo ABCD</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        u = st.text_input("Nombre del EC (Educador Comunitario)")
        if st.form_submit_button("INGRESAR AL PANEL"):
            st.session_state.db.update({"auth": True, "user": u})
            st.rerun()
else:
    st.sidebar.title(f"EC: {st.session_state.db['user']}")
    menu = st.sidebar.radio("MENÚ", ["📅 Planeación IA (Fases)", "✍️ Diario Reflexivo", "📊 Evaluación y Calificaciones"])

    # --- SECCIÓN 1: PLANEACIÓN ABCD CON FASES ---
    if menu == "📅 Planeación IA (Fases)":
        st.header("Generador de Secuencia Didáctica (Fases ABCD)")
        c1, c2 = st.columns(2)
        nivel = c1.selectbox("Nivel", ["Preescolar", "Primaria Multigrado", "Secundaria"])
        tema = c2.text_input("Tema de Interés (Ej. Fotosíntesis)")
        
        if st.button("Generar Contenido Pedagógico"):
            # Lógica de contenido estilo CONAFE
            fases = {
                "Fase 1: Inicio (Activación)": f"Charla introductoria sobre {tema}. Planteamiento de un desafío real para la comunidad.",
                "Fase 2: Desarrollo (Investigación)": f"Indagación en la estación de aprendizaje. Uso de materiales de la región para resolver dudas sobre {tema}.",
                "Fase 3: Cierre (RPA)": f"Presentación pública de lo aprendido (RPA) y registro en el cuaderno de campo.",
                "Fuentes Académicas": "1. Redalyc.org | 2. Scielo.org | 3. Libros de Texto CONALITEG"
            }
            
            pdf = PDF_ABCD()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, limpiar(f"Planeacion Semanal: {tema}"), 0, 1)
            
            for f, contenido in fases.items():
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 8, f, 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, limpiar(contenido))
                pdf.ln(3)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar Planeación", pdf_bytes, f"Planeacion_{tema}.pdf")

    # --- SECCIÓN 2: DIARIO REFLEXIVO ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro de Avances Diarios")
        nom = st.text_input("Nombre del Alumno").upper()
        texto = st.text_area("Descripción de lo aprendido hoy (Escrito Reflexivo)")
        if st.button("Guardar en Historial"):
            if nom not in st.session_state.db["alumnos"]:
                st.session_state.db["alumnos"][nom] = {"diario": []}
            st.session_state.db["alumnos"][nom]["diario"].append(texto)
            st.success(f"Registro guardado para {nom}.")

    # --- SECCIÓN 3: EVALUACIÓN Y CALIFICACIONES ---
    elif menu == "📊 Evaluación y Calificaciones":
        st.header("Informe Trimestral y Calificaciones")
        busqueda = st.text_input("Buscar Alumno por Nombre").upper()
        
        if busqueda in st.session_state.db["alumnos"]:
            st.info(f"Escritos encontrados: {len(st.session_state.db['alumnos'][busqueda]['diario'])}")
            
            grado = st.selectbox("Selecciona Nivel para Calificar", ["Preescolar", "Primaria", "Secundaria 1", "Secundaria 2", "Secundaria 3"])
            
            calificaciones = {}
            st.subheader("Captura Manual de Calificaciones")
            
            if grado == "Preescolar":
                calificaciones["Trayectoria"] = st.text_input("Trayectoria (ej. T205)")
                calificaciones["Logro"] = st.text_area("Descripción del logro (autorregulación, ritmo, etc.)")
            
            elif grado == "Primaria":
                c1, c2 = st.columns(2)
                calificaciones["Lenguajes"] = c1.number_input("Lenguajes", 5, 10)
                calificaciones["Saberes"] = c2.number_input("Saberes y P. Científico", 5, 10)
                calificaciones["Etica"] = c1.number_input("Etica, Nat. y Soc.", 5, 10)
                calificaciones["Humano"] = c2.number_input("De lo Hum. y Com.", 5, 10)
            
            else: # Secundaria
                c1, c2 = st.columns(2)
                calificaciones["Español"] = c1.number_input("Español", 5, 10)
                calificaciones["Matematicas"] = c2.number_input("Matemáticas", 5, 10)
                # Materia de ciencia según grado
                ciencias = {"Secundaria 1": "Biología", "Secundaria 2": "Física", "Secundaria 3": "Química"}
                label_c = ciencias.get(grado)
                calificaciones[label_c] = c1.number_input(label_c, 5, 10)
                calificaciones["Sociedad"] = c2.number_input("Historia/Geografía", 5, 10)

            st.divider()
            st.subheader("Niveles de Lectoescritura")
            col_l, col_e = st.columns(2)
            val_esc = col_l.text_input("Escritura (ej. A7)")
            val_lec = col_e.text_input("Lectura (ej. B7 o 7)")

            if st.button("Generar Informe Trimestral PDF"):
                # Análisis de la IA basado en el diario
                todos_escritos = " ".join(st.session_state.db["alumnos"][busqueda]["diario"])
                informe_ia = f"De acuerdo a los registros, el alumno muestra: {todos_escritos[:200]}... Se observa una evolución positiva en su proceso ABCD."
                
                pdf = PDF_ABCD()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, limpiar(f"EVALUACION TRIMESTRAL: {busqueda}"), 0, 1, 'C')
                
                # Sección de Calificaciones en PDF
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "CALIFICACIONES Y LOGROS:", 0, 1)
                pdf.set_font("Arial", '', 10)
                
                for materia, nota in calificaciones.items():
                    pdf.cell(0, 7, limpiar(f"{materia}: {nota}"), 0, 1)
                
                pdf.ln(3)
                pdf.cell(0, 7, limpiar(f"Nivel Escritura: {val_esc} | Nivel Lectura: {val_lec}"), 0, 1)
                
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "INFORME REFLEXIVO (IA):", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, limpiar(informe_ia))
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button("📥 Descargar Informe Final", pdf_bytes, f"Informe_{busqueda}.pdf")
        else:
            st.warning("Alumno no encontrado. Asegúrate de registrarlo primero en el Diario.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
