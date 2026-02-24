import streamlit as st
from PIL import Image
import base64
import io
import random
import time
from fpdf import FPDF
import unicodedata
import datetime

# --- CONFIGURACIÓN Y ESTILO EMPRESARIAL ---
st.set_page_config(page_title="ProfeEduca | Planeaciones ABCD", page_icon="🍎", layout="wide")
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
    color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE ESTADOS ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {"admin": {"pass": "profe2024", "name": "Admin", "plan": "Magna"}},
        "step": "registro_email",
        "temp": {}
    }

# --- FLUJO DE PANTALLAS ---
if st.session_state.db["step"] == "registro_email":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div style="text-align:center; font-size:4rem;">💼</div>', unsafe_allow_html=True)
        st.title("🍎 ProfeEduca")
        st.subheader("Planeaciones para el Maestro ABCD")
        st.write("Inicia tu registro empresarial ingresando tu correo.")
        email = st.text_input("Correo Electrónico")
        if st.button("Enviar Código de Seguridad"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["temp"]["code"] = str(random.randint(100000, 999999))
                st.session_state.db["step"] = "
