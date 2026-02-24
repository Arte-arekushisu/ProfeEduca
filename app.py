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

# Estilo CSS corregido
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
    color: #f8fafc;
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: #38bdf8;
    text-align: center;
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
# PASO 1: REGISTRO DE EMAIL
if st.session_state.db["step"] == "registro_email":
    st.markdown("<h1 class='main-title'>📏 ProfeEduca ✏️</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1]) # Definimos las columnas para centrar
    
    with col2:
        st.subheader("Bienvenido al sistema de planeaciones")
        email = st.text_input("Ingresa tu correo institucional o personal:")
        
        if st.button("Continuar"):
            if "@" in email:
                st.session_state.db["temp"]["email"] = email
                st.session_state.db["step"] = "verificacion" # Cambiamos al siguiente paso
                st.rerun()
            else:
                st.error("Por favor, ingresa un correo electrónico válido.")
