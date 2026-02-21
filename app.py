import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V0.7", page_icon="🍎", layout="wide")

# (Mantener CSS de versiones anteriores para el diseño Glassmorphism)

# --- 2. MOTOR DE INTELIGENCIA PEDAGÓGICA (EXTENSO) ---
def generar_guia_detallada(d):
    # Lógica de dificultad por nivel
    dif = "juegos y cantos" if d['nivel'] == "Preescolar" else "investigación y debate"
    
    return {
        "inicio_grupo": {
            "pase_lista": "Dinámica 'El tren de las emociones'. Cada alumno, al escuchar su nombre, debe representar con un gesto cómo se siente hoy y los demás lo imitan. Esto fortalece la empatía grupal.",
            "lectura": f"Lectura de un texto literario acorde a {d['nivel']}. El educador leerá con entonación variada. Al terminar, se realizará un mapa mental gigante en el suelo usando gises o carbón.",
            "bienvenida": "Juego 'El nudo humano'. Los niños se toman de las manos y deben desenredarse sin soltarse. Al lograrlo, reflexionamos sobre la importancia de trabajar juntos."
        },
        "estaciones": [
            {"nombre": "Estación de Pensamiento", "act": f"Resolución de retos lógicos usando piedras o semillas. En {d['nivel']} se enfocarán en {dif}."},
            {"nombre": "Estación de Lenguajes", "act": "Creación de un diccionario mural con palabras nuevas descubiertas en la semana usando recortes y dibujos."},
            {"nombre": "Estación de Saberes", "act": f"Experimento práctico sobre un fenómeno natural local (viento, sol o agua) usando materiales de reuso."}
        ],
        "tutoreo_especifico": {
            "introduccion": f"El tema '{d['tema']}' se abordará de forma personalizada. Se inicia rescatando qué sabe el alumno sobre esto y planteando un reto que lo obligue a investigar más allá de lo evidente.",
            "actividad_1": f"Investigación profunda: El alumno buscará en libros del rincón o entrevistará a un compañero sobre aspectos clave de '{d['tema']}'.",
            "actividad_2": "Registro creativo: Elaboración de un borrador de su proceso de aprendizaje (RPA) usando dibujos y textos explicativos.",
            "producto": f"Creación de un modelo físico o cartilla informativa sobre '{d['tema']}' para presentar al resto de la comunidad escolar."
        },
        "post_receso": {
            "materia1": f"Actividad de {d['materia1']}: Secuencia de ejercicios coordinados que integran el conteo o la lectoescritura según el grado.",
            "materia2": f"Actividad de {d['materia2']}: Espacio de libre creación con materiales sobrantes (telas, cartón, plástico) para resolver un problema del aula."
        }
    }

# --- 3. LÓGICA DE INTERFAZ ---
if 'seccion' not in st.session_state: st.session_state.seccion = "inicio"

col_menu, col_main = st.columns([1, 2.5])

with col_menu:
    st.title("🍎 Menú")
    if st.button("🏠 Inicio", use_container_width=True): st.session_state.seccion = "inicio"
    if st.button("📝 Planeación ABCD", use_container_width=True): st.session_state.seccion = "plan"

with col_main:
    if st.session_state.seccion == "plan":
        st.header("📋 Taller de Planeación ABCD")
        
        with st.expander("📝 Configuración de la Clase", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                nivel = st.selectbox("Nivel educativo", ["Preescolar", "Primaria", "Secundaria"])
                grado = st.text_input("Grado específico", placeholder="Ej. 1º y 2º Multigrado")
                nombre_ed = st.text_input("Nombre del Educador")
                nombre_eca = st.text_input("Nombre del ECA")
            with c2:
                comunidad = st.text_input("Comunidad")
                tema = st.text_input("Tema de interés (Tutoreo)", placeholder="Ej. Las abejas")
                m1 = st.text_input("Post-receso 1", value="Educación Física")
                m2 = st.text_input("Post-receso 2", value="Artes")
        
        if st.button("👁️ Visualizar Planeación", use_container_width=True):
            if not tema or not nombre_ed:
                st.warning("Por favor, completa los datos básicos.")
            else:
                guia = generar_guia_detallada({"nivel": nivel, "tema": tema, "materia1": m1, "materia2": m2})
                
                st.markdown("---")
                st.subheader("👀 Vista Previa de tu Planeación")
                
                st.write(f"**Objetivo:** Lograr que el grupo de {nivel} desarrolle autonomía mientras se profundiza en {tema}.")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("### 🕒 Rutina Grupal")
                    st.write(f"**Inicio:** {guia['inicio_grupo']['pase_lista']}")
                    st.write(f"**Lectura:** {guia['inicio_grupo']['lectura']}")
                with col_b:
                    st.markdown("### 🧠 Tutoreo Personalizado")
                    st.write(f"**Tema:** {tema}")
                    st.write(f"**Actividad:** {guia['tutoreo_especifico']['actividad_1']}")
                
                # Botón de descarga aparece solo después de visualizar
                st.success("Si la información es correcta, procede a descargar el PDF completo.")
                # (Aquí iría la función de generación de PDF que ya tenemos, pero usando estos textos largos)
