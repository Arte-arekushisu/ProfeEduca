import streamlit as st
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN Y ESTILO VISUAL DINÁMICO
st.set_page_config(page_title="Planeación Maestro ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .comment-sidebar { background-color: #003366; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; height: 800px; overflow-y: auto; }
    .comment-card { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #00d4ff; font-size: 0.9em; }
    h1 { color: #00d4ff !important; text-align: center; font-family: 'Arial Black'; text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE LIMPIEZA PARA EVITAR ERRORES EN PDF
def limpiar_texto(texto):
    remplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "Ñ": "N", "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}
    for original, nuevo in remplazos.items():
        texto = str(texto).replace(original, nuevo)
    return texto

class PDF(FPDF):
    def header_oficial(self, d):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "PLANEACION PARA EL MAESTRO A B C D", 0, 1, 'C')
        self.set_font('Arial', '', 9)
        info = f"Comunidad: {d['comunidad']} | Lote: {d['lote']} | Casa: {d['casa']} | ECA: {d['eca']}"
        self.cell(0, 5, limpiar_texto(info), 0, 1, 'C')
        self.ln(5)

# 3. BASE DE DATOS LOCAL
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user": "", "plan": "", 
        "alumnos": {}, 
        "comentarios": [
            {"user": "Profe_Juan", "text": "Excelente para el modelo ABCD."},
            {"user": "Educadora_Luz", "text": "Las evaluaciones trimestrales son muy rapidas."}
        ]
    }

# 4. ESTRUCTURA DE LA PÁGINA (COLUMNAS)
if not st.session_state.db["auth"]:
    st.markdown("<h1>Planeación para el Maestro A B C D</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>\"Inspirando el saber, transformando la comunidad: El eco de tu enseñanza es el futuro de todos.\"</p>", unsafe_allow_html=True)
    
    col_reg, col_com = st.columns([2, 1])
    
    with col_reg:
        st.subheader("📝 Registro y Suscripción")
        with st.form("registro"):
            u_email = st.text_input("Correo electrónico")
            u_name = st.text_input("Nombre de usuario")
            u_pass = st.text_input("Contraseña", type="password")
            plan = st.radio("Selecciona tu Plan Mensual", [
                "Plata ($200) - 2 servicios/mes",
                "Oro ($400) - 12 servicios/mes",
                "Platino ($600) - Ilimitado"
            ])
            if st.form_submit_button("REGISTRAR Y ACTIVAR"):
                st.session_state.db.update({"auth": True, "user": u_name, "plan": plan})
                st.rerun()
else:
    # PANEL DE CONTROL POST-LOGIN
    st.sidebar.title("MAESTRO ABCD")
    menu = st.sidebar.radio("MENÚ", ["📅 Planeación", "✍️ Diario Reflexivo", "📊 Evaluación Trimestral", "🆘 SOS Corrección"])

    if menu == "📅 Planeación":
        st.header("Generar Planeación ABCD")
        # Campos Manuales
        c1, c2, c3 = st.columns(3)
        comu = c1.text_input("Comunidad")
        lote = c2.text_input("Lote")
        casa = c3.text_input("Casa")
        eca = c1.text_input("Nombre del ECA (Acompañamiento)")
        educador = c2.text_input("Educador Comunitario")
        
        st.subheader("Contenido de la Clase")
        tema = st.text_input("Tema de Interés")
        estacion = st.text_input("Estación Permanente")
        m1 = st.text_input("Materia Post-Receso 1")
        m2 = st.text_input("Materia Post-Receso 2")

        if st.button("Generar Planeación PDF"):
            datos_pdf = {"comunidad": comu, "lote": lote, "casa": casa, "eca": eca}
            pdf = PDF()
            pdf.add_page()
            pdf.header_oficial(datos_pdf)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 10, limpiar_texto(f"Tema: {tema} | Estacion: {estacion}"), 1, 1)
            pdf.set_font("Arial", '', 10)
            # Contenido simulado de la IA
            contenido = [["Bienvenida", "Dinámica de integracion", "15 min"], 
                         ["Regalo Lectura", "Cuento sugerido por IA", "20 min"],
                         ["Post-Receso", f"{m1} y {m2}", "120 min"]]
            for f in contenido:
                pdf.cell(40, 10, limpiar_texto(f[0]), 1)
                pdf.cell(100, 10, limpiar_texto(f[1]), 1)
                pdf.cell(40, 10, limpiar_texto(f[2]), 1, 1)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Descargar PDF Sin Errores", pdf_bytes, "Planeacion.pdf", "application/pdf")

    elif menu == "✍️ Diario Reflexivo":
        st.header("Escrito Diario")
        al = st.text_input("Nombre del Alumno").upper()
        txt = st.text_area("Descripción de actividades")
        if st.button("Guardar"):
            if al not in st.session_state.db["alumnos"]: st.session_state.db["alumnos"][al] = []
            st.session_state.db["alumnos"][al].append(txt)
            st.success("Guardado.")

    elif menu == "📊 Evaluación Trimestral":
        st.header("Evaluación Trimestral")
        buscar = st.text_input("Nombre del Alumno").upper()
        if buscar in st.session_state.db["alumnos"]:
            st.info(f"Escritos encontrados: {len(st.session_state.db['alumnos'][buscar])}")
            nivel = st.radio("Nivel", ["Preescolar", "Primaria"])
            if nivel == "Primaria":
                st.number_input("Lenguaje", 5, 10)
                st.number_input("Pensamiento Científico", 5, 10)
                st.number_input("Ética", 5, 10)
                st.number_input("Naturaleza y Sociedades", 5, 10)
            st.button("Generar Evaluación PDF")
        else:
            st.warning("Alumno no registrado en el Diario.")

    elif menu == "🆘 SOS Corrección":
        st.header("SOS: Corrección IA")
        t_sos = st.text_area("Pega tu texto aquí")
        if st.button("Corregir"):
            st.write("Sugerencia IA: " + limpiar_texto(t_sos))

# 5. BARRA LATERAL DE COMENTARIOS (COLUMNA DERECHA AZUL)
if not st.session_state.db["auth"]: # Solo mostrar en la pantalla de inicio
    with col_com:
        st.markdown("<div class='comment-sidebar'>", unsafe_allow_html=True)
        st.subheader("💬 Comunidad Maestro ABCD")
        for c in st.session_state.db["comentarios"]:
            st.markdown(f"<div class='comment-card'><b>{c['user']}:</b><br>{c['text']}</div>", unsafe_allow_html=True)
        
        with st.form("nuevo_c", clear_on_submit=True):
            n = st.text_input("Nombre")
            t = st.text_area("Comentario")
            if st.form_submit_button("Publicar"):
                st.session_state.db["comentarios"].append({"user": n, "text": t})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
