import streamlit as st
import os
import glob
from datetime import datetime
import json

st.set_page_config(page_title="Monitor de Calidad y Semáforo", layout="wide", page_icon="🩺")
st.title("🩺 Monitor de Calidad y Sincronía del Sistema")
st.markdown("Auditoría en tiempo real para verificar si las bases de datos en caché están alineadas con los archivos físicos y la doctrina oficial (RAG).")

def get_mtime(path):
    if os.path.exists(path):
        return os.path.getmtime(path)
    return 0

CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'excel_input': 'R40 AAPP - FINAL - Marzo 13.xlsx', 'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

config = load_config()

# 1. Rutas
input_path = config.get('excel_input', '')
output_path = config.get('excel_output', '')
kb_path = "Base de Conocimiento"
guia_path = "guia_estrategica_cra.md"

# 2. Tiempos
t_input = get_mtime(input_path)
t_output = get_mtime(output_path)
t_guia = get_mtime(guia_path)

kb_pdfs = glob.glob(os.path.join(kb_path, "*.pdf"))
t_kb_max = max([get_mtime(pdf) for pdf in kb_pdfs]) if kb_pdfs else 0

# 3. Lógica de validación
needs_nlp = False
needs_export = False
warnings = []
success = []

# Validar Existencia
if not os.path.exists(input_path):
    warnings.append(f"Falta Matriz de Entrada: {input_path}")
    needs_nlp = True
else:
    success.append("Matriz Cruda de Entrada detectada.")

if not os.path.exists(guia_path):
    warnings.append("Falta Guía Estratégica RAG (Se debe Ejecutar Motor NLP).")
    needs_nlp = True
else:
    success.append("Guía Estratégica Base detectada.")

if not os.path.exists(output_path):
    warnings.append(f"Falta Excel de Salida: {output_path} (Se debe Generar Excel).")
    needs_export = True
else:
    success.append("Excel Multi-Dimensional de Resultados (Salida) detectado.")

# Validar Sincronía NLP vs Input
if t_input > 0 and t_guia > 0 and t_input > t_guia:
    warnings.append("La Matriz de Entrada ha sido modificada y es MÁS NUEVA que el análisis TDA guardado. (Reprocesar NLP).")
    needs_nlp = True
elif t_input > 0 and t_guia > 0:
    success.append("Análisis TDA Algorítmico sincronizado con la Matriz de Entrada.")

# Validar Sincronía NLP vs KB (PDFs)
if t_kb_max > 0 and t_guia > 0 and t_kb_max > t_guia:
    warnings.append("Hay PDFs recientes que NO han sido asimilados por el motor RAG. (Reprocesar NLP).")
    needs_nlp = True
elif t_kb_max > 0 and t_guia > 0:
    success.append("La Base de Conocimiento (PDFs) está perfectamente asimilada por el modelo RAG.")

# Validar Sincronía Salida Excel vs NLP y vs Input
if t_output > 0 and t_guia > 0 and t_guia > t_output:
    warnings.append("El Excel de Resultados está desactualizado respecto al último cruce cognitivo (RAG). (Generar Excel).")
    needs_export = True
elif t_output > 0 and t_input > 0 and t_input > t_output:
    warnings.append("El Excel de Resultados es más viejo que la carga limpia del R40 AAPP. (Generar Excel).")
    needs_export = True
elif t_output > 0:
    success.append("Excel de Resultados Excel Sincronizado masivamente.")

st.header("1. Trazabilidad de Bases de Datos Computacionales")
colA, colB, colC = st.columns(3)
with colA:
    st.info(f"💾 **1. Matriz Cruda (Entrada)**\n\nÚltima Modificación Absoluta:\n`{datetime.fromtimestamp(t_input).strftime('%Y-%m-%d %H:%M:%S') if t_input else 'N/A'}`")
with colB:
    st.info(f"🧠 **2. Motor TDA/NLP (Estrategia)**\n\nÚltima Modificación Absoluta:\n`{datetime.fromtimestamp(t_guia).strftime('%Y-%m-%d %H:%M:%S') if t_guia else 'N/A'}`")
with colC:
    st.info(f"📊 **3. Matriz Analítica (Salida)**\n\nÚltima Modificación Absoluta:\n`{datetime.fromtimestamp(t_output).strftime('%Y-%m-%d %H:%M:%S') if t_output else 'N/A'}`")

st.divider()

st.header("2. Semáforo de Acción Operativa")

if len(warnings) == 0:
    st.success("✅ ESTADO ÓPTIMO (CALIDAD AL 100%): Todos los datos de entrada, modelos en caché, y excels generados, están cronológicamente alineados. El equipo puede proceder de forma segura.")
else:
    st.error("⚠️ ALERTA DE DATOS DESFASADOS: Se encontró un cuello de botella o desfase en los documentos. Ejecute los pasos requeridos debajo.")
    for w in warnings:
        st.warning(f"**Hallazgo de Auditoría:** {w}")

st.divider()
st.header("3. Acciones Recomendadas y Requeridas")

col1, col2 = st.columns(2)

with col1:
    if needs_nlp:
        st.error("👉 **ACCIÓN PRIMARIA REQUERIDA:**\nMotor NLP/TDA desactualizado u obra con información de un mes anterior. Ve al Panel de Administración y ejecuta '🚀 Ejecutar Motor Neuronal'.")
        if st.button("Ir al Administrador para Reprocesar Inteligencia", type="primary"):
            st.switch_page("pages/4_Administracion.py")
    else:
        st.success("✅ Integridad neuronal aprobada. No requiere recálculo computacional.")

with col2:
    if needs_export:
        st.warning("👉 **ACCIÓN SECUNDARIA REQUERIDA:**\nEl archivo R40 de resultados para Microsoft Excel está obsoleto. Ve al Panel de Administración y ejecuta '💾 Generar Excel de Resultados'.")
        if st.button("Ir al Administrador para Integrar a Excel", type="primary"):
            st.switch_page("pages/4_Administracion.py")
    else:
        st.success("✅ Archivo de Microsoft Excel exportado con calidad al día.")

st.divider()
with st.expander("Ver Bitácora de Sincronía Exitosa (Logs OK)"):
    for s in success:
        st.markdown(f"- ✔️ {s}")
