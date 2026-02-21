import streamlit as st
from PIL import Image
import base64
import io
import random
import time

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="ProfeEduca | Planeaciones ABCD", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    
    /* Estilo Barra Lateral Versión 0.2 */
    .identity-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #38bdf8;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.2);
        margin-bottom: 20px;
    }
    .brand-name { color: #38bdf8; font-size: 1.5rem; font-weight: 900; }
    .slogan-text { font-style: italic; font-size: 0.85rem; color: #94a3b8; margin-top: 15px; line-height: 1.4; border-top: 1px solid rgba(56, 189, 248, 0.2); padding-top: 10px; }
    
    /* Foto de perfil circular 0.1 */
    .profile-pic { border-radius: 50%; width: 120px; height: 120px; object-fit: cover; border: 3px solid #38bdf8; display: block; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS Y ESTADO (V0.1) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "profe2024", "name": "Admin", "plan": "Magna", "pic": None}},
        "step": "registro_email", 
        "auth": False,
        "menu": "inicio",
        "temp": {}
    }

def image_to_base64(image_file):
    if image_file:
        img = Image.open(image_file)
        img.thumbnail((300, 300))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- 3. LÓGICA DE FLUJO (UNIFICADA) ---

# SI EL USUARIO NO ESTÁ AUTENTICADO -> MOSTRAR REGISTRO/LOGIN (V0.1)
if not st.session_state.db["auth"]:
    
    if st.session_state.db["step"] == "registro_email":
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.title("🍎 ProfeEduca")
            email = st.text_input("Correo Electrónico")
            if st.button("Enviar Código"):
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "verificacion"; st.rerun()

    elif st.session_state.db["step"] == "verificacion":
        st.write(f"Código para {st.session_state.db['temp']['email']}: {st.session_state.db['temp']['code']}")
        code_in = st.text_input("Ingresa el código")
        if st.button("Validar"):
            if code_in == st.session_state.db["temp"]["code"]:
                st.session_state.db["step"] = "perfil"; st.rerun()

    elif st.session_state.db["step"] == "perfil":
        st.title("👤 Perfil del Educador")
        foto = st.file_uploader("Sube tu foto", type=['jpg', 'png'])
        n = st.text_input("Nombre"); a = st.text_input("Apellidos")
        u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
        if st.button("Finalizar Registro"):
            st.session_state.db["temp"].update({"name": f"{n} {a}", "user": u, "pass": p, "pic": image_to_base64(foto)})
            st.session_state.db["step"] = "planes"; st.rerun()

    elif st.session_state.db["step"] == "planes":
        st.title("💎 Elige tu Plan")
        if st.button("Activar Plan Magna (Prueba)"):
            t = st.session_state.db["temp"]
            st.session_state.db["usuarios"][t["user"]] = {"pass": t["pass"], "name": t["name"], "plan": "Magna", "pic": t["pic"]}
            st.session_state.db["auth"] = True; st.rerun()

# SI EL USUARIO YA ESTÁ AUTENTICADO -> MOSTRAR DASHBOARD (V0.2)
else:
    user_data = st.session_state.db["usuarios"][st.session_state.db["temp"].get("user", "admin")]
    
    # BARRA LATERAL CON IDENTIDAD 0.2
    with st.sidebar:
        if user_data["pic"]:
            st.markdown(f'<img src="data:image/png;base64,{user_data["pic"]}" class="profile-pic">', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="identity-card">
                <span style="font-size: 2.5rem;">🍎🐛📏✏️</span>
                <div style="color:white; font-weight:800; margin:10px 0;">🍎 PLANEACIONES PARA EL<br>MAESTRO ABCD</div>
                <div class="brand-name">ProfeEduca 🍎</div>
                <div class="slogan-text">
                    "Sembrando saberes en el corazón de la comunidad,<br>
                    donde la distancia no limita el aprendizaje,<br>
                    cosechando el futuro de México con cada lección."
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 INICIO", use_container_width=True): st.session_state.db["menu"] = "inicio"
        if st.button("📝 PLANEACIÓN ABCD", use_container_width=True): st.session_state.db["menu"] = "planeacion"
        if st.button("🚪 CERRAR SESIÓN"): st.session_state.db["auth"] = False; st.rerun()

    # CONTENIDO SEGÚN EL MENÚ
    if st.session_state.db["menu"] == "inicio":
        st.title(f"Bienvenido, Maestro {user_data['name']}")
        st.write("Tu ecosistema de trabajo está listo.")
    
    elif st.session_state.db["menu"] == "planeacion":
        st.title("📝 Área de Planeación ABCD")
        st.info("Aquí conectaremos el formulario con la IA Gemini en la siguiente fase.")
