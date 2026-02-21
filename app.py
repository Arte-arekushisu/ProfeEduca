import streamlit as st
import random

# --- CONFIGURACIÓN DE VERSIÓN ---
VERSION_SISTEMA = "1.4.0"
ADMIN_USER = "admin_profe"

# 1. BASE DE DATOS ESTRUCTURADA
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {
            "admin": {
                "pass": "master123", "name": "Admin", "role": "admin", 
                "plan": "Magna", "uso": {"plan": 0, "diario": 0, "eval": 0}
            }
        },
        "auth": False,
        "current_user": None,
        "step": "login"
    }

# 2. DEFINICIÓN DETALLADA DE PLANES
PLANES_INFO = {
    "Gratuito": {
        "precio": "$0", "limite": 2, 
        "incluye": "2 Planeaciones ABCD, 2 Escritos Diarios, 2 Evaluaciones.",
        "color": "gray"
    },
    "Plata": {
        "precio": "$200", "limite": 12, 
        "incluye": "12 Planeaciones ABCD, 12 Escritos Diarios, 12 Evaluaciones.",
        "color": "white"
    },
    "Oro": {
        "precio": "$300", "limite": 24, 
        "incluye": "24 Planeaciones ABCD, 24 Escritos Diarios, 24 Evaluaciones.",
        "color": "gold"
    },
    "Platino": {
        "precio": "$450", "limite": 999, 
        "incluye": "Ilimitado: Planeaciones, Escritos y Evaluaciones.",
        "color": "cyan"
    },
    "Magna": {
        "precio": "$3900", "limite": 999, 
        "incluye": "Todo Ilimitado + Soporte Prioritario (Acceso Anual).",
        "color": "red"
    }
}

# 3. INTERFAZ DE REGISTRO CON SELECCIÓN DE PLAN
def pantalla_registro():
    st.title("📝 Registro de Nuevo Educador")
    st.write("Selecciona tu plan inicial (puedes subir de nivel después)")
    
    # Mostrar beneficios antes de registrarse
    cols_p = st.columns(3)
    for i, (p_nom, p_data) in enumerate(list(PLANES_INFO.items())[:3]):
        with cols_p[i]:
            st.markdown(f"### Plan {p_nom}")
            st.write(f"**{p_data['precio']}**")
            st.caption(p_data['incluye'])

    with st.form("registro_completo"):
        col1, col2 = st.columns(2)
        nuevo_u = col1.text_input("Usuario")
        nueva_p = col2.text_input("Contraseña", type="password")
        nombre = col1.text_input("Nombre(s)")
        apellidos = col2.text_input("Apellidos")
        email = st.text_input("Correo Electrónico")
        plan_elegido = st.selectbox("Elige tu plan", list(PLANES_INFO.keys()))
        
        if st.form_submit_button("Crear mi cuenta"):
            if nuevo_u and nueva_p and email:
                st.session_state.db["usuarios"][nuevo_u] = {
                    "pass": nueva_p,
                    "name": f"{nombre} {apellidos}",
                    "email": email,
                    "plan": plan_elegido,
                    "role": "educador",
                    "uso": {"plan": 0, "diario": 0, "eval": 0} # IA gestiona desde cero
                }
                st.success("¡Registro exitoso! Ya puedes iniciar sesión.")
                st.session_state.db["step"] = "login"
                st.rerun()

# 4. DASHBOARD DEL MAESTRO CON CONTADORES POR DOCUMENTO
def mostrar_dashboard():
    user_id = st.session_state.db["current_user"]
    user_data = st.session_state.db["usuarios"][user_id]
    plan = user_data["plan"]
    limite = PLANES_INFO[plan]["limite"]
    
    st.sidebar.title(f"Maestro: {user_data['name']}")
    st.sidebar.info(f"Plan Actual: {plan}")
    
    st.title("🚀 Generador ABCD")
    
    # Cuadros de información de límites
    c1, c2, c3 = st.columns(3)
    
    def mostrar_metrica(col, titulo, actual, maximo):
        restante = "∞" if maximo > 100 else (maximo - actual)
        col.metric(titulo, f"{actual}/{maximo if maximo < 100 else '∞'}", f"Quedan: {restante}")

    mostrar_metrica(c1, "Planeaciones", user_data["uso"]["plan"], limite)
    mostrar_metrica(c2, "Escritos Diarios", user_data["uso"]["diario"], limite)
    mostrar_metrica(c3, "Evaluaciones", user_data["uso"]["eval"], limite)

    st.divider()

    # Botones de Acción
    st.subheader("¿Qué deseas crear hoy?")
    b1, b2, b3 = st.columns(3)
    
    if b1.button("📄 Nueva Planeación ABCD"):
        ejecutar_accion(user_id, "plan", "Planeación")
    
    if b2.button("✍️ Nuevo Escrito Reflexivo"):
        ejecutar_accion(user_id, "diario", "Escrito")
        
    if b3.button("📊 Nueva Evaluación Trimestral"):
        ejecutar_accion(user_id, "eval", "Evaluación")

def ejecutar_accion(user_id, tipo, nombre_doc):
    user_data = st.session_state.db["usuarios"][user_id]
    limite = PLANES_INFO[user_data["plan"]]["limite"]
    
    if user_data["uso"][tipo] < limite:
        user_data["uso"][tipo] += 1
        st.balloons()
        st.success(f"¡{nombre_doc} generada con éxito!")
    else:
        st.error(f"⚠️ Has alcanzado el límite de {nombre_doc}s para el plan {user_data['plan']}.")
        st.info("Para seguir creando, actualiza tu suscripción en la barra lateral.")

# 5. LÓGICA DE NAVEGACIÓN
if not st.session_state.db["auth"]:
    if st.session_state.db["step"] == "login":
        st.title("🍎 Profe Educa ABCD")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if u in st.session_state.db["usuarios"] and st.session_state.db["usuarios"][u]["pass"] == p:
                st.session_state.db["auth"] = True
                st.session_state.db["current_user"] = u
                st.rerun()
        if st.button("¿Eres nuevo? Regístrate"):
            st.session_state.db["step"] = "registro"
            st.rerun()
    else:
        pantalla_registro()
else:
    mostrar_dashboard()
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.db["auth"] = False
        st.rerun()
