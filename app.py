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
    def __init__(self, logo_izq=None, logo_der=None):
        super().__init__()
        self.logo_izq = logo_izq
        self.logo_der = logo_der

    def header(self):
        if self.logo_izq:
            self.image(self.logo_izq, 10, 8, 25)
        if self.logo_der:
            self.image(self.logo_der, 175, 8, 25)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'TEXTO REFLEXIVO TRIMESTRAL - ABCD', 0, 1, 'C')
        self.ln(5)

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
    menu = st.sidebar.radio("MENÚ", ["🏠 Inicio", "✍️ Diario Reflexivo", "📊 Evaluación"])
    
    # --- 1. INICIO ---
    if menu == "🏠 Inicio":
        st.title("Panel Profe Educa")
        st.info("Suscripción Oro: Activa ✅ | Período: 2026")
        # [Mantenemos tu código original de comentarios aquí...]

    # --- 2. DIARIO REFLEXIVO (Mejorado con Temas de Interés) ---
    elif menu == "✍️ Diario Reflexivo":
        st.header("Registro de Avances Diarios")
        col_diario1, col_diario2 = st.columns(2)
        
        with col_diario1:
            alumno = st.text_input("Nombre del Alumno").upper()
        with col_diario2:
            temas_interes = st.text_input("Temas de interés del niño hoy")
            
        texto = st.text_area("Escrito reflexivo de hoy (Avances en campos formativos)")
        
        if st.button("Guardar Registro"):
            if alumno:
                if alumno not in st.session_state.db["alumnos"]:
                    st.session_state.db["alumnos"][alumno] = {"diario": [], "temas": []}
                st.session_state.db["alumnos"][alumno]["diario"].append(texto)
                st.session_state.db["alumnos"][alumno]["temas"].append(temas_interes)
                st.success(f"Registro y temas guardados para {alumno}")

    # --- 3. EVALUACIÓN (Formato Profesional Solicitado) ---
    elif menu == "📊 Evaluación":
        st.header("Evaluación Trimestral Estructurada")
        
        with st.expander("🖼️ Configuración de Imagenes (Logos PDF)", expanded=True):
            col_l1, col_l2 = st.columns
