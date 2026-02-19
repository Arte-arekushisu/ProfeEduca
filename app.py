import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Profe.Educa Premium", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stSidebar { background-color: #1a1c24; }
    h1, h2, h3 { color: #00d4ff !important; }
    .welcome-box {
        padding: 30px; border-radius: 15px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #00d4ff; margin-bottom: 25px;
    }
    .price-card {
        padding: 20px; border-radius: 10px; background: #1a1c24;
        border: 1px solid #00d4ff; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE GENERACIÓN DE WORD PROFESIONAL
def crear_encabezado_oficial(doc, d, titulo, logo1=None, logo2=None):
    # Tabla para logos y título
    tab_header = doc.add_table(rows=1, cols=3)
    tab_header.width = Inches(6)
    
    if logo1:
        img1 = Image.open(logo1)
        img1_path = "logo1.png"
        img1.save(img1_path)
        tab_header.cell(0, 0).paragraphs[0].add_run().add_picture(img1_path, width=Inches(1))
    
    run_titulo = tab_header.cell(0, 1).paragraphs[0].add_run(titulo)
    run_titulo.bold = True
    run_titulo.font.size = Pt(14)
    tab_header.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    if logo2:
        img2 = Image.open(logo2)
        img2_path = "logo2.png"
        img2.save(img2_path)
        tab_header.cell(0, 2).paragraphs[0].add_run().add_picture(img2_path, width=Inches(1))

    # Datos Generales
    doc.add_paragraph(f"\nComunidad: {d['comunidad']} | EC: {d['nombre']} | ECA: {d['eca']}")
    doc.add_paragraph(f"Nivel: {d['nivel']} | Fecha: {d['fecha']}")
    doc.add_paragraph("-" * 80)

def agregar_tabla_planeacion(doc, contenido_ia):
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdrs = table.rows[0].cells
    for i, txt in enumerate(['Actividad', 'Desarrollo/Instrucción', 'Materiales', 'Tiempo']):
        hdrs[i].text = txt
        hdrs[i].paragraphs[0].runs[0].bold = True

    lineas = contenido_ia.replace("**", "").split('\n')
    for linea in lineas:
        if '|' in linea:
            partes = linea.split('|')
            if len(partes) >= 4:
                row = table.add_row().cells
                for i in range(4): row[i].text = partes[i].strip()

def agregar_firmas(doc, p1="Educador Comunitario", p2="Padre de Familia / APEC"):
    doc.add_paragraph("\n\n\n")
    f_table = doc.add_table(rows=1, cols=2)
    f_table.cell(0, 0).text = f"__________________________\nFirma: {p1}"
    f_table.cell(0, 1).text = f"__________________________\nFirma: {p2}"

# 3. INTERFAZ Y NAVEGACIÓN
with st.sidebar:
    st.title("🍎 Menú Profe.Educa")
    opcion = st.radio("Sección:", ["🏠 Inicio y Registro", "📅 Planeación Semanal", "✍️ Reflexión Diaria", "📊 Evaluación Trimestral", "🆘 Centro de Ayuda"])
    st.divider()
    comunidad = st.text_input("Comunidad")
    nombre_ec = st.text_input("Educador")
    eca = st.text_input("ECA")
    nivel = st.selectbox("Nivel", ["Preescolar", "Primaria Multigrado", "Secundaria Multigrado"])
    fecha = st.date_input("Fecha")
    st.divider()
    logo1 = st.file_uploader("Logo Izquierdo", type=["png", "jpg"])
    logo2 = st.file_uploader("Logo Derecho", type=["png", "jpg"])

datos_id = {"comunidad": comunidad, "nombre": nombre_ec, "eca": eca, "nivel": nivel, "fecha": str(fecha)}

# 4. LÓGICA DE SECCIONES
if opcion == "🏠 Inicio y Registro":
    st.markdown("""
    <div class='welcome-box'>
        <h1>"Educar no es dar carrera para vivir, sino templar el alma para las dificultades de la vida."</h1>
        <p>Bienvenido, Educador. Esta herramienta ha sido diseñada para devolverte lo más valioso: tu tiempo. Genera documentos oficiales con precisión pedagógica.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Selecciona tu Plan de Trabajo")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='price-card'><h3>Prueba</h3><p>7 Días Gratis</p><p>Acceso Total</p></div>", unsafe_allow_html=True)
        st.button("Empezar Gratis", key="free")
    with c2:
        st.markdown("<div class='price-card'><h3>Mensual</h3><p>$699 MXN</p><p>Planeación + Reflexión</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Mensual", key="month")
    with c3:
        st.markdown("<div class='price-card'><h3>Anual 🌟</h3><p>$6,400 MXN</p><p>Todo + Soporte IA 24/7</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Anual", key="year")

elif opcion == "📅 Planeación Semanal":
    st.header("Generador de Planeación Limpia")
    tema = st.text_input("Tema de Interés Principal")
    obj = st.text_area("Objetivo propuesto (o deja que la IA lo proponga)")
    materias = st.text_input("Materias Post-Receso (hasta 2 por hora)", placeholder="Ej: Matemáticas y Ciencias")
    
    if st.button("Crear Planeación en Word"):
        prompt = f"Genera planeación CONAFE para {tema}. Mañana: Bienvenida, Pase Lista, Regalo Lectura, Relación Tutora en Estaciones. Tarde: {materias} con actividades técnicas. Formato tabla con '|'."
        # Lógica de IA y descarga (similar a funciones anteriores pero con crear_encabezado_oficial)
        st.info("Generando tabla estructurada para Word...")

elif opcion == "✍️ Reflexión Diaria":
    st.header("Reflexión Diaria por Alumno")
    alumno = st.text_input("Nombre del Alumno")
    trayectoria = st.text_input("Trayectoria seguida")
    notas = st.text_area("Observaciones del día")
    
    if st.button("Guardar y Generar Word"):
        st.success(f"Reflexión de {alumno} lista para impresión.")

elif opcion == "📊 Evaluación Trimestral":
    st.header("Evaluación Trimestral (Campos Formativos)")
    alumno_ev = st.text_input("Buscar Alumno")
    proyecto = st.text_input("Nombre del Proyecto Comunitario")
    
    st.subheader("Calificaciones y Niveles")
    colA, colB, colC = st.columns(3)
    with colA:
        cal_leng = st.number_input("Lenguajes", 5, 10)
        cal_saberes = st.number_input("Saberes y PC", 5, 10)
    with colB:
        cal_etica = st.number_input("Ética, Nat y Soc", 5, 10)
        cal_humano = st.number_input("De lo Humano", 5, 10)
    with colC:
        lectura = st.selectbox("Nivel Lectura", ["Requiere Apoyo", "En Desarrollo", "Nivel Esperado"])
        escritura = st.selectbox("Nivel Escritura", ["Requiere Apoyo", "En Desarrollo", "Nivel Esperado"])

    if st.button("Generar Evaluación Oficial (Word)"):
        st.info("Redactando evaluación basada en los campos de la NEM y reflexiones previas...")

elif opcion == "🆘 Centro de Ayuda":
    st.header("Centro de Ayuda y Soporte")
    st.write("Si tienes cuenta **Anual**, nuestra IA te atiende 24/7. Si no puede resolverlo, te contactará con el Profe personalmente.")
    st.text_area("Describe tu duda:")
    st.button("Enviar a Soporte Técnico")
