import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import datetime
from supabase import create_client, Client

# --- 1. CONEXIÓN AL MOTOR SUPABASE ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except:
    st.error("⚠️ Falta configurar las llaves de Supabase en los secretos de la página.")

# --- 2. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Profe.Educa", layout="wide", page_icon="🍎")
st.sidebar.title("🍎 Profe.Educa")
menu = st.sidebar.radio("Menú Principal", ["Inicio", "Planeación Semanal", "Texto Reflexivo Diario", "Evaluación Trimestral", "Admin"])

# --- 3. MÓDULO: PLANEACIÓN SEMANAL (CON GUARDADO Y WORD) ---
if menu == "Planeación Semanal":
    st.title("📋 Planeación de Trayectos")
    with st.form("form_p"):
        col1, col2 = st.columns(2)
        with col1:
            ec = st.text_input("Educador Comunitario")
        with col2:
            eca = st.text_input("E.C. de Acompañamiento")
        
        meta = st.text_area("Meta de la semana")
        actividades = st.text_area("Actividades principales")
        
        enviar = st.form_submit_button("Guardar y Generar Word")
        
        if enviar:
            # 1. Guardar en Supabase
            data_p = {
                "educador_nombre": ec,
                "ec_acompaniamiento": eca,
                "meta_semana": meta,
                "actividades": actividades
            }
            try:
                supabase.table("planeaciones").insert(data_p).execute()
                st.success("✅ Planeación guardada en la base de datos")
                
                # 2. Generar Word
                doc = Document()
                doc.add_heading('PLANEACIÓN CONAFE', 0)
                doc.add_paragraph(f"Fecha: {datetime.date.today()}")
                doc.add_paragraph(f"EC: {ec}")
                doc.add_paragraph(f"Acompañante: {eca}")
                doc.add_paragraph(f"Meta: {meta}")
                doc.add_paragraph(f"Actividades: {actividades}")
                
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                st.download_button("📥 Descargar Archivo Word", buffer, f"Planeacion_{ec}.docx")
            except Exception as e:
                st.error(f"Error al guardar: {e}")

# --- 4. MÓDULO: REFLEXIÓN DIARIA ---
elif menu == "Texto Reflexivo Diario":
    st.title("✍️ Registro de Relación Tutora")
    with st.form("registro"):
        alumno = st.text_input("Nombre del Alumno")
        notas = st.text_area("Anotaciones del día")
        if st.form_submit_button("Guardar en la Nube"):
            data = {"alumno_nombre": alumno, "contenido_reflexivo": notas}
            supabase.table("reflexiones").insert(data).execute()
            st.success("✅ Guardado permanentemente en Supabase")

# --- 5. MÓDULO: EVALUACIÓN / CONSULTA ---
elif menu == "Evaluación Trimestral":
    st.title("📊 Consulta y Evaluación")
    tab1, tab2 = st.tabs(["Buscar por Alumno", "Ver todas las Planeaciones"])
    
    with tab1:
        busqueda = st.text_input("Nombre del alumno para consultar historial")
        if st.button("Buscar Registros"):
            res = supabase.table("reflexiones").select("*").ilike("alumno_nombre", f"%{busqueda}%").execute()
            if res.data:
                st.write(f"Se encontraron {len(res.data)} registros:")
                df = pd.DataFrame(res.data)
                df['created_at'] = pd.to_datetime(df['created_at']).dt.date
                st.table(df[['created_at', 'alumno_nombre', 'contenido_reflexivo']])
            else:
                st.warning("No se encontraron registros para ese nombre.")

    with tab2:
        if st.button("Actualizar Lista de Planeaciones"):
            res_p = supabase.table("planeaciones").select("*").execute()
            if res_p.data:
                st.dataframe(pd.DataFrame(res_p.data))
            else:
                st.info("Aún no hay planeaciones guardadas.")
