import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ESTELAR
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(-45deg, #050505, #1a1c24, #00d4ff, #050505); 
        background-size: 400% 400%; 
        animation: gradient 15s ease infinite; 
        color: white; 
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    
    .comment-card { 
        background: rgba(255, 255, 255, 0.1); 
        border-radius: 15px; 
        padding: 15px; 
        margin: 10px; 
        border-left: 5px solid #00d4ff; 
        animation: fadeIn 1s;
    }
    .profile-pic { 
        border-radius: 50%; 
        width: 50px; 
        height: 50px; 
        object-fit: cover; 
        border: 2px solid #00d4ff; 
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES TÉCNICAS
@st.cache_data(show_spinner=False)
def process_image(image_file):
    if image_file is not None:
        try:
            img = Image.open(image_file)
            img.thumbnail((150, 150))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        except: return ""
    return ""

def limpiar(t):
    r = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k, v in r.items(): t = str(t).replace(k, v)
    return t

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'SISTEMA INTEGRAL ABCD - CONAFE', 0, 1, 'C')

# 3. BASE DE DATOS DE SESIÓN BLINDADA
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, 
        "user_data": {}, 
        "alumnos": {}, 
        "comentarios": [{"user": "Admin", "text": "¡Bienvenidos a la era ABCD!", "pic": ""}]
    }

# 4. ACCESO AL SISTEMA
if not st.session_state.db["auth"]:
    t1, t2 = st.tabs(["🔑 Ingresar", "📝 Registrarse"])
    
    with t2:
        st.subheader("Registro de Educador Comunitario")
        with st.form("reg_form"):
            new_u = st.text_input("Usuario")
            new_p = st.text_input("Contraseña", type="password")
            nom = st.text_input("Nombre(s)")
            ape = st.text_input("Apellidos")
            foto = st.file_uploader("Foto de Perfil", type=['jpg', 'png'])
            if st.form_submit_button("REGISTRARSE"):
                if new_u and new_p:
                    pic_b64 = process_image(foto)
                    st.session_state.db["user_data"][new_u] = {"pass": new_p, "name": f"{nom} {ape}", "pic": pic_b64}
                    st.success("¡Cuenta creada! Ya puedes ingresar.")
                
    with t1:
        st.subheader("Inicio de Sesión")
        with st.form("login_form"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR"):
                if u in st.session_state.db["user_data"] and st.session_state.db["user_data"][u]["pass"] == p:
                    st.session_state.db["auth"] = True
                    st.session_state.db["user"] = u
                    st.rerun()
                else: st.error("Usuario o contraseña incorrectos")

else:
    # --- BARRA LATERAL ---
    user_info = st.session_state.db["user_data"][st.session_state.db["user"]]
    st.sidebar.markdown(f"### Hola, {user_info['name']}")
    if user_info.get('pic'):
        st.sidebar.markdown(f'<img src="data:image/png;base64,{user_info["pic"]}" class="profile-pic">', unsafe_allow_html=True)
    
    st.sidebar.divider()
    menu = st.sidebar.radio("MENÚ", ["🏠 Inicio", "📅 Planeación ABCD", "✍️ Diario Reflexivo", "📊 Evaluación"])
    
    if st.sidebar.button("🆘 ASISTENCIA SOS 24/7"):
        st.sidebar.warning("⚠️ SOS: ¿En qué error técnico puedo ayudarte hoy?")

    # --- 1. INICIO Y COMENTARIOS (COLLAGE) ---
    if menu == "🏠 Inicio":
        st.title("Panel Profe Educa")
        st.info("Suscripción Oro: Activa ✅ | Período: 2026")
        
        with st.expander("💬 Compartir en el Muro"):
            msg = st.text_input("¿Qué quieres decir a la comunidad?")
            if st.button("Publicar"):
                st.session_state.db["comentarios"].append({"user": user_info['name'], "text": msg, "pic": user_info['pic']})
                st.rerun()

        cols = st.columns(2)
        for i, c in enumerate(reversed(st.session_state.db["comentarios"])):
            with cols[i % 2]:
                pic_data = c.get('pic', '')
                img_html = f'<img src="data:image/png;base64,{pic_data}" class="profile-pic">' if pic_data else "👤"
                st.markdown(f"""
                <div class="comment-card">
                    <div style="display:flex; align-items:center; gap:15px;">
                        {img_html}
                        <div><strong>{c.get('user', 'Anónimo')}</strong><br>{c.get('text', '')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- 2. DIARIO REFLEXIVO ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro de Avances Diarios")
        alumno = st.text_input("Nombre del Alumno").upper()
        texto = st.text_area("Escrito reflexivo de hoy")
        if st.button("Guardar Registro"):
            if alumno:
                if alumno not in st.session_state.db["alumnos"]:
                    st.session_state.db["alumnos"][alumno] = {"diario": []}
                st.session_state.db["alumnos"][alumno]["diario"].append(texto)
                st.success(f"Registro guardado para {alumno}")

    # --- 3. EVALUACIÓN Y CALIFICACIONES (COMPLETO) ---
    elif menu == "📊 Evaluación":
        st.header("Evaluación Trimestral")
        busqueda = st.text_input("Buscar Alumno").upper()
        
        if busqueda in st.session_state.db["alumnos"]:
            nivel = st.selectbox("Grado Escolar", ["Preescolar", "Primaria", "Secundaria 1°", "Secundaria 2°", "Secundaria 3°", "Multigrado"])
            
            c1, c2 = st.columns(2)
            califs = {}
            
            if "Preescolar" in nivel:
                califs["Trayectoria"] = c1.text_input("Trayectoria (ej. T205)")
                califs["Observación"] = st.text_area("Ritmo de aprendizaje")
            elif "Primaria" in nivel or "Multigrado" in nivel:
                califs["Lenguajes"] = c1.number_input("Lenguajes", 5, 10)
                califs["Saberes"] = c2.number_input("Saberes y P.C.", 5, 10)
                califs["Etica"] = c1.number_input("Etica, Nat. y Soc.", 5, 10)
                califs["Humano"] = c2.number_input("De lo Hum. y Com.", 5, 10)
            elif "Secundaria" in nivel:
                califs["Español"] = c1.number_input("Español", 5, 10)
                califs["Matemáticas"] = c2.number_input("Matemáticas", 5, 10)
                materia_c = "Biología" if "1°" in nivel else "Física" if "2°" in nivel else "Química"
                califs[materia_c] = c1.number_input(materia_c, 5, 10)

            st.divider()
            l_esc = st.text_input("Nivel Escritura (ej. A7)")
            l_lec = st.text_input("Nivel Lectura")

            if st.button("Generar PDF Final"):
                pdf = PDF_ABCD()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, limpiar(f"REPORTE: {busqueda}"), 0, 1, 'C')
                
                pdf.set_font("Arial", '', 12)
                for m, n in califs.items():
                    pdf.cell(0, 10, limpiar(f"{m}: {n}"), 0, 1)
                
                pdf.cell(0, 10, limpiar(f"Lectoescritura: {l_esc} / {l_lec}"), 0, 1)
                
                # Resumen del diario
                diario_full = " ".join(st.session_state.db["alumnos"][busqueda]["diario"])
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "EVOLUCION ABCD:", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, limpiar(diario_full[:500]))
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button("📥 Descargar Reporte", pdf_bytes, f"Reporte_{busqueda}.pdf")
        else:
            st.warning("El alumno no tiene registros previos en el Diario.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
