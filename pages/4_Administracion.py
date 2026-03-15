import streamlit as st
import os
import json
import subprocess
import time
import glob

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING
# ==========================================
st.set_page_config(page_title="SABIA - Panel de Administración", layout="wide", page_icon="⚙️")
import menu
menu.render_menu()



st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* System Cards */
    div.stButton > button {
        border-radius: 6px;
        font-weight: 600;
    }
    .metric-box {
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("⚙️ SABIA: Consola de Administración MLOps")
    st.markdown("**Gestión central de bases de Excel, acervo histórico documental y recalibración del motor matemático.**")

# ==========================================
# 2. FUNCIONES CORE
# ==========================================
CONFIG_FILE = 'config.json'

def get_kb_state():
    kb_path = "Base de Conocimiento"
    if not os.path.exists(kb_path): return {}
    pdfs = glob.glob(os.path.join(kb_path, "*.pdf"))
    state = {}
    for pdf in pdfs:
        stat = os.stat(pdf)
        state[os.path.basename(pdf)] = f"{stat.st_size}_{stat.st_mtime}"
    return state

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    return {'excel_input': 'R40 AAPP - FINAL - Marzo 13.xlsx', 'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx', 'kb_state': {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f: json.dump(config, f)

config = load_config()

# ==========================================
# 3. INTERFAZ DE ADMINISTRACIÓN
# ==========================================

st.markdown("### 1. Ingesta de Matriz Ciudadana (Input Layer)")
st.info(f"**Data Lake Activo (Matriz Principal):** `{config['excel_input']}`")

uploaded_file = st.file_uploader("Actualizar Sábana R40 (Excel .xlsx)", type=["xlsx"])

if uploaded_file is not None:
    if st.button("💾 Empujar a Producción y Activar Matriz", type="primary"):
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        config['excel_input'] = file_path
        save_config(config)
        st.success(f"Archivo **{file_path}** mapeado como Ingesta 0 (Input Root).")
        st.cache_data.clear()
        st.cache_resource.clear()
        time.sleep(1)
        st.rerun()

st.divider()

st.markdown("### 2. Base de Conocimiento (Archivos Institucionales)")
kb_path = "Base de Conocimiento"
if not os.path.exists(kb_path):
    os.makedirs(kb_path)

current_kb_state = get_kb_state()
saved_kb_state = config.get('kb_state', {})

if current_kb_state != saved_kb_state:
    st.warning("⚠️ **Desincronización en Base Documental:** Se ha detectado una mutación (adición/eliminación) de archivos PDF subyacentes. Se exige recalibración del Motor Neuronal para prevenir Alucinaciones.")

uploaded_pdfs = st.file_uploader("Expandir Acervo con Decretos / Leyes / Documentos Técnicos (PDF)", type=["pdf"], accept_multiple_files=True)
if uploaded_pdfs:
    if st.button("💾 Inyectar PDFs a la Base Vectorial", type="secondary"):
        for pdf in uploaded_pdfs:
            pdf_path = os.path.join(kb_path, pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(pdf.getbuffer())
        st.success(f"Se han guardado {len(uploaded_pdfs)} documentos exitosamente en el Acervo Institucional.")
        st.rerun()

st.divider()

st.markdown("### 3. Orquestador Automático y Recálculo Analítico")
st.error("⚠️ **Carga Computacional Alta:** La ejecución de estos modelos consume CPU y RAM. Evitar lanzar múltiples recalibraciones simultáneas.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🧠 Capa 1: Recalibrar Topología y Contexto")
    st.markdown("Este botón reconstruye toda la agrupación ciudadana a novel nacional, calcula sus diferencias conceptuales y formula la afinidad contra los PDFs cargados en la fase 2.")
    if st.button("🚀 Lanzar Motor de Inteligencia (Pipeline A)", use_container_width=True, type="primary"):
        with st.spinner("Compilando Tensores y Grafos (Espere por favor)..."):
            try:
                result = subprocess.run(["python", "analysis.py"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("Arquitectura Topológica reconstruida exitosamente.")
                    config['kb_state'] = get_kb_state()
                    save_config(config)
                    with st.expander("Ver Traza del Compilador"):
                        st.code(result.stdout)
                else:
                    st.error("Error crítico en Pipeline A.")
                    with st.expander("Ver Dump de Error"):
                        st.code(result.stderr)
            except Exception as e:
                st.error(f"Falla del orquestador: {e}")

with col2:
    st.markdown("#### 📊 Capa 2: Ensamblar Artefacto de Salida (Output)")
    st.markdown("Traduce los clústeres matemáticos de la Capa 1 y los consolida en una macro-matriz Excel interactiva para el equipo legal.")
    out_name = st.text_input("Pipeline Output (Archivo a Exportar):", value=config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx'))
    
    if st.button("💾 Generar Matriz de Resultados", use_container_width=True, type="secondary"):
        config['excel_output'] = out_name
        save_config(config)
        
        with st.spinner("Ensamblando Matriz Multidimensional Excel..."):
             try:
                 result = subprocess.run(["python", "export_tda_excel.py"], capture_output=True, text=True)
                 if result.returncode == 0:
                     st.success(f"Artefacto Excel generado: {out_name}")
                     with st.expander("Ver Traza del Empaquetador"):
                         st.code(result.stdout)
                 else:
                     st.error("Error empaquetando el artefacto.")
                     with st.expander("Ver Dump de Error"):
                         st.code(result.stderr)
             except Exception as e:
                 st.error(f"Falla del orquestador: {e}")

st.divider()
st.markdown("#### 🚽 Mantenimiento del Servidor")
if st.button("🧹 Limpiar Caché Vectorial y Memoria GUI"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Memoria gráfica y RAM liberadas exitosamente.")
