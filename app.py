import streamlit as st
import datetime
import unicodedata
from groq import Groq
from supabase import create_client, Client

# --- CONFIGURACIÓN DE SUPABASE ---
# Reemplaza con tus credenciales reales de Supabase
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-anon-key-de-supabase"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Memoria Pedagógica", layout="wide", page_icon="🗄️")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1e293b 0%, #020617 100%); color: #f8fafc; }
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: #0f172a; color: #38bdf8; border: 1px solid #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

GROQ_KEY = "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"

def llamar_ia_redaccion_extensa(datos):
    try:
        client = Groq(api_key=GROQ_KEY)
        prompt = f"""
        Como experto en el Modelo ABCD, redacta una CRÓNICA REFLEXIVA EXTENSA.
        ALUMNO: {datos['alumno']} | NIVEL: {datos['nivel']}
        LOGROS: {datos['logros']} | RETOS: {datos['dificultades']}
        SENTIMIENTOS: {datos['emociones']} | COMPROMISO: {datos['compromiso']}
        
        Redacta de forma profesional y extensa para registro histórico. No uses asteriscos.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return completion.choices[0].message.content.replace("*", "")
    except Exception as e:
        return f"Error IA: {str(e)}"

# --- INTERFAZ ---
st.markdown('<h1 style="color:#38bdf8;">🗄️ Registro en Memoria Pedagógica (Supabase)</h1>', unsafe_allow_html=True)
st.write("Las reflexiones se guardarán para que la IA las use en la evaluación trimestral.")

with st.form("Form_Reflexivo_Supabase"):
    c1, c2 = st.columns(2)
    with c1:
        nombre_ec = st.text_input("Nombre del EC", "AXEL REYES")
        nombre_alumno = st.text_input("Nombre del Alumno")
    with c2:
        comunidad = st.text_input("Comunidad", "PARAJES")
        nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Baja", "Primaria Alta", "Secundaria"])
    
    fecha = st.date_input("Día del registro", datetime.date.today())
    st.divider()
    
    logros = st.text_area("🚀 Logros y aprendizajes")
    dificultades = st.text_area("⚠️ Retos y dificultades")
    emociones = st.text_area("🌈 Registro Social/Emociones")
    compromiso = st.text_area("🤝 Compromisos")

    submit = st.form_submit_button("🚀 GUARDAR EN MEMORIA HISTÓRICA")

if submit:
    if not nombre_alumno:
        st.error("Por favor, escribe el nombre del alumno.")
    else:
        with st.spinner("Redactando y subiendo a la nube..."):
            # 1. Generar la redacción extensa con IA
            info_ia = {
                "alumno": nombre_alumno, "logros": logros, "nivel": nivel,
                "dificultades": dificultades, "emociones": emociones, "compromiso": compromiso
            }
            texto_extenso = llamar_ia_redaccion_extensa(info_ia)
            
            # 2. Preparar datos para Supabase
            # Asegúrate de que tu tabla en Supabase se llame 'reflexiones'
            data_to_save = {
                "fecha": str(fecha),
                "ec": nombre_ec,
                "alumno": nombre_alumno.upper(),
                "comunidad": comunidad,
                "nivel": nivel,
                "texto_reflexivo": texto_extenso,
                "puntos_clave": f"Logros: {logros} | Retos: {dificultades}"
            }
            
            # 3. Insertar en Supabase
            try:
                response = supabase.table("reflexiones").insert(data_to_save).execute()
                st.success(f"✅ ¡Registro guardado con éxito en Supabase para {nombre_alumno}!")
                st.markdown("### Redacción guardada:")
                st.info(texto_extenso)
            except Exception as e:
                st.error(f"❌ Error al guardar en Supabase: {str(e)}")
