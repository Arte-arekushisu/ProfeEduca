import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import io

# 1. CONFIGURACIÓN Y ESTILO (Mantenemos tu estética Pro)
st.set_page_config(page_title="Profe Educa ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #1a1c24; color: white; }
    .comment-card { background: rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #00d4ff; }
    .profile-pic { border-radius: 50%; width: 45px; height: 45px; object-fit: cover; border: 2px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE APOYO
def get_image_base64(image_file):
    if image_file is not None:
        try:
            img = Image.open(image_file)
            img.thumbnail((150, 150))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        except: return None
    return None

# 3. INICIALIZACIÓN BLINDADA (Aquí evitamos el TypeError)
if 'db' not in st.session_state:
    st.session_state.db = {
        "auth": False, 
        "user": None,
        "user_data": {}, 
        "alumnos": {}, # DEBE SER DICCIONARIO
        "comentarios": []
    }

# 4. LÓGICA DE ACCESO
if not st.session_state.db["auth"]:
    t1, t2 = st.tabs(["Ingresar", "Registrarse"])
    with t2:
        with st.form("reg"):
            u_n = st.text_input("Usuario")
            p_n = st.text_input("Contraseña", type="password")
            nom = st.text_input("Nombre y Apellido")
            foto = st.file_uploader("Foto", type=['jpg','png'])
            if st.form_submit_button("CREAR CUENTA"):
                st.session_state.db["user_data"][u_n] = {"pass": p_n, "name": nom, "pic": get_image_base64(foto)}
                st.success("¡Listo! Ya puedes ingresar.")
    with t1:
        with st.form("log"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("ENTRAR"):
                if u in st.session_state.db["user_data"] and st.session_state.db["user_data"][u]["pass"] == p:
                    st.session_state.db["auth"] = True
                    st.session_state.db["user"] = u
                    st.rerun()
                else: st.error("Error en datos")

# 5. PANEL PRINCIPAL
else:
    user = st.session_state.db["user"]
    info = st.session_state.db["user_data"][user]
    
    st.sidebar.image(f"data:image/png;base64,{info['pic']}" if info['pic'] else "https://via.placeholder.com/50", width=100)
    st.sidebar.title(f"EC: {info['name']}")
    menu = st.sidebar.radio("IR A:", ["🏠 Inicio", "✍️ Diario", "📊 Evaluación", "🆘 SOS"])

    if menu == "🏠 Inicio":
        st.title("Muro de la Comunidad")
        with st.expander("Publicar mensaje"):
            msg = st.text_input("¿Qué compartes?")
            if st.button("Enviar"):
                st.session_state.db["comentarios"].append({"n": info['name'], "t": msg, "p": info['pic']})
                st.rerun()
        
        for c in reversed(st.session_state.db["comentarios"]):
            st.markdown(f"""<div class="comment-card">
                <img src="data:image/png;base64,{c['p']}" class="profile-pic" style="float:left; margin-right:10px;">
                <b>{c['n']}</b><br>{c['t']}</div>""", unsafe_allow_html=True)

    elif menu == "✍️ Diario":
        st.header("Escrito Diario")
        nombre = st.text_input("Nombre del Alumno").upper()
        texto = st.text_area("Aprendizaje de hoy")
        if st.button("Guardar"):
            if nombre:
                # Aseguramos que sea un diccionario antes de guardar
                if not isinstance(st.session_state.db["alumnos"], dict):
                    st.session_state.db["alumnos"] = {}
                
                if nombre not in st.session_state.db["alumnos"]:
                    st.session_state.db["alumnos"][nombre] = []
                
                st.session_state.db["alumnos"][nombre].append(texto)
                st.success(f"Guardado para {nombre}")

    elif menu == "📊 Evaluación":
        st.header("Buscador de Alumnos")
        busq = st.text_input("Nombre a buscar").upper()
        
        # Validación anti-error de tipo
        if isinstance(st.session_state.db["alumnos"], dict) and busq in st.session_state.db["alumnos"]:
            st.write(f"Historial de {busq}:")
            for entrada in st.session_state.db["alumnos"][busq]:
                st.info(entrada)
        else:
            st.warning("No hay registros aún.")

    elif menu == "🆘 SOS":
        st.error("### Central de Ayuda IA")
        st.write("Si ves el error 'TypeError', es porque intentaste buscar un nombre en una lista vacía. El código de arriba ya tiene el parche para que no vuelva a suceder.")

    if st.sidebar.button("Salir"):
        st.session_state.db["auth"] = False
        st.rerun()
