import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN DE PÁGINA Y CSS OPTIMIZADO
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

# Usamos animaciones ligeramente más suaves para no saturar la GPU
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
        background: rgba(255, 255, 255, 0.08); 
        border-radius: 12px; 
        padding: 12px; 
        margin-bottom: 10px; 
        border-left: 4px solid #00d4ff; 
        transition: transform 0.3s;
    }
    .comment-card:hover { transform: scale(1.02); }
    
    .profile-pic { 
        border-radius: 50%; 
        width: 45px; 
        height: 45px; 
        object-fit: cover; 
        border: 2px solid #00d4ff; 
    }
    
    .sos-btn { 
        background-color: #ff4b4b; 
        color: white; 
        border-radius: 8px; 
        padding: 10px; 
        text-align: center; 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE APOYO (OPTIMIZADAS)
@st.cache_data(show_spinner=False)
def process_image(image_file):
    """Optimiza la imagen para que no pese en la base de datos de sesión"""
    if image_file is not None:
        img = Image.open(image_file)
        img.thumbnail((150, 150)) # Reducimos tamaño para velocidad
        buffered = io.BytesIO()
        img.save(buffered, format="PNG", optimize=True)
        return base64.b64encode(buffered.getvalue()).decode()
    return None

class PDF_ABCD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'SISTEMA INTEGRAL ABCD - CONAFE', 0, 1, 'C')

# 3. BASE DE DATOS DE SESIÓN
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, 
        "user_data": {}, 
        "alumnos": {}, 
        "comentarios": [{"user": "Admin", "text": "¡Bienvenidos a la plataforma optimizada!", "pic": None}]
    }

# 4. SISTEMA DE ACCESO
if not st.session_state.db["auth"]:
    tab1, tab2 = st.tabs(["🔑 Ingresar", "📝 Registrarse"])
    
    with tab2:
        st.subheader("Crear Cuenta de Educador")
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
                    st.success("¡Cuenta lista! Ya puedes entrar.")
                else:
                    st.warning("El usuario y contraseña son obligatorios.")
                
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
                    st.error("Datos incorrectos")

else:
    # --- BARRA LATERAL ---
    current_u = st.session_state.db["user"]
    user_info = st.session_state.db["user_data"][current_u]
    
    st.sidebar.markdown(f"### Hola, {user_info['name']}")
    if user_info['pic']:
        st.sidebar.markdown(f'<img src="data:image/png;base64,{user_info["pic"]}" class="profile-pic">', unsafe_allow_html=True)
    
    st.sidebar.divider()
    menu = st.sidebar.radio("MENÚ PRINCIPAL", ["🏠 Muro de Inicio", "📅 Planeación ABCD", "✍️ Diario Reflexivo", "📊 Evaluación"])
    
    if st.sidebar.button("🆘 ASISTENCIA IA SOS"):
        st.sidebar.warning("⚠️ Modo SOS activado. ¿En qué error técnico puedo ayudarte?")

    # --- 1. MURO DE INICIO ---
    if menu == "🏠 Muro de Inicio":
        st.title("Comunidad Profe Educa")
        st.info("Suscripción Oro: Activa ✅")
        
        with st.expander("📣 Publicar en el Muro"):
            msg = st.text_input("¿Cómo va tu comunidad hoy?")
            if st.button("Enviar"):
                st.session_state.db["comentarios"].append({"user": user_info['name'], "text": msg, "pic": user_info['pic']})
                st.rerun()

        cols = st.columns(2)
        for i, c in enumerate(reversed(st.session_state.db["comentarios"])):
            with cols[i % 2]:
                pic_src = f'data:image/png;base64,{c["pic"]}' if c["pic"] else ""
                img_tag = f'<img src="{pic_src}" class="profile-pic">' if c["pic"] else "👤"
                st.markdown(f"""
                <div class="comment-card">
                    <div style="display:flex; align-items:center; gap:15px;">
                        {img_tag}
                        <div><strong>{c['user']}</strong><br>{c['text']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- 2. DIARIO REFLEXIVO ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro Diario")
        alumno = st.text_input("Nombre del Alumno").upper()
        texto = st.text_area("¿Qué se logró hoy?")
        if st.button("Guardar en Memoria"):
            if alumno:
                if alumno not in st.session_state.db["alumnos"]:
                    st.session_state.db["alumnos"][alumno] = {"diario": []}
                st.session_state.db["alumnos"][alumno]["diario"].append(texto)
                st.success("Guardado correctamente.")

    # --- 3. EVALUACIÓN Y PDF ---
    elif menu == "📊 Evaluación":
        st.header("Evaluación Trimestral")
        busqueda = st.text_input("Buscar Alumno").upper
