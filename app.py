import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN Y ESTILO VISUAL
st.set_page_config(page_title="Planeación Maestro ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-sidebar { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; height: 100%; }
    .comment-card { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #00d4ff; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS LOCAL (SIMULADA)
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user": "", "plan": "", 
        "alumnos": {}, # {nombre: [escritos]}
        "comentarios": [
            {"user": "Profe_Reyes", "text": "Excelente herramienta para el modelo ABCD."},
            {"user": "Educadora_M", "text": "Las evaluaciones por campo formativo son muy precisas."}
        ]
    }

# 3. INTERFAZ DE REGISTRO
if not st.session_state.db["auth"]:
    st.markdown("<h1>Planeación para el Maestro A B C D</h1>", unsafe_allow_html=True)
    col_reg, col_com = st.columns([2, 1])
    
    with col_reg:
        st.subheader("📝 Registro de Usuario")
        with st.form("registro"):
            u_email = st.text_input("Correo electrónico")
            u_name = st.text_input("Nombre de usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan = st.radio("Selecciona tu Plan Mensual", [
                "Plata ($200) - 2 servicios/mes",
                "Oro ($400) - 12 servicios/mes",
                "Platino ($600) - Ilimitado"
            ])
            if st.form_submit_button("Registrar y Entrar"):
                st.session_state.db.update({"auth": True, "user": u_name, "plan": plan})
                st.rerun()

    with col_com:
        st.markdown("<div class='comment-sidebar'>", unsafe_allow_html=True)
        st.subheader("💬 Opiniones")
        for c in st.session_state.db["comentarios"]:
            st.markdown(f"<div class='comment-card'><b>{c['user']}:</b><br>{c['text']}</div>", unsafe_allow_html=True)
        
        with st.form("add_comment", clear_on_submit=True):
            c_user = st.text_input("Tu nombre")
            c_text = st.text_area("Comentario")
            if st.form_submit_button("Publicar"):
                st.session_state.db["comentarios"].append({"user": c_user, "text": c_text})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 4. PANEL DE CONTROL (POST-LOGIN)
else:
    st.sidebar.title("MAESTRO ABCD")
    menu = st.sidebar.radio("MENÚ", ["📅 Planeación", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 SOS Corrección"])

    # --- SECCIÓN PLANEACIÓN ---
    if menu == "📅 Planeación":
        st.header("Generar Planeación Semanal")
        with st.expander("📍 Datos de Identificación (Manual)", expanded=True):
            c1, c2, c3 = st.columns(3)
            comunidad = c1.text_input("Comunidad")
            fecha = c2.date_input("Fecha de creación")
            eca_acompa = c3.text_input("Nombre del ECA (Acompañamiento)")
            lote = c1.text_input("Lote")
            casa = c2.text_input("Casa")
            educador = c3.text_input("Educador Comunitario")

        with st.expander("🧠 Contenido Pedagógico"):
            tema = st.text_input("Tema de Interés")
            estacion = st.text_input("Estación Permanente")
            c4, c5 = st.columns(2)
            m1 = c4.text_input("Materia Post-Receso 1")
            m2 = c5.text_input("Materia Post-Receso 2")

        if st.button("Generar Planeación PDF"):
            st.success("IA Procesando: Bienvenida, Regalo de lectura, Pase de lista, Estaciones y Rincón.")
            # Aquí se integra la lógica de FPDF para generar el documento inalterable
            st.download_button("📥 Descargar PDF", "CONTENIDO_SIMULADO", "Planeacion_ABCD.pdf")

    # --- SECCIÓN DIARIO ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Escrito Diario del Alumno")
        nombre_al = st.text_input("Nombre del Alumno").upper()
        reflexion = st.text_area("¿Qué aprendió o realizó hoy?")
        if st.button("Guardar Escrito"):
            if nombre_al not in st.session_state.db["alumnos"]:
                st.session_state.db["alumnos"][nombre_al] = []
            st.session_state.db["alumnos"][nombre_al].append(reflexion)
            st.success(f"Escrito guardado para {nombre_al}.")

    # --- SECCIÓN EVALUACIÓN ---
    elif menu == "📊 Evaluación Trimestral":
        st.header("Generador de Evaluación Trimestral")
        buscar = st.text_input("Buscar Alumno por Nombre").upper()
        
        if buscar in st.session_state.db["alumnos"]:
            st.info(f"Se encontraron {len(st.session_state.db['alumnos'][buscar])} escritos diarios.")
            nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria"])
            
            if nivel == "Preescolar":
                trayectoria = st.text_area("Agregar Trayectorias Manualmente")
            else:
                st.subheader("Evaluación por Campos Formativos")
                col_f1, col_f2 = st.columns(2)
                col_f1.number_input("Lenguaje", 5, 10)
                col_f2.number_input("Pensamiento Científico", 5, 10)
                col_f1.number_input("Ética", 5, 10)
                col_f2.number_input("Naturaleza y Sociedades", 5, 10)
                
                st.write("---")
                st.selectbox("Nivel de Lectura/Escritura", ["Requiere apoyo", "En desarrollo", "Nivel esperado"])
                st.text_area("Compromisos del Alumno")

            if st.button("Generar Reporte Trimestral PDF"):
                st.write("IA redactando evaluación basada en escritos diarios...")
        else:
            st.warning("Alumno no encontrado en la base de datos.")

    # --- SECCIÓN SOS ---
    elif menu == "🆘 SOS Corrección":
        st.header("Botón SOS: Corrección de Texto")
        texto_error = st.text_area("Pega aquí el texto con errores o dudas:")
        if st.button("Corregir y Sugerir Cambios"):
            st.info("La IA está analizando y optimizando el texto...")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
