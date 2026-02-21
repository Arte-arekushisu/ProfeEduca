import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ProfeEduca V1.0", page_icon="🍎", layout="wide")

# --- 2. MOTOR DE REDACCIÓN EXTENSA (Basado en tu nivel seleccionado) ---
def generar_texto_educativo(d):
    nivel = d['nivel']
    tema = d['tema']
    
    # Adaptación de lenguaje pedagógico
    if nivel == "Preescolar":
        metodo = "a través del juego y la exploración de texturas."
    elif nivel == "Primaria":
        metodo = "mediante la investigación guiada y el registro en cuadernos."
    else:
        metodo = "con análisis crítico, debates y prototipos funcionales."

    return {
        "inicio": {
            "pase": f"Actividad 'El eco de mi comunidad': Al mencionar su nombre, cada alumno menciona una palabra que rime con su nombre o un objeto que traiga de casa. Esto fomenta la identidad y la escucha activa. (5-10 min).",
            "lectura": f"Regalo de lectura: Se realizará la lectura en voz alta de un texto literario acorde a {nivel}. El educador hará pausas para preguntar '¿Qué creen que pasará después?'. Al final, se hará un dibujo rápido de la escena favorita. (15 min).",
            "bienvenida": f"Actividad rítmica: 'El pulso del grupo'. Usando aplausos o percusiones en las mesas, seguimos un ritmo coordinado para sincronizar la energía del grupo antes de iniciar. (10 min)."
        },
        "estaciones": [
            {"t": "Estación 1: Lenguajes", "d": f"Instrucciones: Los alumnos diseñarán un cartel informativo usando recortes de periódico y dibujos. El objetivo es comunicar un mensaje positivo a la comunidad. {metodo}"},
            {"t": "Estación 2: Saberes", "d": f"Instrucciones: Experimentación con materiales del entorno (tierra, agua, hojas) para observar cambios físicos. Registro de observaciones en una cartulina colectiva. {metodo}"},
            {"t": "Estación 3: Ética y Naturaleza", "d": f"Instrucciones: Diálogo sobre el cuidado del agua en la comunidad. Los alumnos proponen dos acciones concretas para ahorrar agua en la escuela. {metodo}"}
        ],
        "tutoreo": {
            "intro": f"El estudio de '{tema}' es fundamental para entender nuestro entorno. Se busca que el alumno desarrolle curiosidad científica y capacidad de síntesis.",
            "pasos": [
                f"1. Exploración inicial: ¿Qué te llamó la atención de {tema}? Lluvia de ideas.",
                f"2. Investigación: Uso de libros del rincón y diccionarios para definir conceptos clave de {tema}.",
                f"3. Relación de Aprendizaje (RPA): El alumno redacta qué sabía antes y qué descubrió ahora.",
                f"4. Demostración pública: Preparar una exposición breve para compartir con un compañero."
            ],
            "producto": f"Maqueta o álbum ilustrado detallado sobre '{tema}' utilizando materiales de reúso encontrados en la comunidad."
        }
    }

# --- 3. DISEÑO DEL PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'GUÍA PEDAGÓGICA - MODELO DE DIÁLOGO', 0, 1, 'C')
        self.ln(5)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 11); self.set_fill_color(30, 41, 59); self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', True); self.set_text_color(0, 0, 0); self.ln(3)

# --- 4. INTERFAZ (Campos manuales restaurados) ---
if 'seccion' not in st.session_state: st.session_state.seccion = "plan"

# Menú lateral
with st.sidebar:
    st.title("🍎 ProfeEduca")
    if st.button("📝 Crear Planeación"): st.session_state.seccion = "plan"

if st.session_state.seccion == "plan":
    st.header("📋 Taller de Planeación ABCD")
    
    with st.form("formulario_completo"):
        c1, c2 = st.columns(2)
        with c1:
            nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria"])
            grado = st.text_input("Grado específico", placeholder="Ej. 2º Grado")
            nombre_ed = st.text_input("Nombre del Educador")
            nombre_eca = st.text_input("Nombre del ECA")
        with c2:
            comunidad = st.text_input("Comunidad")
            fecha = st.date_input("Fecha de aplicación")
            tema = st.text_input("Tema de Interés (Para Tutoreo)", placeholder="Ej. Las abejas")
            rincon = st.text_input("Rincón asignado")
        
        st.markdown("---")
        st.subheader("Actividades Post-Receso")
        m1 = st.text_input("Materia 1", value="Educación Física")
        m2 = st.text_input("Materia 2", placeholder="Ej. Educación Socioemocional")
        
        btn_previa = st.form_submit_button("👁️ GENERAR VISTA PREVIA")

    if btn_previa:
        if not tema or not nombre_ed:
            st.warning("⚠️ Falta el nombre del educador o el tema central.")
        else:
            datos = {"nivel": nivel, "grado": grado, "nombre_ed": nombre_ed, "nombre_eca": nombre_eca, 
                     "comunidad": comunidad, "fecha": str(fecha), "tema": tema, "rincon": rincon, "m1": m1, "m2": m2}
            
            c = generar_texto_educativo(datos)
            
            st.markdown("### 👁️ Vista Previa")
            st.success(f"**Planeación para {nivel} - Tema: {tema}**")
            
            col_preview_1, col_preview_2 = st.columns(2)
            with col_preview_1:
                st.write("**🌞 Rutina Grupal:**", c['inicio']['pase'])
                st.write("**Estación de Lenguaje:**", c['estaciones'][0]['d'])
            with col_preview_2:
                st.write("**🧠 Tutoreo Personalizado:**", c['tutoreo']['intro'])
                st.write("**📦 Producto Final:**", c['tutoreo']['producto'])

            # --- GENERAR PDF ---
            pdf = PDF()
            pdf.add_page()
            
            # Tabla de Datos
            pdf.chapter_title("I. DATOS DE IDENTIFICACIÓN")
            pdf.set_font('Arial', 'B', 10)
            filas = [["Educador", nombre_ed], ["ECA", nombre_eca], ["Nivel/Grado", f"{nivel} / {grado}"], ["Comunidad", comunidad], ["Fecha", str(fecha)], ["Rincón", rincon]]
            for k, v in filas:
                pdf.set_fill_color(240, 240, 240); pdf.cell(50, 8, k, 1, 0, 'L', True)
                pdf.set_font('Arial', '', 10); pdf.cell(0, 8, v, 1, 1); pdf.set_font('Arial', 'B', 10)
            
            pdf.ln(4); pdf.chapter_title("II. OBJETIVO GENERAL")
            pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, f"Desarrollar aprendizajes profundos y autonomía en los estudiantes de {nivel} mediante el diálogo y la exploración de '{tema}', vinculando el conocimiento científico con la realidad de la comunidad {comunidad}.")

            pdf.chapter_title("III. ACTIVIDADES GRUPALES (PARA CARTULINA)")
            pdf.multi_cell(0, 5, f"{c['inicio']['pase']}\n\n{c['inicio']['lectura']}\n\n{c['inicio']['bienvenida']}")

            pdf.chapter_title("IV. ESTACIONES DE TRABAJO")
            for est in c['estaciones']:
                pdf.set_font('Arial', 'B', 10); pdf.cell(0, 8, est['t'], 0, 1); pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, est['d']); pdf.ln(2)

            pdf.chapter_title(f"V. TUTOREO INDIVIDUAL: {tema.upper()}")
            pdf.multi_cell(0, 5, c['tutoreo']['intro'])
            for p in c['tutoreo']['pasos']: pdf.multi_cell(0, 5, f"- {p}")
            pdf.ln(2); pdf.set_font('Arial', 'B', 10); pdf.cell(0, 8, "Producto:", 0, 1); pdf.set_font('Arial', '', 10); pdf.multi_cell(0, 5, c['tutoreo']['producto'])

            pdf.chapter_title("VI. POST-RECESO")
            pdf.multi_cell(0, 6, f"1. {m1}: Dinámicas de movimiento coordinado para retomar la calma.\n2. {m2}: Reflexión sobre los aprendizajes logrados durante la jornada.")

            pdf_out = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 DESCARGAR PDF COMPLETO", data=pdf_out, file_name=f"Planeacion_{tema}.pdf", mime="application/pdf", use_container_width=True)
