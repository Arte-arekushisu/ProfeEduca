import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V0.8", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE GENERACIÓN PEDAGÓGICA EXTENSA ---
def generar_contenido_experto(d):
    nivel = d['nivel']
    tema = d['tema']
    
    # Adaptación de dificultad según el nivel manual
    if nivel == "Preescolar":
        enfoque = "Basado en el juego simbólico y exploración sensorial."
        ejemplo_mats = "Masilla casera, colores naturales, cartones grandes."
    elif nivel == "Primaria":
        enfoque = "Enfoque en la investigación guiada y registro gráfico."
        ejemplo_mats = "Libros de texto, lupas, material de desecho para maquetas."
    else: # Secundaria
        enfoque = "Análisis crítico, debate y sistematización de información."
        ejemplo_mats = "Fuentes bibliográficas, materiales para prototipos funcionales."

    return {
        "inicio": {
            "pase": f"Actividad 'El Eco de la Comunidad': Al mencionar su nombre, el alumno debe compartir un saber o habilidad que alguien de su familia le haya enseñado. Duración: 5 min.",
            "lectura": f"Regalo de lectura: 'Voces de nuestra tierra'. Se leerá un fragmento de un autor académico o relato comunitario. Al finalizar, cada alumno dibujará en una hoja reciclada la idea principal. Duración: 10 min.",
            "bienvenida": f"Actividad: 'El círculo de diálogo'. Los niños se sientan en círculo y comparten una meta para el día. Se utiliza una 'piedra del habla' para respetar turnos. Duración: 10 min."
        },
        "estaciones": [
            {"t": "Estación de Lenguajes", "d": f"Desarrollo: Los alumnos crearán un mural de palabras nuevas. {enfoque} Materiales: Periódicos viejos, pegamento de almidón."},
            {"t": "Estación de Saberes", "d": f"Desarrollo: Clasificación de elementos naturales del entorno. {enfoque} Materiales: Hojas secas, piedras, envases reciclados."},
            {"t": "Estación Ética y Naturaleza", "d": f"Desarrollo: Representación de un problema socio-ambiental de la comunidad y propuesta de solución."}
        ],
        "tutoreo": {
            "desarrollo": f"PROFUNDIZACIÓN: El educador guiará al alumno en el estudio de '{tema}'. Se explica que este tema es una ventana al conocimiento científico y social. Se analizarán las causas y efectos relacionados con el entorno local.",
            "actividades": [
                f"1. Investigación autónoma: Buscar en el rincón de lectura 3 fuentes que hablen sobre '{tema}'.",
                f"2. Entrevista dirigida: Preparar preguntas para un compañero que ya conozca sobre el tema.",
