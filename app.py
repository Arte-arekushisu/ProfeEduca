# --- AGREGAR ESTO AL FINAL DE LA SECCIÓN "WITH ST.SIDEBAR:" ---

with st.sidebar:
    st.divider()
    st.markdown("### 🆘 ¿Necesitas Ayuda?")
    
    with st.expander("🚨 BOTÓN SOS - Soporte Rápido", expanded=False):
        st.error("¿Algo no funciona?")
        
        # Opción 1: Dudas sobre Gemini / IA
        if st.button("🤖 Dudas sobre la IA", use_container_width=True):
            st.info("""
            **Guía Rápida de Gemini:**
            1. **Escritos Reflexivos:** Asegúrate de escribir al menos 3 párrafos para un mejor análisis.
            2. **Campos Formativos:** Si la IA no llena el cuadro, verifica que mencionaste actividades de esa área.
            """)
            
        # Opción 2: Error Técnico
        if st.button("💻 Reportar un Error", use_container_width=True):
            st.warning("Si el PDF no se genera:")
            st.write("- Verifica que el nombre del alumno no tenga símbolos raros.")
            st.write("- Asegúrate de que las fotos no pesen más de 5MB.")
            
        # Opción 3: Contacto Directo
        st.write("---")
        st.caption("Contacto Directo:")
        st.link_button("📲 WhatsApp Soporte", "https://wa.me/tu_numero", use_container_width=True)

# --- ESTILO VISUAL LLAMATIVO (Opcional, agregar al inicio) ---
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 10px;
    }
    /* Estilo especial para el SOS si fuera un botón flotante */
    div[data-testid="stExpander"] {
        border: 2px solid #FF4B4B;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
