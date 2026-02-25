import streamlit as st
import datetime
import unicodedata
from groq import Groq
from supabase import create_client, Client
from fpdf import FPDF

# --- CONFIGURACIÓN DE CONEXIONES ---
# Sustituye con tus credenciales de Supabase
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-anon-key-de-supabase"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

GROQ_KEY = "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"

# --- FUNCIONES DE LÓGICA ---
def llamar_ia_redaccion_extensa(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Eres un asesor pedagógico experto en el Modelo ABCD. 
        Tu tarea es redactar un TEXTO REFLEXIVO DIARIO extenso y profesional.
        ALUMNO: {datos['alumno']} | NIVEL: {datos['nivel']}
        LOGROS: {datos['logros']} | RETOS: {datos['dificultades']}
        SENTIMIENTOS: {datos['emociones']} | COMPROMISO: {datos['compromiso']}
        Redacta en tercera persona, con un tono motivador y pedagógico. Mínimo 3 párrafos. No uses asteriscos.
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
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 15, clean('TEXTO REFLEXIVO DIARIO - PROFEEDUCA'), 0, 1, 'C')
        self.ln(5)

# --- INTERFAZ Y DISEÑO OSCURO ---
st.set_page_config(page_title="Texto Reflexivo Diario", layout="wide", page_icon="📝")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1e293b 0%, #020617 100%); 
        color: #f8fafc; 
    }
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: #0f172a;
        color: #38bdf8;
        border: 1px solid #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 style="color:#38bdf8;">📝 Texto Reflexivo Diario</h1>', unsafe_allow_html=True)
st.write("Registra el avance diario del alumno. La información se guardará en la nube y podrás descargar el PDF.")

with st.form("Form_Reflexivo_Diario"):
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Escribe el nombre aquí...")
        comunidad = st.text_input("Comunidad", "PARAJES")
    with c2:
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])
        fecha = st.date_input("Fecha del registro", datetime.date.today())
    
    st.divider()
    logros = st.text_area("🚀 Logros y aprendizajes del día", height=100)
    dificultades = st.text_area("⚠️ Desafíos encontrados", height=100)
    emociones = st.text_area("🌈 Registro Social y Emocional", height=100)
    compromiso = st.text_area("🤝 Compromiso para la siguiente sesión", height=100)

    submit = st.form_submit_button("🔨 GUARDAR REGISTRO Y GENERAR REPORTE")

if submit:
    if not nombre_alumno:
        st.error("Por favor, ingresa el nombre del alumno.")
    else:
        with st.spinner("La IA está analizando los datos..."):
            # 1. Redacción de IA
            info_ia = {"alumno": nombre_alumno, "logros": logros, "nivel": nivel, 
                       "dificultades": dificultades, "emociones": emociones, "compromiso": compromiso}
            texto_reflexivo = llamar_ia_redaccion_extensa(info_ia)
            
            # 2. Guardado en Supabase
            registro = {
                "fecha": str(fecha),
                "ec": nombre_ec,
                "alumno": nombre_alumno.upper(),
                "comunidad": comunidad,
                "nivel": nivel,
                "texto_reflexivo": texto_reflexivo
            }
            
            try:
                supabase.table("reflexiones").insert(registro).execute()
                st.success(f"✅ ¡Registro de {nombre_alumno} guardado en Supabase!")
                
                st.markdown("### Vista Previa de la Reflexión:")
                st.info(texto_reflexivo)
                
                # 3. Generación de PDF
                pdf = ReflexivoPDF()
                pdf.add_page()
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_fill_color(240, 249, 255)
                pdf.cell(95, 8, clean(f" ALUMNO: {nombre_alumno.upper()}"), 1, 0, 'L', True)
                pdf.cell(95, 8, clean(f" FECHA: {fecha}"), 1, 1, 'L', True)
                pdf.ln(5)
                pdf.set_font('Helvetica', '', 11)
                pdf.multi_cell(0, 7, clean(texto_reflexivo))
                
                pdf_bytes = pdf.output(dest='S')
                st.download_button(
                    label="📥 DESCARGAR TEXTO REFLEXIVO (PDF)",
                    data=bytes(pdf_bytes),
                    file_name=f"Reflexion_Diaria_{nombre_alumno}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"❌ Error al sincronizar con la nube: {e}")
