import streamlit as st
from supabase import create_client, Client

# --- CONFIGURACIÓN Y CONEXIÓN ---
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="PROFEEDUCA MASTER", layout="wide", page_icon="🎓")

# --- ESTILO VISUAL LLAMATIVO ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: white; }
    
    .plan-box {
        border: 2px solid #38bdf8;
        padding: 20px;
        border-radius: 20px;
        background: linear-gradient(145deg, #0f172a, #1e293b);
        height: 420px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.2);
        transition: transform 0.3s ease;
    }
    .plan-box:hover {
        transform: translateY(-10px);
        border-color: #7dd3fc;
        box-shadow: 0 20px 25px -5px rgba(56, 189, 248, 0.4);
    }
    
    h1 { font-size: 3.5rem !important; color: #38bdf8 !important; text-align: center; font-weight: 900 !important; }
    h3 { color: #f8fafc !important; font-size: 1.5rem !important; margin-bottom: 10px; }
    
    .price { 
        font-size: 28px; 
        font-weight: 900; 
        color: #fbbf24; 
        margin-top: 15px;
        text-shadow: 0 0 10px rgba(251, 191, 36, 0.4);
    }
    
    .feature-list { text-align: left; font-size: 0.9rem; color: #cbd5e1; height: 120px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=
