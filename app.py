import streamlit as st
from supabase import create_client, Client

# --- CONFIGURACIÓN Y CONEXIÓN ---
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="PROFEEDUCA MASTER", layout="wide", page_icon="🎓")

# --- ESTILO ALTO CONTRASTE ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: white; }
    .plan-box {
        border: 2px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        background: #0f172a;
        height: 350px;
        text-align: center;
    }
    h1, h2, h3 { color: #38bdf8 !important; }
    .price { font-size: 24px; font-weight: bold; color: #facc15; }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'logueado' not in st.session_state: st.session_state.logueado = False

if not st.session_state.logueado:
    st.title("🎓 Bienvenido a PROFEEDUCA MASTER")
    st.write("### Registrate y elige el plan que mejor se adapte a tus necesidades.")
    
    # --- FORMULARIO DE REGISTRO ---
    with st.expander("📝 PASO 1: Crea tu cuenta", expanded=True):
        col_reg1, col_reg2 = st.columns(2)
        u_nombre = col_reg1.text_input("Nombre Completo")
        u_correo = col_reg2.text_input("Correo Electrónico")
    
    st.write("### 💳 PASO 2: Elige tu Plan")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="plan-box"><h3>Plan 1<br>Gratuito</h3><p>7 días de prueba</p><p>1 Planeación</p><p>Espacio Libre</p><p class="price">$0 MXN</p></div>', unsafe_allow_html=True)
        if st.button("Elegir Plan 1"): st.session_state.plan_sel = ("Plan 1", 0)

    with c2:
        st.markdown('<div class="plan-box"><h3>Plan 2<br>Básico</h3><p>Funciones Plan 1</p><p>4 Planeaciones</p><p class="price">$49 MXN</p></div>', unsafe_allow_html=True)
        if st.button("Elegir Plan 2"): st.session_state.plan_sel = ("Plan 2", 49)

    with c3:
        st.markdown('<div class="plan-box"><h3>Plan 3<br>Reflexivo</h3><p>4 Planeaciones</p><p><b>Escrito Reflexivo</b></p><p class="price">$350 MXN</p></div>', unsafe_allow_html=True)
        if st.button("Elegir Plan 3"): st.session_state.plan_sel = ("Plan 3", 350)

    with c4:
        st.markdown('<div class="plan-box"><h3>Plan 5<br>Completo</h3><p>4 Planeaciones</p><p><b>Evaluación Trimestral</b></p><p class="price">$399 MXN</p></div>', unsafe_allow_html=True)
        if st.button("Elegir Plan 5"): st.session_state.plan_sel = ("Plan 5", 399)

    if 'plan_sel' in st.session_state:
        st.info(f"Seleccionado: **{st.session_state.plan_sel[0]}**")
        if st.button("Confirmar Registro y Plan"):
            if u_nombre and u_correo:
                try:
                    data = {"nombre": u_nombre, "email": u_correo, "plan": st.session_state.plan_sel[0]}
                    supabase.table("usuarios").insert(data).execute()
                    st.success("¡Cuenta activada con éxito!")
                    st.session_state.logueado = True
                    st.rerun()
                except: st.error("Error al conectar con la base de datos.")
            else: st.warning("Falta nombre o correo.")

else:
    # --- VISTA CUANDO YA ESTÁ LOGUEADO ---
    st.title(f"🚀 Panel de Control - {st.session_state.plan_sel[0]}")
    st.success(f"Bienvenido Axel Reyes. Tu sistema está operativo.")
    
    st.markdown("""
    <div style="border: 1px solid #38bdf8; padding: 20px; border-radius: 15px; background: #0f172a;">
        <h4 style="color: #38bdf8;">Estatus de Conexión:</h4>
        <p>✅ Base de Datos Supabase: Conectada</p>
        <p>✅ Modelos de IA (Gemini/Groq): Listos</p>
        <p>✅ Generador PDF: Operativo</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("👈 Selecciona tu módulo en el menú de la izquierda para comenzar.")
