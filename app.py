import streamlit as st
import datetime

# --- CONFIGURACIÓN DE VERSIÓN ---
VERSION_SISTEMA = "1.3.0"

# 1. BASE DE DATOS ESTRUCTURADA CON PLANES
if 'db' not in st.session_state:
    st.session_state.db = {
        "usuarios": {
            "admin": {
                "pass": "master123", 
                "name": "Administrador", 
                "role": "admin", 
                "plan": "Magna",
                "uso": {"plan": 0, "diario": 0, "eval": 0}
            }
        },
        "auth": False,
        "current_user": None,
        "step": "login"
    }

# 2. DEFINICIÓN DE PLANES Y PRECIOS
# He estructurado los límites para que el sistema los valide antes de cada descarga
PLANES = {
    "Gratuito": {"precio": "7 días prueba", "limite": 2, "desc": "Ideal para probar la herramienta."},
    "Plata":    {"precio": "$200", "limite": 12, "desc": "Para maestros con grupos pequeños."},
    "Oro":      {"precio": "$300", "limite": 24, "desc": "Eficiencia total para tu salón."},
    "Platino":  {"precio": "$450", "limite": 9999, "desc": "Acceso total sin límites mensuales."},
    "Magna":    {"precio": "$3900 (Anual)", "limite": 9999, "desc": "El prestigio máximo del educador."}
}

# 3. INTERFAZ DE USUARIO (DENTRO DEL PANEL)
def mostrar_dashboard():
    user_id = st.session_state.db["current_user"]
    user_data = st.session_state.db["usuarios"][user_id]
    plan = user_data["plan"]
    limite = PLANES[plan]["limite"]
    
    st.title(f"🍎 Panel de Control - {user_data['name']}")
    
    # Barra de estado de suscripción
    cols = st.columns(4)
    with cols[0]:
        st.metric("Tu Plan", plan)
    with cols[1]:
        # Si es Magna o Platino, el límite es infinito visualmente
        uso_actual = user_data["uso"]["plan"] + user_data["uso"]["diario"] + user_data["uso"]["eval"]
        restante = "∞" if limite > 1000 else (limite - uso_actual)
        st.metric("Créditos restantes", restante)
    
    st.divider()

    # --- SIMULACIÓN DE CONTENIDO ---
    st.subheader("🛠️ Herramientas de Generación")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.write("📋 **Planeación ABCD**")
        if st.button("Generar Planeación"):
            validar_y_generar(user_id, "plan")

    with c2:
        st.write("✍️ **Escrito Reflexivo**")
        if st.button("Generar Escrito"):
            validar_y_generar(user_id, "diario")

    with c3:
        st.write("📊 **Evaluación Trimestral**")
        if st.button("Generar Evaluación"):
            validar_y_generar(user_id, "eval")

# 4. MOTOR DE VALIDACIÓN DE LÍMITES
def validar_y_generar(user_id, tipo_doc):
    user_data = st.session_state.db["usuarios"][user_id]
    plan = user_data["plan"]
    limite = PLANES[plan]["limite"]
    uso_actual = sum(user_data["uso"].values())

    if uso_actual < limite:
        # Aumentar el contador
        user_data["uso"][tipo_doc] += 1
        st.success(f"✅ Documento generado. Uso actual: {uso_actual + 1}/{limite if limite < 1000 else '∞'}")
        # Aquí llamaríamos a la función del PDF que hicimos antes
    else:
        st.error(f"❌ Has agotado tus créditos del plan {plan}.")
        st.info("Mejora tu suscripción para seguir creando materiales.")
        mostrar_tabla_precios()

# 5. TABLA DE PRECIOS PROFESIONAL
def mostrar_tabla_precios():
    st.markdown("### 🚀 Mejora tu Nivel Educativo")
    cols = st.columns(len(PLANES))
    for i, (nombre, info) in enumerate(PLANES.items()):
        with cols[i]:
            st.info(f"**{nombre}**")
            st.write(f"**{info['precio']}**")
            st.caption(info['desc'])
            if st.button(f"Elegir {nombre}", key=f"btn_{nombre}"):
                st.toast(f"Redirigiendo a pasarela de pago para plan {nombre}...")

# --- LÓGICA PRINCIPAL ---
if not st.session_state.db["auth"]:
    # Aquí iría el código de Login/Registro que ya tenemos
    st.warning("Inicia sesión para ver tus límites de suscripción.")
    # (Para efectos de esta demo, vamos a simular que el admin entra)
    if st.button("Simular Entrada Admin"):
        st.session_state.db["auth"] = True
        st.session_state.db["current_user"] = "admin"
        st.rerun()
else:
    mostrar_dashboard()
    if st.sidebar.button("Ver Planes"):
        mostrar_tabla_precios()
