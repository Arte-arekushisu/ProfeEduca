import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

# Estilo visual optimizado
st.markdown("""
    <style>
    .stApp { background: #1a1c24; color: white; }
    .comment-card { 
        background: rgba(255, 255, 255, 0.08); 
        border-radius: 12px; 
        padding: 12px; 
        margin-bottom: 10px; 
        border-left: 4px solid #00d4ff;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .profile-pic { border-radius: 50%; width: 45px; height: 45px; object-fit: cover; border: 2px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES
def get_image_base64(image_file):
    if image_file is not None:
        try:
            img = Image.open(image_file)
            img.thumbnail((100, 100))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return base64.b64encode(buf.getvalue()).decode()
        except: return ""
    return ""

# 3. BASE DE DATOS
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, "user": None, "user_data": {}, 
        "alumnos": {}, "comentarios": []
    }

# 4. ACCESO
if not st.session_state.db["auth"]:
    t1, t2 = st.tabs(["Ingresar", "Registrarse"])
    with t2:
        with st.form("reg"):
            u_n = st.text_input("Usuario")
            p_n = st.text_input("Contraseña", type="password")
            nom = st.text_input("Nombre y Apellido")
            foto = st.file_uploader("Foto", type=['jpg','png'])
            if st.form_submit_button("CREAR CUENTA"):
                st.session_state.db["user_data"][u_n] = {
                    "pass": p_n, "name": nom, "pic": get_image_base64(foto)
                }
                st.success("¡Cuenta creada!")
    with t1:
        with st.form("log"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR"):
                if u in st.session_state.db["user_data"] and st.session_state.db["user_data"][u]["pass"] == p:
                    st.session_state.db["auth"] = True
                    st.session_state.db["user"] = u
                    st.rerun()
                else: st.error("Datos incorrectos")

# 5. PANEL
else:
    user = st.session_state.db["user"]
    info = st.session_state.db["user_data"][user]
    
    st.sidebar.title(f"EC: {info['name']}")
    menu = st.sidebar.radio("MENU", ["🏠 Inicio", "✍️ Diario", "📊 Evaluación", "🆘 SOS"])

    if menu == "🏠 Inicio":
        st.title("Muro de la Comunidad")
        with st.expander("Publicar mensaje"):
            msg = st.text_input("¿Qué compartes?")
            if st.button("Enviar"):
                st.session_state.db["comentarios"].append({
                    "n": info.get('name', 'Usuario'), 
                    "t": msg, 
                    "p": info.get('pic', '')
                })
                st.rerun()
        
        # RENDERIZADO SEGURO DE COMENTARIOS
        for c in reversed(st.session_state.db["comentarios"]):
            # Usamos .get() para evitar el KeyError si falta 'p', 'n' o 't'
            nombre = c.get('n', 'Anónimo')
            texto = c.get('t', '')
            foto_b64 = c.get('p', '')
            
            img_html = f'<img src="data:image/png;base64,{foto_b64}" class="profile-pic">' if foto_b64 else "👤"
            
            st.markdown(f"""
                <div class="comment-card">
                    <div>{img_html}</div>
                    <div><b>{nombre}</b><br>{texto}</div>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "✍️ Diario":
        st.header("Escrito Diario")
        nombre_al = st.text_input("Nombre del Alumno").upper()
        aprendizaje = st.text_area("Aprendizaje de hoy")
        if st.button("Guardar"):
            if nombre_al:
                if nombre_al not in st.session_state.db["alumnos"]:
                    st.session_state.db["alumnos"][nombre_al] = []
                st.session_state.db["alumnos"][nombre_al].append(aprendizaje)
                st.success("Guardado.")

    elif menu == "📊 Evaluación":
        st.header("Evaluación")
        busq = st.text_input("Alumno").upper()
        if busq in st.session_state.db["alumnos"]:
            st.write(f"Historial de {busq}:")
            for e in st.session_state.db["alumnos"][busq]:
                st.info(e)
        else: st.warning("Sin registros.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
        
