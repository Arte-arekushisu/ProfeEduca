import streamlit as st
import datetime
import unicodedata
from groq import Groq
from supabase import create_client, Client
from fpdf import FPDF

# --- 1. CONFIGURACIÓN DE CONEXIONES (PON TUS DATOS AQUÍ) ---
SUPABASE_URL = "https://XYZ.supabase.co" # Cambia XYZ por tu ID real
SUPABASE_KEY = "sb_publishable_MXI7GvNreB5ZEhUJxQ2mXw_rzQpuyZ4"
GROQ_KEY = "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"

# Inicializar Supabase con manejo de errores
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# --- 2. FUNCIONES DE LÓGICA ---
def llamar_ia_redaccion_extensa(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Eres un asesor pedagógico experto. Redacta un TEXTO REFLEXIVO DIARIO extenso.
        ALUMNO: {datos['alumno']} | LOGROS: {datos['logros']} | RETOS: {datos['dificultades']}
        Usa lenguaje profesional, sin asteriscos y sé muy detallado.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content.replace("*", "")
    except Exception as e:
        return f"Nota: La IA no pudo redactar el texto automáticamente. Datos manuales: {datos['logros']}"

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('“', '"').replace('”', '"')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

class ReflexivoPDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(56, 189, 248)
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 15, clean('TEXTO REFLEXIVO DIARIO'), 0, 1, 'C')

# --- 3. INTERFAZ ---
st.set_page_config(page_title="Texto Reflexivo Diario", layout="wide")

# Estilo Oscuro
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .stTextArea textarea { background: #0f172a; color: #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 Texto Reflexivo Diario")

with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        nombre_ec = st.text_input("Educador", "AXEL REYES")
        alumno = st.text_input("Alumno")
    with col2:
        fecha = st.date_input("Fecha", datetime.date.today())
    
    logros = st.text_area("Logros")
    retos = st.text_area("Retos")
    submit = st.form_submit_button("🚀 GUARDAR Y DESCARGAR")

if submit:
    if not alumno:
        st.warning("Escribe el nombre del alumno.")
    else:
        with st.spinner("Procesando..."):
            # 1. Generar texto con IA
            datos = {"alumno": alumno, "logros": logros, "dificultades": retos, "nivel": "General", "emociones": "", "compromiso": ""}
            texto_ia = llamar_ia_redaccion_extensa(datos)
            
            # 2. Intentar guardar en Supabase (Si falla, la app sigue viva)
            try:
                if supabase:
                    supabase.table("reflexiones").insert({
                        "fecha": str(fecha), "ec": nombre_ec, "alumno": alumno.upper(), "texto_reflexivo": texto_ia
                    }).execute()
                    st.success("✅ Guardado en la nube.")
            except Exception as e:
                st.error(f"⚠️ No se pudo guardar en la nube (revisa tu URL), pero generaremos tu PDF.")

            # 3. Generar PDF (Independiente de la base de datos)
            pdf = ReflexivoPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, clean(f"Alumno: {alumno}"), 0, 1)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, clean(texto_ia))
            
            pdf_bytes = pdf.output(dest='S')
            
            st.markdown("### Vista Previa")
            st.info(texto_ia)
            
            st.download_button(
                label="📥 DESCARGAR PDF",
                data=bytes(pdf_bytes),
                file_name=f"Reflexion_{alumno}.pdf",
                mime="application/pdf"
            )
