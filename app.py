import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V1.1", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE REDACCIÓN EXTENSA (4 CAMPOS FORMATIVOS) ---
def generar_texto_educativo(d):
    n = d['nivel']
    t = d['tema']
    
    return {
        "inicio": {
            "pase": "Actividad 'El eco de mi voz': Al mencionar su nombre, cada alumno comparte una palabra clave o saber previo sobre el entorno. (10 min).",
            "lectura": f"Regalo de lectura: Texto literario acorde a {n}. Reflexión grupal sobre el mensaje central y cómo se conecta con la realidad local. (15 min).",
            "bienvenida": "Dinámica 'El pulso del grupo': Sincronización rítmica con aplausos para enfocar la atención y crear cohesión grupal. (5 min)."
        },
        "estaciones": [
            {
                "campo": "Lenguajes",
                "act": f"Creación de un 'Códice Comunitario'. Instrucciones: Los alumnos redactarán o dibujarán un mensaje sobre cómo {t} impacta en su lenguaje cotidiano. Materiales: Hojas, colores, recortes de periódicos."
            },
            {
                "campo": "Saberes y Pensamiento Científico",
                "act": f"Laboratorio de observación. Instrucciones: Analizar las formas, medidas y ciclos relacionados con {t}. Uso de conteo o gráficas simples según el grado. Materiales: Semillas, reglas, lupas."
            },
            {
                "campo": "Ética, Naturaleza y Sociedades",
                "act": f"Círculo de justicia ambiental. Instrucciones: Diálogo reflexivo sobre el impacto humano en {t}. Propuesta de un 'Acuerdo de Convivencia' para proteger el entorno natural."
            },
            {
                "campo": "De lo Humano y lo Comunitario",
                "act": f"Feria de identidades. Instrucciones: Juego de roles donde se representa el papel de cada miembro de la comunidad en el cuidado de {t}. Fortalecimiento del tejido social."
            }
        ],
        "tutoreo": {
            "intro": f"Estudio profundo de '{t}': El alumno lidera su propia investigación bajo la guía del tutor, analizando fuentes del rincón de lectura y conectándolas con su experiencia personal.",
            "pasos": [
                "1. Pregunta detonante: ¿Qué misterio o curiosidad de este tema te gustaría investigar hoy?",
                "2. Registro RPA: Narrativa personal escrita o dibujada del proceso de aprendizaje y nuevos hallazgos.",
                "3. Producto: Una maqueta, cartel informativo o demostración pública para compartir con la comunidad escolar."
            ]
        }
    }

# --- 3. CLASE PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'PLANEACIÓN PEDAGÓGICA - 4 CAMPOS FORMATIVOS', 0, 1, 'C')
        self.ln(5)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

# --- 4. INTERFAZ ---
st.header("📋 Taller de Planeación Integral")

with st.form("form_final"):
    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
        grado = st.text_input("Grado específico", value="1º y 2º Multigrado")
        nombre_ed = st.text_input("Nombre del Educador")
        nombre_eca = st.text_input("Nombre del ECA")
    with c2:
        comunidad = st.text_input("Comunidad")
        fecha = st.date_input("Fecha de planeación")
        tema = st.text_input("Tema de Interés (Solo para Tutoreo)", placeholder="Ej. El ciclo del agua")
        rincon = st.text_input("Rincón asignado")
    
    st.markdown("---")
    m1 = st.text_input("Materia Post-Receso 1", value="Educación Física")
    m2 = st.text_input("Materia Post-Receso 2", value="Artes")
    
    submit = st.form_submit_button("🚀 GENERAR PLANEACIÓN Y VISTA PREVIA")

if submit:
    if not tema or not nombre_ed:
        st.error("⚠️ Completa los campos obligatorios (Nombre y Tema).")
    else:
        # Se definen las variables dentro del flujo de ejecución para evitar el NameError
        datos = {
            "nivel": nivel, "grado": grado, "nombre_ed": nombre_ed, 
            "nombre_eca": nombre_eca, "comunidad": comunidad, 
            "fecha": str(fecha), "tema": tema, "rincon": rincon, 
            "m1": m1, "m2": m2
        }
        
        c = generar_texto_educativo(datos)
        
        # --- VISTA PREVIA ---
        st.markdown("---")
        st.subheader("👁️ Vista Previa")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("#### Estaciones por Campos Formativos")
            for e in c['estaciones']:
                st.write(f"**{e['campo']}:** {e['act']}")
        with col_v2:
            st.markdown("#### Tutoreo Personalizado")
            st.write(c['tutoreo']['intro'])
            st.write(f"**Pasos sugeridos:** {', '.join(c['tutoreo']['pasos'])}")

        # --- GENERACIÓN DE PDF ---
        pdf = PDF()
        pdf.add_page()
        
        pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
        pdf.set_font('Arial', 'B', 10)
        items = [
            ["Educador", nombre_ed], ["ECA", nombre_eca], 
            ["Nivel/Grado", f"{nivel}/{grado}"], ["Comunidad", comunidad], 
            ["Fecha", str(fecha)], ["Rincón", rincon]
        ]
        for k, v in items:
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(50, 8, k, 1, 0, 'L', True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 8, str(v), 1, 1, 'L')
            pdf.set_font('Arial', 'B', 10)
        
        pdf.chapter_title("II. INICIO Y BIENVENIDA")
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, f"{c['inicio']['pase']}\n\n{c['inicio']['lectura']}\n\n{c['inicio']['bienvenida']}")

        pdf.chapter_title("III. ESTACIONES POR CAMPOS FORMATIVOS")
        for e in c['estaciones']:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 8, e['campo'], 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, e['act'])
            pdf.ln(2)

        pdf.chapter_title(f"IV. TUTOREO: {tema.upper()}")
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, c['tutoreo']['intro'])
        for p in c['tutoreo']['pasos']:
            pdf.multi_cell(0, 5, f"- {p}")

        pdf.chapter_title("V. POST-RECESO")
        pdf.multi_cell(0, 5, f"1. {m1}: Actividad de reforzamiento físico o lógico.\n2. {m2}: Cierre artístico y reflexión colectiva sobre los hallazgos del día.")

        # Manejo de salida PDF
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="📥 DESCARGAR PLANEACIÓN COMPLETA (PDF)", 
            data=pdf_bytes, 
            file_name=f"Planeacion_{tema}.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
