import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
from groq import Groq
import io
import re

# --- 1. CONFIGURACIÓN ---
GEMINI_KEY = "AIzaSyBGZ7-k5lvJHp-CaX7ruwG90jEqbvC0zXM"
GROQ_KEY = "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"

st.set_page_config(page_title="ProfeEduca ABCD Pro", page_icon="🍎", layout="wide")

# Estilos Visuales
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); color: #f8fafc; }
    .brand-header { font-size: 2.5rem; font-weight: 900; color: #38bdf8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE INTELIGENCIA ---
def llamar_ia(prompt):
    try:
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un experto pedagogo. Generas planeaciones extensas, profesionales, sin usar asteriscos (*) y con horarios detallados."},
                      {"role": "user", "content": prompt}],
            temperature=0.6, max_tokens=4000
        )
        texto = completion.choices[0].message.content
        # Limpieza agresiva de asteriscos
        return texto.replace("*", ""), "Groq"
    except:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
            texto = res.json()['candidates'][0]['content']['parts'][0]['text']
            return texto.replace("*", ""), "Gemini"
        except: return None, None

# --- 3. GENERACIÓN DE PDF ---
def generar_pdf(datos, contenido_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="PLANEACIÓN PROFESIONAL ABCD", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 8, txt=f"Vigencia: {datos['duracion']}", ln=True, align='C')
    pdf.ln(5)
    
    # Cuadro de datos B/N Profesional
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(95, 8, txt=f" E.C.: {datos['ec']}", border=1, fill=True)
    pdf.cell(95, 8, txt=f" E.C.A.: {datos['eca']}", border=1, fill=True, ln=True)
    pdf.cell(95, 8, txt=f" Comunidad: {datos['comunidad']}", border=1)
    pdf.cell(95, 8, txt=f" Nivel: {datos['nivel']} ({datos['grados']})", border=1, ln=True)
    pdf.cell(95, 8, txt=f" Rincón: {datos['rincon']}", border=1)
    pdf.cell(95, 8, txt=f" Fecha de Inicio: {datos['fecha']}", border=1, ln=True)
    pdf.ln(10)

    # Contenido (Sin asteriscos)
    pdf.set_font("Arial", size=11)
    texto_limpio = contenido_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ ---
st.markdown('<div class="brand-header">📏 ProfeEduca ABCD Pro ✏️</div>', unsafe_allow_html=True)

with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        ec = st.text_input("Nombre E.C.")
        eca = st.text_input("Nombre E.C.A.")
        comu = st.text_input("Comunidad")
        nivel = st.selectbox("Nivel Educativo", ["Preescolar", "Primaria", "Secundaria", "Multigrado"])
        duracion = st.selectbox("Periodo de Planeación (Plan de Pago)", ["1 Día", "1 Semana Hábil", "2 Semanas Hábiles"])
    with c2:
        grados = st.text_input("Grado(s)")
        inst = st.selectbox("Institución", ["SEP", "CET", "Privada", "Otros"])
        rincon = st.text_input("Rincón / Tema de Interés")
        fecha_gen = datetime.now().strftime("%d/%m/%Y")

    tema_tutora = st.text_area("Desarrollo Extenso del Tema de Interés (Relación Tutora)")
    post_receso_req = st.text_area("Actividades Post-Receso (Menciona si deseas materias específicas por día)")

    boton_generar = st.form_submit_button("🚀 Generar Planeación Semanal")

if boton_generar:
    if not ec or not tema_tutora:
        st.error("Por favor completa los campos obligatorios.")
    else:
        with st.spinner(f"Construyendo planeación extensa para {duracion}..."):
            prompt_maestro = f"""
            Genera una PLANEACIÓN PROFESIONAL ABCD para {duracion}. 
            REGLA CRÍTICA: NO USES ASTERISCOS (*) EN NINGUNA PARTE DEL TEXTO.
            
            1. HORARIO ESCOLAR (8:00 AM - 2:00 PM):
               - Detalla los minutos exactos para cada momento: Bienvenida (15 min), Pase de lista (10 min), Regalo de lectura (20 min), Relación Tutora (120 min), Receso (30 min), Estaciones (90 min), Cierre (30 min).
            
            2. RELACIÓN TUTORA (EXTENSA):
               - Desarrolla a profundidad el tema: {tema_tutora}. Incluye bibliografía real, fundamentos pedagógicos y 5 PREGUNTAS DETONANTES potentes.
            
            3. CRONOGRAMA SEMANAL:
               - Si la duración es de una semana o más, describe las actividades de LUNES A VIERNES.
               - El bloque POST-RECESO debe cambiar cada día (Lunes: {post_receso_req} o sugerencia de Artes, Martes: Educación Física, Miércoles: Vida Saludable, etc.).
            
            4. 4 ESTACIONES AUTÓNOMAS:
               - Una para cada Campo Formativo. Con nombres creativos, uso de MATERIAL RECICLADO y pasos detallados para que el alumno trabaje sin ayuda del maestro.
            
            Nota: Mantén un lenguaje formal y profesional. Elimina cualquier mención a CONAFE.
            """
            
            respuesta_ia, motor = llamar_ia(prompt_maestro)
            
            if respuesta_ia:
                st.success(f"Planeación generada con éxito.")
                st.write(respuesta_ia)
                
                datos_doc = {"ec": ec, "eca": eca, "comunidad": comu, "nivel": nivel, 
                             "grados": grados, "inst": inst, "rincon": rincon, 
                             "fecha": fecha_gen, "duracion": duracion}
                
                pdf_output = generar_pdf(datos_doc, respuesta_ia)
                st.download_button(label="📥 Descargar PDF (Sin Asteriscos)", data=pdf_output,
                                   file_name=f"Planeacion_Semanal_{ec}.pdf", mime="application/pdf")
