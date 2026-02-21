import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN Y ESTILO AVANZADO
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); background-size: 400% 400%; animation: gradient 12s ease infinite; color: white; }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    
    /* Estilo de Comentarios */
    .comment-card { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 15px; margin: 10px; border-left: 5px solid #00d4ff; animation: fadeIn 1s; }
    .profile-pic { border-radius: 50%; width: 50px; height: 50px; object-fit: cover; border: 2px solid #00d4ff; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    /* Botón SOS */
    .sos-btn { background-color: #ff4b4b; color: white; border-radius: 10px; padding: 10px; text-align: center; font-weight: bold; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE APOYO
def get_image_base64(image_file):
    if image_file is not None:
        img = Image.open(image_file)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'SISTEMA INTEGRAL ABCD - CONAFE', 0, 1, 'C')

# 3. BASE DE DATOS LOCAL (SIMULADA EN SESIÓN)
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, 
        "user_data": {}, 
        "alumnos": {}, 
        "comentarios": [
            {"user": "Admin", "text": "¡Bienvenidos a la nueva era ABCD!", "pic": None}
        ]
    }

# 4. SISTEMA DE ACCESO Y REGISTRO
if not st.session_state.db["auth"]:
    tab1, tab2 = st.tabs(["Ingresar", "Registrarse"])
    
    with tab2:
        st.subheader("Crear Cuenta de Educador")
        with st.form("reg_form"):
            new_u = st.text_input("Usuario")
            new_p = st.text_input("Contraseña", type="password")
            nom = st.text_input("Nombre(s)")
            ape = st.text_input("Apellidos")
            foto = st.file_uploader("Foto de Perfil", type=['jpg', 'png'])
            if st.form_submit_button("REGISTRARSE"):
                pic_b64 = get_image_base64(foto)
                st.session_state.db["user_data"][new_u] = {"pass": new_p, "name": f"{nom} {ape}", "pic": pic_b64}
                st.success("Cuenta creada. Ahora puedes ingresar.")
                
    with tab1:
        st.subheader("Inicio de Sesión")
        with st.form("login_form"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR"):
                if u in st.session_state.db["user_data"] and st.session_state.db["user_data"][u]["pass"] == p:
                    st.session_state.db["auth"] = True
                    st.session_state.db["user"] = u
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

else:
    # --- SIDEBAR Y SOS ---
    user_info = st.session_state.db["user_data"][st.session_state.db["user"]]
    st.sidebar.markdown(f"### Bienvido, {user_info['name']}")
    if user_info['pic']:
        st.sidebar.markdown(f'<img src="data:image/png;base64,{user_info["pic"]}" class="profile-pic">', unsafe_allow_html=True)
    
    st.sidebar.divider()
    menu = st.sidebar.radio("MENÚ", ["🏠 Inicio", "📅 Planeación ABCD", "✍️ Diario Reflexivo", "📊 Evaluación"])
    
    if st.sidebar.button("🆘 ASISTENCIA IA 24/7 (SOS)"):
        st.sidebar.info("Conectando con soporte técnico... Un asesor IA te atenderá en breve.")

    # --- SECCIÓN INICIO Y COMENTARIOS ---
    if menu == "🏠 Inicio":
        st.title("Panel de Control Profe Educa")
        st.markdown("""
        > **Tu suscripción activa:** Prueba 3 días (Gratis)  
        > *Incluye: Planeación semanal, diario reflexivo y evaluaciones trimestrales automáticas.*
        """)
        
        st.subheader("💬 Muro de la Comunidad (Collage)")
        
        # Publicar comentario
        with st.expander("Escribir un comentario"):
            new_comm = st.text_input("¿Qué quieres compartir hoy?")
            if st.button("Publicar"):
                st.session_state.db["comentarios"].append({
                    "user": user_info['name'], 
                    "text": new_comm, 
                    "pic": user_info['pic']
                })
                st.rerun()

        # Mostrar collage animado
        cols = st.columns(2)
        for i, c in enumerate(reversed(st.session_state.db["comentarios"])):
            with cols[i % 2]:
                pic_html = f'<img src="data:image/png;base64,{c["pic"]}" class="profile-pic">' if c["pic"] else "👤"
                st.markdown(f"""
                <div class="comment-card">
                    <table><tr>
                        <td>{pic_html}</td>
                        <td style="padding-left:15px;"><strong>{c['user']}</strong><br>{c['text']}</td>
                    </tr></table>
                </div>
                """, unsafe_allow_html=True)

    # --- SECCIÓN DIARIO (CORRECCIÓN DE GUARDADO) ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro de Avances Diarios")
        nom_a = st.text_input("Nombre Completo del Alumno").upper()
        texto_a = st.text_area("Escrito Reflexivo del día")
        if st.button("Guardar Registro"):
            if nom_a not in st.session_state.db["alumnos"]:
                st.session_state.db["alumnos"][nom_a] = {"diario": []}
            st.session_state.db["alumnos"][nom_a]["diario"].append(texto_a)
            st.success(f"Registro guardado exitosamente para {nom_a}")

    # --- SECCIÓN EVALUACIÓN (GRADOS Y MATERIAS) ---
    elif menu == "📊 Evaluación":
        st.header("Calificaciones y Reporte PDF")
        busq = st.text_input("Buscar Alumno").upper()
        
        if busq in st.session_state.db["alumnos"]:
            nivel = st.selectbox("Grado Escolar", ["Preescolar", "Primaria 1°", "Primaria 2°", "Primaria 3°", "Primaria 4°", "Primaria 5°", "Primaria 6°", "Secundaria 1°", "Secundaria 2°", "Secundaria 3°", "Multigrado"])
            
            # Lógica de materias por grado
            c1, c2 = st.columns(2)
            califs = {}
            
            if "Preescolar" in nivel:
                califs["Trayectoria"] = c1.text_input("Trayectoria (ej. T205)")
                califs["Observación"] = st.text_area("Desempeño observado")
            elif "Primaria" in nivel or "Multigrado" in nivel:
                califs["Lenguajes"] = c1.number_input("Lenguajes", 5, 10)
                califs["Saberes"] = c2.number_input("Saberes y P.C.", 5, 10)
                califs["Etica"] = c1.number_input("Etica, Nat. y Soc.", 5, 10)
                califs["Humano"] = c2.number_input("De lo Hum. y Com.", 5, 10)
            elif "Secundaria" in nivel:
                califs["Español"] = c1.number_input("Español", 5, 10)
                califs["Matemáticas"] = c2.number_input("Matemáticas", 5, 10)
                ciencia = "Biología" if "1°" in nivel else "Física" if "2°" in nivel else "Química"
                califs[ciencia] = c1.number_input(ciencia, 5, 10)

            st.divider()
            l_esc = st.text_input("Nivel Escritura (ej. A7)")
            l_lec = st.text_input("Nivel Lectura (ej. 7)")

            if st.button("Generar Informe PDF"):
                # Aquí iría la generación del PDF con los datos recolectados
                st.balloons()
                st.info("Generando informe reflexivo basado en el historial del diario...")
        else:
            st.warning("El alumno debe tener al menos un registro en el Diario Reflexivo.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
