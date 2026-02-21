import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CLASE PDF MEJORADA ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'GUÍA DE APRENDIZAJE - MODELO DE DIÁLOGO', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def create_table(self, data):
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(240, 240, 240)
        for key, value in data.items():
            self.cell(50, 8, key, 1, 0, 'L', True)
            self.set_font('Arial', '', 10)
            self.cell(0, 8, value, 1, 1, 'L')
            self.set_font('Arial', 'B', 10)
        self.ln(5)

def generar_contenido_ia(tema, nivel):
    # Aquí simulamos la respuesta de la IA redactando temas reales
    # En la siguiente fase conectaremos Gemini API para que sea 100% único
    return {
        "pase_lista": f"Actividad 'El eco del saber': Al mencionar su nombre, el alumno debe decir una palabra que rime con {tema} y hacer un movimiento corporal representativo.",
        "regalo_lectura": f"Lectura de 'El viaje de {tema}': Relato breve sobre cómo este elemento influye en nuestra naturaleza. Al finalizar, cada niño compartirá qué parte le sorprendió más.",
        "bienvenida": f"Dinámica 'Círculo de Ideas': Los niños se pasan una pelota de estambre y dicen qué conocen sobre {tema}, formando una red visual de conocimientos.",
        "estacion1": f"Exploración Sensorial: Manipular materiales que representen a {tema}. Los alumnos describen texturas y formas en su cuaderno.",
        "estacion2": f"Simulación Práctica: Usar objetos reciclados para construir un modelo de {tema}, explicando su funcionamiento a sus compañeros.",
        "estacion3": f"Expresión Artística: Crear un mural comunitario donde cada alumno dibuje cómo {tema} ayuda a su propia familia.",
        "tutoreo_desarrollo": f"Profundización en {tema}: Explicar que este proceso es vital para el equilibrio local. Ejemplo: Si trabajamos {tema}, compararlo con el crecimiento de las siembras en la comunidad.",
        "tutoreo_actividades": f"1. Elaborar un diagrama de flujo con ramas y hojas secas.\n2. Crear una exposición oral para el resto del grupo usando cartones reciclados.",
        "producto": f"Maqueta funcional o álbum ilustrado de {tema} con materiales de bajo costo (tierra, cartón, envases)."
    }

def crear_pdf_final(d):
    pdf = PDF()
    pdf.add_page()
    
    # 1. TABLA DE IDENTIFICACIÓN
    pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
    tabla_datos = {
        "Nivel y Grado": f"{d['nivel']} - {d['grado']}",
        "Educador / ECA": f"{d['nombre_ed']} / {d['nombre_eca']}",
        "Comunidad": d['comunidad'],
        "Fecha": d['fecha'],
        "Tema Central": d['tema'],
        "Rincón": d['rincon'] if d['rincon'] else "General"
    }
    pdf.create_table(tabla_datos)

    # 2. OBJETIVO GENERAL
    pdf.chapter_title("II. OBJETIVO GENERAL")
    pdf.set_font('Arial', '', 10)
    objetivo = (f"Que los alumnos de {d['nivel']} comprendan a profundidad el tema '{d['tema']}' "
                "mediante procesos de investigación y diálogo colaborativo. Se busca desarrollar "
                "habilidades de observación y análisis, logrando que el estudiante sea capaz de "
                "explicar el tema con sus propias palabras y lo vincule con su vida diaria.")
    pdf.multi_cell(0, 5, objetivo)
    pdf.ln(5)

    # Contenido generado por IA
    ia = generar_contenido_ia(d['tema'], d['nivel'])

    # 3. RUTINA DE INICIO
    pdf.chapter_title("III. INICIO (MOMENTOS PEDAGÓGICOS)")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Pase de lista (5 min):", 0, 1); pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, ia['pase_lista']); pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Regalo de lectura (10 min):", 0, 1); pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, ia['regalo_lectura']); pdf.ln(2)

    # 4. ESTACIONES
    pdf.chapter_title("IV. ESTACIONES DE TRABAJO (45 min)")
    pdf.multi_cell(0, 5, f"1. {ia['estacion1']}\n\n2. {ia['estacion2']}\n\n3. {ia['estacion3']}")
    pdf.ln(5)

    # 5. TUTOREO PROFUNDO
    pdf.chapter_title(f"V. TUTOREO: {d['tema'].upper()}")
    pdf.multi_cell(0, 5, f"Introducción al tema: {ia['tutoreo_desarrollo']}")
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Actividades de desarrollo:", 0, 1); pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, ia['tutoreo_actividades'])
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Producto Final:", 0, 1); pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, ia['producto'])

    # 6. POST-RECESO
    pdf.chapter_title("VI. ACTIVIDADES POST-RECESO")
    pdf.multi_cell(0, 5, f"Materia 1: {d['materia1']}\nDesarrollo: Actividad práctica de refuerzo cognitivo utilizando materiales sobrantes.\n\nMateria 2: {d['materia2']}\nDesarrollo: Sesión de coordinación motriz y juegos tradicionales de la comunidad.")

    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ STREAMLIT (Botón Planeación ABCD) ---
# ... (Aquí va tu código de menú y columnas de la Fase anterior)
if st.session_state.seccion == "plan":
    st.header("📋 Taller de Planeación ABCD")
    # Campos de entrada...
    if st.button("🚀 GENERAR PLANEACIÓN COMPLETA", use_container_width=True):
        datos_pdf = {
            "nivel": nivel, "grado": grado, "nombre_ed": nombre_ed,
            "nombre_eca": nombre_eca, "comunidad": comunidad,
            "fecha": str(fecha), "tema": tema, "rincon": rincon,
            "materia1": m1, "materia2": m2
        }
        archivo = crear_pdf_final(datos_pdf)
        st.download_button("📥 Descargar Guía Pedagógica", archivo, f"Guia_{tema}.pdf", "application/pdf")
