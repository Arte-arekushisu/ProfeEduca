import streamlit as st
import random

# --- CONFIGURACIÓN DE VERSIÓN ---
VERSION_SISTEMA = "1.4.1"
ADMIN_USER = "admin_profe"

# 1. BASE DE DATOS ESTRUCTURADA
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {
            "admin": {
                "pass": "master123", "name": "Admin Master", "role": "admin", 
                "plan": "Magna", "uso": {"plan": 0, "diario": 0, "eval": 0}
            }
        },
        "auth": False,
        "current_user": None,
        "step": "login"
    }

# 2. DEFINICIÓN DETALLADA DE PLANES (Precios y Límites Actualizados)
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
        "precio": "$450", "limite": 9999, 
        "incluye": "Ilimitado: Planeaciones, Escritos y Evaluaciones (Mensual).",
        "color": "cyan"
    },
    "Magna": {
        "precio": "$3999", "limite": 9999, 
        "incluye": "TODO ILIMITADO + Soporte VIP (Anualidad Premium).",
        "color": "red"
    }
}

# 3. INTERFAZ DE REGISTRO
def pantalla_registro():
    st.title("📝 Registro de Nuevo Educador")
    st.write("Explora nuestros planes y elige el que mejor se adapte a tu labor docente:")
    
    # Mostrar beneficios en columnas (ahora en 5 para incluir Magna)
    cols_p = st.columns(5)
    planes_lista = list(PLANES_INFO.items())
    for i, (p_nom, p_data) in enumerate(planes_lista):
        with cols_p[i]:
            st.markdown(f"### {p_nom}")
            st.markdown(f"**{p_data['precio']}**")
            st.caption(p_data['incluye'])

    with st.form("registro_completo"):
        col1, col2 = st.columns(2)
        nuevo_u = col1.text_input("Nombre de Usuario")
        nueva_p = col2.text_input("Contraseña", type="password")
        nombre = col1.text_input("Nombre(s)")
        apellidos = col2.text_input("Apellidos")
        email = st.text_input("Correo Electrónico de Verificación")
        plan_elegido = st.selectbox("Selecciona tu suscripción", list(PLANES_INFO.keys()))
        
        if st.form_submit_button("Finalizar Registro"):
            if nuevo_u and nueva_p and email:
                st.session_state.db["usuarios"][nuevo_u] = {
                    "pass": nueva_p,
                    "name": f"{nombre} {apellidos}",
                    "email": email,
                    "plan": plan_elegido,
                    "role": "educador",
                    "uso": {"plan": 0, "diario": 0, "eval": 0}
                }
                st.success(f"¡Bienvenido Maestro {nombre}! Cuenta creada con el plan {plan_elegido}.")
                st.session_state.db["step"] = "login"
                st.rerun()
            else:
                st.error("Faltan datos importantes para crear tu espacio seguro.")

# 4. DASHBOARD DEL MAESTRO
def mostrar_dashboard():
    user_id = st.session_state.db["current_user"]
    user_data = st.session_state.db["usuarios"][user_id]
    plan = user_data["plan"]
    limite = PLANES_INFO[plan]["limite"]
    
    st.sidebar.title(f"🍎 Profe Educa")
