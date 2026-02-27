import streamlit as st
from fpdf import FPDF
import unicodedata
import io
import datetime
from groq import Groq

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.8.1 IA", layout="wide", page_icon="🛡️")
GROQ_KEY = "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"

# --- MOTOR DE IA ---
def llamar_ia(prompt, temp=0.7):
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp, max_tokens=1000
        )
        return completion.choices[0].message.content.replace("*", "")
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N').replace('¿', '').replace('¡', '')
    return txt.encode('latin-1', 'ignore').decode('latin-1')

# --- INTERFAZ TOTAL DARK ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .error-box { padding: 10px; background-color: #450a0a; border: 1px solid #f87171; border-radius: 5px; color: #fca5a5; margin-bottom: 10px; }
    .stTextArea textarea { background-color: #1e293b !important; color: #38bdf8 !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CON SIMULADOR DE ERRORES ---
with st.sidebar:
    st.header("⚙️ Configuración")
    nombre_ec = st.text_input("Educador", "AXEL REYES")
    nombre_alumno = st.text_input("Alumno")
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    
    st.divider()
    st.header("🛡️ CENTRO DE DIAGNÓSTICO")
    modo_error = st.toggle("Simular Errores de Redacción")
    
    if st.button("🆘 ANALIZAR MI REPORTE (IA SOS)"):
        if not nombre_alumno:
            st.error("Error: No has puesto el nombre del alumno.")
        else:
            with st.spinner("IA analizando calidad pedagógica..."):
                # La IA revisa lo que el usuario ha escrito hasta ahora
                contexto_actual = f"Alumno: {nombre_alumno}. Nivel: {nivel_edu}. Campos: {st.session_state.get('t_Lenguajes', 'Vacío')}"
                diagnostico = llamar_ia(f"Actúa como supervisor. Analiza si este reporte es profesional o está incompleto: {contexto_actual}. Da consejos breves.")
                st.info(diagnostico)

st.title("🛡️ PROFEEDUCA: Fase IA Auto-Correctora")

# --- LÓGICA DE GENERACIÓN ---
if st.button("✨ GENERAR REPORTE MAESTRO", use_container_width=True):
    if not nombre_alumno:
        st.error("⚠️ El sistema no puede crear una historia sin un protagonista (Falta nombre).")
    else:
        with st.spinner("IA redactando con estilo reflexivo..."):
            campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
            for c in campos:
                st.session_state[f"t_{c}"] = llamar_ia(f"Escribe una reflexión de cuento pedagógico para {nombre_alumno} en {c}. Nivel {nivel_edu}.")
            st.session_state["resumen_ia"] = llamar_ia(f"Haz una crónica emotiva del periodo de {nombre_alumno}.")

# --- CAMPOS FORMATIVOS ---
campos_nombres = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
eval_campos = {}

cols = st.columns(2)
for i, campo in enumerate(campos_nombres):
    with cols[i % 2]:
        # SIMULACIÓN DE ERROR VISUAL
        if modo_error and not st.session_state.get(f"t_{campo}"):
            st.markdown(f'<div class="error-box">⚠️ El campo {campo} está vacío o es muy corto.</div>', unsafe_allow_html=True)
            
        eval_campos[campo] = st.text_area(f"Campo: {campo}", value=st.session_state.get(f"t_{campo}", ""), height=120)

st.divider()
resumen_txt = st.text_area("📝 Resumen General", value=st.session_state.get("resumen_ia", ""), height=150)

# --- BOTÓN DE DESCARGA CON PROTECCIÓN ---
if st.button("🚀 GENERAR PDF FINAL"):
    # VALIDACIÓN ANTES DE GENERAR
    errores = []
    if not nombre_alumno: errores.append("Falta el nombre del alumno.")
    if len(resumen_txt) < 10: errores.append("El resumen es demasiado corto para un reporte profesional.")
    
    if errores:
        st.error("🛑 BLOQUEO DE SEGURIDAD:")
        for err in errores: st.write(f"- {err}")
        if st.button("🤖 IA: CORREGIR ERRORES AUTOMÁTICAMENTE"):
            st.session_state["resumen_ia"] = llamar_ia(f"Amplía este resumen de forma profesional y emotiva: {resumen_txt}")
            st.rerun()
    else:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, clean("REPORTE DE APRENDIZAJE PROFESIONAL"), 0, 1, 'C')
            pdf.ln(10)
            pdf.set_font("Helvetica", "", 12)
            pdf.multi_cell(0, 10, clean(f"Alumno: {nombre_alumno}\n\nResumen:\n{resumen_txt}"))
            
            st.download_button("📥 DESCARGAR PDF CORREGIDO", pdf.output(), f"Reporte_{nombre_alumno}.pdf", "application/pdf")
            st.success("¡PDF generado sin errores técnicos!")
        except Exception as e:
            st.error(f"Fallo técnico: {e}. Intenta usar el botón SOS.")
