import streamlit as st
import datetime
import unicodedata
from groq import Groq
from supabase import create_client, Client
from fpdf import FPDF

# --- CONFIGURACIÓN DE CONEXIONES ---
SUPABASE_URL = "https://pmqmqeukhufaqecbuodg.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtcW1xZXVraHVmYXFlY2J1b2RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NzY2MzksImV4cCI6MjA4NzA1MjYzOX0.Hr_3LlyI43zEoV4ZMn28gSKiBABK35VPTWip9rjC-zc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
GROQ_KEY = "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"

# --- FUNCIONES DE LÓGICA ---
def llamar_ia_redaccion_extensa(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"Redacta un TEXTO REFLEXIVO DIARIO profesional para {datos['alumno']}. Logros: {datos['logros']}. Retos: {datos['dificultades']}. Nivel: {datos['nivel']}. No uses asteriscos."
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content.replace("*", "")
    except:
        return f"Registro diario para {datos['alumno']}. Logros: {datos['logros']}."

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexivoPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 15, clean('TEXTO REFLEXIVO DIARIO'), 0, 1, 'C')

# --- INTERFAZ ---
st.set_page_config(page_title="Texto Reflexivo Diario", layout="wide")
st.markdown("<style>.stApp { background: #020617; color: #f8fafc; }</style>", unsafe_allow_html=True)
st.title("📝 Texto Reflexivo Diario")

with st.form("Form_Reflexivo_Diario"):
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno")
        comunidad = st.text_input("Comunidad", "PARAJES")
    with c2:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])
        fecha = st.date_input("Fecha", datetime.date.today())
    
    logros = st.text_area("🚀 Logros")
    dificultades = st.text_area("⚠️ Desafíos")
    emociones = st.text_area("🌈 Registro Social")
    compromiso = st.text_area("🤝 Compromiso")
    submit = st.form_submit_button("🔨 GUARDAR Y GENERAR")

if submit:
    if not nombre_alumno:
        st.error("Ingresa el nombre del alumno.")
    else:
        with st.spinner("Procesando..."):
            # 1. IA redacta
            texto_ia = llamar_ia_redaccion_extensa({"alumno": nombre_alumno, "logros": logros, "nivel": nivel, "dificultades": dificultades, "emociones": emociones, "compromiso": compromiso})
            
            # 2. Guardar en Supabase
            try:
                registro = {"fecha": str(fecha), "ec": nombre_ec, "alumno": nombre_alumno.upper(), "comunidad": comunidad, "nivel": nivel, "texto_reflexivo": texto_ia}
                supabase.table("reflexiones").insert(registro).execute()
                st.success("✅ Guardado en la nube correctamente.")
            except Exception as e:
                st.error(f"Error al guardar en la nube: {e}")

            # 3. Generación Segura de PDF
            try:
                pdf = ReflexivoPDF()
                pdf.add_page()
                pdf.set_font('Helvetica', 'B', 12)
                pdf.cell(0, 10, clean(f"ALUMNO: {nombre_alumno.upper()} - FECHA: {fecha}"), 0, 1)
                pdf.ln(5)
                pdf.set_font('Helvetica', '', 11)
                pdf.multi_cell(0, 7, clean(texto_ia))
                
                # Generamos los bytes del PDF
                pdf_output = pdf.output(dest='S')
                
                # Solo si se generó bien el PDF, mostramos el botón
                if pdf_output:
                    st.info(texto_ia)
                    st.download_button(
                        label="📥 DESCARGAR PDF",
                        data=bytes(pdf_output),
                        file_name=f"Reflexion_{nombre_alumno}.pdf",
                        mime="application/pdf"
                    )
            except Exception as pdf_err:
                st.error(f"Error al crear el archivo PDF: {pdf_err}")
