import streamlit as st
import os
import json
import subprocess
import time
import glob

st.set_page_config(page_title="Administración del Sistema", layout="wide", page_icon="⚙️")
st.title("⚙️ Panel de Administración y Reprocesamiento")
st.markdown("Actualice la matriz de datos y relance los algoritmos de Inteligencia Artificial (NLP & TDA).")

CONFIG_FILE = 'config.json'

def get_kb_state():
    kb_path = "Base de Conocimiento"
    if not os.path.exists(kb_path):
        return {}
    pdfs = glob.glob(os.path.join(kb_path, "*.pdf"))
    state = {}
    for pdf in pdfs:
        stat = os.stat(pdf)
        state[os.path.basename(pdf)] = f"{stat.st_size}_{stat.st_mtime}"
    return state

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'excel_input': 'R40 AAPP - FINAL - Marzo 13.xlsx', 'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx', 'kb_state': {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

st.header("1. Actualizar Matriz de Participación Ciudadana")
st.info(f"**Archivo de entrada activo:** `{config['excel_input']}`")

uploaded_file = st.file_uploader("Suba la nueva matriz de datos R40 (Excel .xlsx)", type=["xlsx"])

if uploaded_file is not None:
    if st.button("💾 Guardar y Establecer como Activo", type="primary"):
        # Guardar archivo fisicamente
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Actualizar config
        config['excel_input'] = file_path
        save_config(config)
        st.success(f"Archivo **{file_path}** guardado y configurado como la nueva matriz de entrada.")
        st.cache_data.clear()
        st.cache_resource.clear()
        time.sleep(1)
        st.rerun()

st.divider()

st.header("2. Base de Conocimiento (PDFs)")
kb_path = "Base de Conocimiento"
if not os.path.exists(kb_path):
    os.makedirs(kb_path)

current_kb_state = get_kb_state()
saved_kb_state = config.get('kb_state', {})

if current_kb_state != saved_kb_state:
    st.warning("⚠️ **Cambios Detectados en la Base de Conocimiento:** Se han añadido, modificado o eliminado documentos PDF. Se recomienda Reprocesar el Motor Neuronal para actualizar el cruce normativo.")

uploaded_pdfs = st.file_uploader("Subir nuevos documentos normativos (PDF)", type=["pdf"], accept_multiple_files=True)
if uploaded_pdfs:
    if st.button("💾 Guardar PDFs en Base de Conocimiento", type="secondary"):
        for pdf in uploaded_pdfs:
            pdf_path = os.path.join(kb_path, pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(pdf.getbuffer())
        st.success(f"Se han guardado {len(uploaded_pdfs)} documentos exitosamente en '{kb_path}'.")
        st.rerun()

st.divider()

st.header("3. Pipeline de Reprocesamiento (TDA & NLP)")
st.warning("⚠️ **Atención:** Ejecutar estos algoritmos requiere alta capacidad de cómputo. El proceso leerá la nueva matriz activa y recalculará la Topología Matemática y la Base Normativa RAG de cero.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧠 Paso A: Recalcular Topología y RAG")
    st.markdown("Lee la nueva matriz, genera embeddings, detecta clústeres y cruza con la Base Doc. Genera una nueva Guía Estratégica.")
    if st.button("🚀 Ejecutar Motor Neuronal", use_container_width=True):
        with st.spinner("Ejecutando Modelos NLP (Puede tomar varios minutos)..."):
            try:
                # Ejecutar analysis.py como subproceso bloqueante
                result = subprocess.run(["python", "analysis.py"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("Tópicos y Cruce Normativo recalculados exitosamente.")
                    config['kb_state'] = get_kb_state()
                    save_config(config)
                    with st.expander("Ver Log de Consola"):
                        st.code(result.stdout)
                else:
                    st.error("Error al ejecutar el Script de Análisis.")
                    with st.expander("Ver Detalles de Error"):
                        st.code(result.stderr)
            except Exception as e:
                st.error(f"Falla del sistema: {e}")

with col2:
    st.markdown("### 📊 Paso B: Ensamblar Excel Final")
    st.markdown("Inyecta los sub-resultados espaciales y estratégicos nuevamente al Excel preservando su formato original estructural.")
    out_name = st.text_input("Nombre del archivo de Salida a generar:", value=config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx'))
    
    if st.button("💾 Generar Excel de Resultados", use_container_width=True):
        config['excel_output'] = out_name
        save_config(config)
        
        with st.spinner("Ensamblando Matriz Multidimensional Excel..."):
             try:
                 result = subprocess.run(["python", "export_tda_excel.py"], capture_output=True, text=True)
                 if result.returncode == 0:
                     st.success(f"Matriz de Resultados exportada como: {out_name}")
                     with st.expander("Ver Log de Consola"):
                         st.code(result.stdout)
                 else:
                     st.error("Error empaquetando el Excel.")
                     with st.expander("Ver Detalles de Error"):
                         st.code(result.stderr)
             except Exception as e:
                 st.error(f"Falla del sistema: {e}")

st.divider()
st.markdown("### 🚽 Limpieza de Caché de Memoria")
if st.button("🧹 Purgar Memoria Caches de Streamlit"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Memoria caché liberada.")
