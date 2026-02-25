import streamlit as st
import datetime
import unicodedata
from groq import Groq
from supabase import create_client, Client
from fpdf import FPDF

# --- CONFIGURACIÓN DE CONEXIONES ---
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-anon-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

GROQ_KEY = "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"

# --- FUNCIONES DE APOYO ---
def llamar_ia_redaccion_extensa(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Eres un asesor pedagógico del Modelo ABCD. Redacta una CRÓNICA REFLEXIVA EXTENSA.
        ALUMNO: {datos['alumno']} | NIVEL: {datos['nivel']}
        LOGROS: {datos['logros']} | RETOS: {datos['dificultades']}
        SENTIMIENTOS: {datos['emociones']} | COMPROMISO: {datos['compromiso']}
        Redacta de forma profesional, extensa y sin usar asteriscos (*).
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content.replace("*", "")
    except Exception as e:
        return f"Error en redacción: {str(e)}"

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexivoPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('INFORME PEDAGOGICO REFLEXIVO (MEMORIA DIGITAL)'), 0, 1, 'C')
        self.ln(5)

# --- INTERFAZ ---
st.set_page_config(page_title="PROFEEDUCA - Registro Dual", layout="wide")

st.markdown('<h1 style="color:#38bdf8;">📝 Registro de Reflexión: Nube y PDF</h1>', unsafe_allow_html=True)

with st.form("Form_Dual"):
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno")
        comunidad = st.text_input("Comunidad", "PARAJES")
    with c2:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])
        fecha = st.date_input("Fecha", datetime.date.today())
    
    st.divider()
    logros = st.text_area("🚀 Logros")
    dificultades = st.text_area("⚠️ Retos")
    emociones = st.text_area("🌈 Emociones (Registro Social)")
    compromiso = st.text_area("🤝 Compromisos")

    submit = st.form_submit_button("🚀 PROCESAR REGISTRO")

if submit:
    if not nombre_alumno:
        st.error("Ingresa el nombre del alumno.")
    else:
        with st.spinner("Sincronizando con Supabase y redactando reporte..."):
            # 1. IA redacta
            info_ia = {"alumno": nombre_alumno, "logros": logros, "nivel": nivel, "dificultades": dificultades, "emociones": emociones, "compromiso": compromiso}
            cronica_final = llamar_ia_redaccion_extensa(info_ia)
            
            # 2. Guardar en Supabase
            registro = {
                "fecha": str(fecha), "ec": nombre_ec, "alumno": nombre_alumno.upper(),
                "comunidad": comunidad, "nivel": nivel, "texto_reflexivo": cronica_final
            }
            try:
                supabase.table("reflexiones").insert(registro).execute()
                st.success("✅ Datos guardados en Supabase.")
                
                # 3. Preparar PDF para descarga inmediata
                pdf = ReflexivoPDF()
                pdf.add_page()
                # Tabla de datos en PDF
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(95, 8, clean(f" ALUMNO: {nombre_alumno.upper()}"), 1, 0)
                pdf.cell(95, 8, clean(f" FECHA: {fecha}"), 1, 1)
                pdf.ln(5)
                pdf.set_font('Helvetica', '', 11)
                pdf.multi_cell(0, 7, clean(cronica_final))
                
                pdf_output = pdf.output(dest='S')
                
                st.info("La redacción ha sido procesada. Puedes descargarla abajo:")
                st.download_button(
                    label="📥 DESCARGAR PDF PARA EXPEDIENTE",
                    data=bytes(pdf_output),
                    file_name=f"Reflexion_{nombre_alumno}_{fecha}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Error al conectar con la base de datos: {e}")
