import streamlit as st
from fpdf import FPDF
import unicodedata
import io
import datetime
from groq import Groq
from supabase import create_client, Client

# --- CONFIGURACIÓN DE CONEXIONES ---
# Nota: He mantenido tus credenciales de los chats anteriores para que funcione directo
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"
GROQ_KEY = "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"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# --- FUNCIONES DE LÓGICA ---
def llamar_ia_analisis_formativo(campo, alumno, nivel, indicadores):
    """Genera el análisis cualitativo para cada campo formativo."""
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Eres un experto pedagogo del Modelo ABCD. Redacta el análisis cualitativo para el reporte trimestral.
        CAMPO FORMATIVO: {campo}
        ALUMNO: {alumno} | NIVEL: {nivel}
        CONTEXTO: Lectura {indicadores['lectura']}, Escritura {indicadores['escritura']}.
        Redacta un párrafo profesional, sin asteriscos, describiendo avances y sugerencias.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return "Análisis generado manualmente por el Educador."

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REPORTE DE EVALUACION TRIMESTRAL'), 0, 1, 'C')
        self.ln(5)

    def tabla_datos(self, ec, com, alumno, niv, gra, periodo):
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        w, h = 95, 8
        self.cell(w, h, clean(f" EDUCADOR: {ec}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" COMUNIDAD: {com}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" ALUMNO: {alumno}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" TRIMESTRE: {periodo}"), 1, 1, 'L', True)
        self.cell(w, h, clean(f" NIVEL: {niv}"), 1, 0, 'L', True)
        self.cell(w, h, clean(f" GRADO: {gra}"), 1, 1, 'L', True)
        self.ln(10)

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.6 IA", layout="wide", page_icon="📊")

st.title("📊 Fase 0.6: Evaluación con IA Integrada")

with st.sidebar:
    st.header("📌 Identificación")
    nombre_ec = st.text_input("Nombre del Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Ej. Juan Perez")
    comunidad = st.text_input("Comunidad", "PARAJES")
    trimestre = st.selectbox("Trimestre", ["1er Trimestre", "2do Trimestre", "3er Trimestre"])
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.selectbox("Grado/Fase", ["1", "2", "3"])
    
    st.divider()
    st.header("📸 Evidencias")
    fotos = st.file_uploader("Subir imágenes (Máx. 2)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# --- INDICADORES ---
st.subheader("📖 Indicadores de Logro")
c_ind1, c_ind2 = st.columns(2)
ind_lectura = c_ind1.text_input("Indicador de Lectura (ej. 12A)", "12A")
ind_escritura = c_ind2.text_input("Indicador de Escritura (ej. 6)", "6")

st.divider()

# --- SECCIÓN DE ANÁLISIS / TRAYECTORIAS ---
eval_campos = {}
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]

st.subheader("🤖 Análisis Cualitativo (IA + Edición)")
st.info("💡 Haz clic en 'GENERAR ANÁLISIS CON IA' para redactar los campos automáticamente.")

if st.button("✨ GENERAR ANÁLISIS CON IA"):
    if not nombre_alumno:
        st.warning("⚠️ Ingresa el nombre del alumno primero.")
    else:
        with st.spinner("La IA está redactando las trayectorias..."):
            indicadores = {"lectura": ind_lectura, "escritura": ind_escritura}
            for campo in campos_nombres:
                st.session_state[f"eval_{campo}"] = llamar_ia_analisis_formativo(campo, nombre_alumno, nivel_edu, indicadores)
        st.success("✅ Análisis generados. Puedes editarlos abajo si es necesario.")

cols = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols[i % 2]:
        # Usamos session_state para que la IA pueda escribir en el text_area
        eval_campos[campo] = st.text_area(f"Análisis en {campo}:", 
                                          value=st.session_state.get(f"eval_{campo}", ""), 
                                          height=150, key=f"eval_{campo}")

# --- CALIFICACIONES DINÁMICAS ---
eval_detalles = []
if nivel_edu != "Preescolar":
    st.divider()
    st.subheader(f"🔢 Calificaciones ({nivel_edu} - {grado_edu}º)")
    
    if nivel_edu == "Primaria":
        materias = campos_nombres
    else:  # Secundaria
        materias_base = ["Español", "Matematicas", "Historia", "Geografia", "F. Civica y Etica", "Artes", "Ed. Fisica", "Ingles"]
        materias = ([ "Biologia" if grado_edu=="1" else "Fisica" if grado_edu=="2" else "Quimica"] + materias_base)

    for mat in materias:
        c1, c2 = st.columns([2, 1])
        nota = c1.number_input(f"Nota: {mat}", 5, 10, 8, key=f"n_{mat}")
        clave = c2.text_input(f"Clave", "T", max_chars=5, key=f"c_{mat}")
        eval_detalles.append({"concepto": mat, "nota": nota, "clave": clave})

# --- GENERACIÓN DEL PDF ---
if st.button("📊 GUARDAR EN NUBE Y DESCARGAR REPORTE", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ Falta el nombre del alumno.")
    else:
        try:
            # 1. Guardar en Supabase (Opcional pero recomendado)
            if supabase:
                data_supabase = {
                    "fecha": str(datetime.date.today()), "ec": nombre_ec, "alumno": nombre_alumno.upper(),
                    "nivel": nivel_edu, "trimestre": trimestre
                }
                supabase.table("reportes_trimestrales").insert(data_supabase).execute()

            # 2. PDF
            pdf = EvaluacionPDF()
            pdf.add_page()
            pdf.tabla_datos(nombre_ec, comunidad, nombre_alumno, nivel_edu, grado_edu, trimestre)

            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(95, 8, clean(f"INDICADOR LECTURA: {ind_lectura}"), 1, 0, 'L')
            pdf.cell(95, 8, clean(f"INDICADOR ESCRITURA: {ind_escritura}"), 1, 1, 'L')
            pdf.ln(5)

            for campo, texto in eval_campos.items():
                pdf.set_font('Helvetica', 'B', 10); pdf.cell(0, 7, clean(f"{campo}:"), 0, 1)
                pdf.set_font('Helvetica', '', 9)
                pdf.multi_cell(0, 5, clean(texto if texto else "Sin registro."))
                pdf.ln(2)

            # Tabla de notas
            if nivel_edu != "Preescolar":
                pdf.ln(5); pdf.set_font('Helvetica', 'B', 10); pdf.set_fill_color(200, 200, 200)
                pdf.cell(90, 10, clean(" ASIGNATURA"), 1, 0, 'C', True)
                pdf.cell(50, 10, clean(" NOTA"), 1, 0, 'C', True)
                pdf.cell(50, 10, clean(" CLAVE"), 1, 1, 'C', True)
                for it in eval_detalles:
                    pdf.set_font('Helvetica', '', 10)
                    pdf.cell(90, 8, clean(f" {it['concepto']}"), 1, 0, 'L')
                    pdf.cell(50, 8, str(it['nota']), 1, 0, 'C')
                    pdf.cell(50, 8, clean(it['clave']), 1, 1, 'C')

            if fotos:
                pdf.add_page()
                for i, f in enumerate(fotos[:2]):
                    pdf.image(io.BytesIO(f.getvalue()), x=(10 if i==0 else 110), y=30, w=90)

            pdf_out = pdf.output(dest='S')
            # Manejo de bytes para evitar el error anterior
            pdf_bytes = pdf_out.encode('latin-1') if isinstance(pdf_out, str) else pdf_out

            st.download_button("📥 DESCARGAR REPORTE PDF", pdf_bytes, f"Reporte_{nombre_alumno}.pdf", "application/pdf")
            st.success("✅ ¡Proceso completado!")
        except Exception as e:
            st.error(f"Error: {e}")
