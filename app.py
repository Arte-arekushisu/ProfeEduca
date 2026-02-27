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
""", unsafe_allow_html=True)

# --- LÓGICA ---
if 'logueado' not in st.session_state: st.session_state.logueado = False

if not st.session_state.logueado:
    st.markdown("<h1>🎓 PROFEEDUCA MASTER</h1>", unsafe_allow_html=True)
    st.write("<h4 style='text-align: center; color: #94a3b8;'>Impulsa tu labor docente con Inteligencia Artificial</h4>", unsafe_allow_html=True)
    st.write("---")
    
    # --- FORMULARIO ---
    with st.container():
        st.subheader("📝 Paso 1: Tu Identidad Digital")
        c_form1, c_form2 = st.columns(2)
        u_nombre = c_form1.text_input("Nombre Completo")
        u_correo = c_form2.text_input("Correo Institucional")
    
    st.write("### 💳 Paso 2: Selecciona tu Nivel de Poder")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('''<div class="plan-box">
            <h3>🌱 EXPLORADOR</h3>
            <div class="feature-list">
                • 7 Días de prueba<br>
                • 1 Planeación ABCD<br>
                • Acceso a Espacio Libre
            </div>
            <p class="price">$0 MXN</p>
        </div>''', unsafe_allow_html=True)
        if st.button("🚀 Iniciar Prueba Gratis", key="p1"): 
            st.session_state.plan_sel = ("Explorador (Gratis)", 0)
            st.balloons()

    with c2:
        st.markdown('''<div class="plan-box" style="border-color: #0ea5e9;">
            <h3>⚡ IMPULSO BÁSICO</h3>
            <div class="feature-list">
                • Todo lo del Explorador<br>
                • Genera 4 Planeaciones<br>
                • Soporte Estándar
            </div>
            <p class="price">$49 MXN</p>
        </div>''', unsafe_allow_html=True)
        if st.button("🔥 Elegir Impulso", key="p2"): 
            st.session_state.plan_sel = ("Impulso Básico", 49)
            st.balloons()

    with c3:
        st.markdown('''<div class="plan-box" style="border-color: #a855f7;">
            <h3>🧠 MENTOR REFLEXIVO</h3>
            <div class="feature-list">
                • Genera 4 Planeaciones<br>
                • <b>Escrito Reflexivo IA</b><br>
                • Análisis Pedagógico
            </div>
            <p class="price">$350 MXN</p>
        </div>''', unsafe_allow_html=True)
        if st.button("💎 Elegir Mentor", key="p3"): 
            st.session_state.plan_sel = ("Mentor Reflexivo", 350)
            st.balloons()

    with c4:
        st.markdown('''<div class="plan-box" style="border-color: #facc15;">
            <h3>👑 MAESTRO ELITE</h3>
            <div class="feature-list">
                • Genera 4 Planeaciones<br>
                • <b>Evaluación Trimestral IA</b><br>
                • Acceso Total de por vida
            </div>
            <p class="price">$399 MXN</p>
        </div>''', unsafe_allow_html=True)
        if st.button("⭐ Elegir Elite", key="p4"): 
            st.session_state.plan_sel = ("Maestro Elite", 399)
            st.balloons()

    # --- BOTÓN FINAL ---
    if 'plan_sel' in st.session_state:
        st.success(f"Has seleccionado: **{st.session_state.plan_sel[0]}**")
        if st.button("CONFIRMAR REGISTRO Y ACTIVAR 🚀", use_container_width=True):
            if u_nombre and u_correo:
                try:
                    data = {"nombre": u_nombre, "email": u_correo, "plan": st.session_state.plan_sel[0]}
                    supabase.table("usuarios").insert(data).execute()
                    st.session_state.logueado = True
                    st.rerun()
                except: st.error("Error de conexión. Verifica tu internet.")
            else: st.warning("¡Oye! No olvides poner tu nombre y correo.")

else:
    # --- PANEL PRINCIPAL ---
    st.title(f"🚀 Centro de Mando: {st.session_state.plan_sel[0]}")
    st.success(f"¡Bienvenido de nuevo, Maestro/a!")
    st.info("👈 Navega entre tus herramientas usando el menú lateral.")
    
    st.markdown("""
    <div style="padding: 20px; border-radius: 15px; background: #0f172a; border: 1px solid #38bdf8;">
        <h4 style="color: #38bdf8;">Estado de tu cuenta:</h4>
        <p>👤 <b>Usuario:</b> Identificado</p>
        <p>📊 <b>Plan Activo:</b> """ + st.session_state.plan_sel[0] + """</p>
        <p>✅ <b>Motor IA:</b> Conectado y listo</p>
    </div>
    """, unsafe_allow_html=True)
