import streamlit as st
from fpdf import FPDF
import unicodedata
import io
from datetime import date

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PROFEEDUCA - Fase 0.8", layout="wide", page_icon="📊")

# --- FUNCIONES DE LIMPIEZA PARA PDF ---
def clean(txt):
    if not txt: return ""
    txt = "".join(c for c in unicodedata.normalize('NFD', str(txt)) if unicodedata.category(c) != 'Mn')
    txt = txt.replace('ñ', 'n').replace('Ñ', 'N')
    return txt

# --- CLASES DE PDF ---
class EvaluacionPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102) 
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 15, clean('REPORTE DE EVALUACION TRIMESTRAL'), 0, 1, 'C')
        self.ln(5)

class FacturaPDF(FPDF):
    def header(self):
        self.set_fill_color(33, 47, 61)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 20, clean('COMPROBANTE DE PAGO - PROFEEDUCA'), 0, 1, 'C')
        self.ln(10)

# --- INTERFAZ PRINCIPAL ---
st.title("📊 PROFEEDUCA: Gestión Integral")

# Pestañas para organizar el flujo
tab_eval, tab_fact = st.tabs(["📝 Evaluación Trimestral", "💳 Facturación y Pagos"])

# --- CONTENIDO DE EVALUACIONES ---
with tab_eval:
    with st.sidebar:
        st.header("📌 Identificación")
        nombre_ec = st.text_input("Educador", "AXEL REYES")
        nombre_alumno = st.text_input("Alumno", placeholder="Ej. Tania")
        nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
        grado_edu = st.selectbox("Grado", ["1", "2", "3", "4", "5", "6"])
        
        st.divider()
        st.markdown("### 🆘 AYUDA")
        with st.expander("🚨 BOTÓN SOS"):
            st.link_button("📲 Soporte WhatsApp", "https://wa.me/tu_numero")

    st.subheader("Análisis por Campo Formativo")
    campos = ["Lenguajes", "Saberes y P.C.", "Etica, N. y S.", "De lo Humano y lo Com."]
    eval_textos = {}
    
    cols = st.columns(2)
    for i, campo in enumerate(campos):
        with cols[i % 2]:
            eval_textos[campo] = st.text_area(f"Análisis de {campo}:", height=100)

    if st.button("🚀 GENERAR REPORTE EDUCATIVO"):
        st.success("¡Generando PDF de Evaluación...!")

# --- CONTENIDO DE FACTURACIÓN ---
with tab_fact:
    st.header("🧾 Generación de Comprobantes")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        razon_social = st.text_input("Nombre / Razón Social", placeholder="Ej. Asociación de Padres")
        rfc_dni = st.text_input("RFC o Identificación")
    
    with col_f2:
        monto = st.number_input("Monto Total ($)", min_value=0.0, format="%.2f")
        metodo = st.selectbox("Método de Pago", ["Transferencia", "Efectivo", "Depósito"])

    concepto = st.text_area("Concepto del pago", "Aportación para materiales educativos trimestre 2.")

    if st.button("📝 EMITIR COMPROBANTE DE PAGO"):
        if not razon_social or monto <= 0:
            st.error("⚠️ Datos incompletos para facturar.")
        else:
            f_pdf = FacturaPDF()
            f_pdf.add_page()
            f_pdf.set_font('Helvetica', 'B', 12)
            f_pdf.cell(0, 10, clean(f"RECEPTOR: {razon_social}"), 0, 1)
            f_pdf.cell(0, 10, clean(f"RFC/ID: {rfc_dni}"), 0, 1)
            f_pdf.ln(10)
            
            # Tabla de Cobro
            f_pdf.set_fill_color(33, 47, 61); f_pdf.set_text_color(255, 255, 255)
            f_pdf.cell(140, 10, clean(" CONCEPTO"), 1, 0, 'L', True)
            f_pdf.cell(50, 10, clean(" TOTAL"), 1, 1, 'C', True)
            
            f_pdf.set_text_color(0, 0, 0); f_pdf.set_font('Helvetica', '', 11)
            f_pdf.cell(140, 15, clean(concepto), 1, 0, 'L')
            f_pdf.cell(50, 15, f"${monto:,.2f}", 1, 1, 'C')
            
            st.download_button("📥 DESCARGAR FACTURA", bytes(f_pdf.output()), f"Factura_{razon_social}.pdf")
            st.balloons()
