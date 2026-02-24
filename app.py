import streamlit as st
import requests
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN Y CREDENCIALES ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"

st.set_page_config(page_title="ProfeEduca | Fase 2", page_icon="🍎", layout="wide")

# Inicializar Supabase (solo para jalar perfil si es necesario)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inicializar Chat Temporal en la memoria de la sesión
if 'chat_temporal' not in st.session_state:
    st.session_state.chat_temporal = []

# --- 2. ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    @keyframes worm-move {
        0%, 100% { transform: translate(45px, -30px) scale(1); opacity: 0; }
        25% { transform: translate(30px, -45px) scale(1.1); opacity: 1; }
        50% { transform: translate(0px, -50px) scale(1.2); opacity: 1; }
        75% { transform: translate(-30px, -45px) scale(1.1); opacity: 1; }
        90% { transform: translate(-45px, -30px) scale(1); opacity: 0; }
    }
    .apple-container { position: relative; display: inline-block; font-size: 8rem; margin-top: 10px; }
    .worm-icon { position: absolute; font-size: 3rem; animation: worm-move 5s ease-in-out infinite; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    .slogan-final { font-style: italic; color: #94a
