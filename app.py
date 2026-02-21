import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V1.1", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE REDACCIÓN EXTENSA (4 CAMPOS FORMATIVOS) ---
def generar_texto_educativo(d):
    n = d['nivel']
    t = d['tema']
    
    # Adaptación por nivel
    if n == "Preescolar":
        enfoque = "exploración sensorial y juego."
    elif n == "Primaria":
        enfoque = "investigación guiada y registro gráfico."
    else:
        enfoque = "pensamiento crítico y proyectos técnicos."

    return {
        "inicio": {
            "pase": "Actividad 'El eco de mi voz': Al mencionar su nombre, cada alumno menciona una palabra que rime o un saber previo. (10 min).",
            "lectura": f"Regalo de lectura: Texto literario acorde a {n}. Reflexión grupal sobre el mensaje central. (15 min).",
            "bienvenida": "Dinámica 'El pulso del grupo': Sincronización rítmica con aplausos para enfocar la atención. (5 min)."
        },
        "estaciones": [
            {
                "campo": "Lenguajes",
                "act": f"Creación de un 'Códice Comunitario'. Instrucciones: Los alumnos redactarán o dibujarán un mensaje sobre cómo {t} impacta en su lenguaje cotidiano. Materiales: Hojas, colores, recortes."
            },
            {
                "campo": "Saberes y Pensamiento Científico",
                "act": f"Laboratorio de observación. Instrucciones: Analizar las formas y medidas relacionadas con {t}. Uso de conteo o gráficas simples según el grado. Materiales: Semillas, reglas, lupas."
            },
            {
                "campo": "Ética, Naturaleza y Sociedades",
                "act": f"Círculo de justicia ambiental. Instrucciones: Debate sobre el cuidado del entorno en relación a {t}. Propuesta de un 'Acuerdo de Convivencia' con la naturaleza."
            },
            {
                "campo": "De lo Humano y lo Comunitario",
                "act": f"Feria de identidades. Instrucciones: Juego de roles donde se representa cómo {t} une a la comunidad. Fortalecimiento del tejido social y empatía."
            }
        ],
        "tutoreo": {
            "intro": f"Estudio profundo de '{t}': El alumno lidera su propia investigación bajo la guía del tutor, buscando fuentes confiables en el rincón de lectura.",
            "pasos": [
                "1. Pregunta detonante: ¿Qué misterio de este tema quieres resolver?",
                "2. Registro RPA: Narrativa personal del proceso de aprendizaje.",
                "3. Producto: Una maqueta, cartel o demostración pública para la comunidad escolar."
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
        self.set_font('Arial', 'B', 11); self.set_fill_color(30, 41, 59); self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True); self.set_text_color(0, 0, 0); self.ln(3)

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
        fecha = st.date_input("Fecha de aplicación")
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
        datos = {"nivel": nivel, "grado": grado, "nombre_ed": nombre_ed, "nombre_eca": nombre_eca, 
                 "comunidad": comunidad, "fecha": str(fecha), "tema": tema, "rincon": rincon, "m1": m1, "m2": m2}
        
        c = generar_texto_educativo(datos)
        
        # --- VISTA PREVIA ---
        st.markdown("### 👁️ Vista Previa")
        st.info(f"**Tema de Tutoreo:** {tema} | **Enfoque:** {nivel}")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.write("**Estaciones de Trabajo:**")
            for e in c['estaciones']:
                st.write(f"- **{e['campo']}:** {e['act']}")
        with col_v2:
            st.write("**Tutoreo Personalizado:**")
            st.write(c['tutoreo']['intro'])
            st.write(f"**Producto Final sugerido:** {c['tutoreo']['pasos'][2]}")

        # --- GENERAR PDF ---
        pdf = PDF()
        pdf.add_page()
        
        pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
        pdf.set_font('Arial', 'B',
