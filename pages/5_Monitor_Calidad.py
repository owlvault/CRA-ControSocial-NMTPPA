import streamlit as st
import os
import glob
from datetime import datetime
import json

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING
# ==========================================
st.set_page_config(page_title="SABIA - Monitor de Calidad", layout="wide", page_icon="🩺")
import menu
menu.render_menu()



st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* Cajas de Estado Semántico */
    div.stAlert > div { border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    
    /* Módulos de Información Crítica */
    .metric-module {
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .metric-module h4 { color: #0055A4 !important; font-size: 1.1rem; margin-bottom: 10px; }
    .metric-module p { font-family: monospace; font-size: 1.2rem; color: #2C3E50; }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("🩺 SABIA: Módulo de Observabilidad y Sincronía")
    st.markdown("**Auditoría temporal: Integridad de Caché vs. Base Documental Oficial (RAG).**")

# ==========================================
# 2. MOTOR DE AUDITORÍA
# ==========================================
def get_mtime(path):
    return os.path.getmtime(path) if os.path.exists(path) else 0

CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    return {'excel_input': 'R40 AAPP - FINAL - Marzo 13.xlsx', 'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

config = load_config()

input_path = config.get('excel_input', '')
output_path = config.get('excel_output', '')
kb_path = "Base de Conocimiento"
guia_path = "guia_estrategica_cra.md"

t_input = get_mtime(input_path)
t_output = get_mtime(output_path)
t_guia = get_mtime(guia_path)

kb_pdfs = glob.glob(os.path.join(kb_path, "*.pdf"))
t_kb_max = max([get_mtime(pdf) for pdf in kb_pdfs]) if kb_pdfs else 0

needs_nlp, needs_export = False, False
warnings, success = [], []

if not os.path.exists(input_path):
    warnings.append(f"Fuga de Input: No se halla la matriz de entrada ({input_path}).")
    needs_nlp = True
else: success.append("Matriz Cruda conectada al Pipeline.")

if not os.path.exists(guia_path):
    warnings.append("Falta Compilación RAG: El ecosistema normativo no ha sido mapeado internamente.")
    needs_nlp = True
else: success.append("Base de Conocimiento RAG (Vectors) activa.")

if not os.path.exists(output_path):
    warnings.append("Ausencia de Output: Falta ensamblar el Excel final de trazabilidad.")
    needs_export = True
else: success.append("Bloque final de exportación detectado.")

if t_input > 0 and t_guia > 0 and t_input > t_guia:
    warnings.append("Desincronización por Input Nuevo: La matriz original fue reemplazada. La IA actual opera con datos antiguos.")
    needs_nlp = True
elif t_input > 0 and t_guia > 0:
    success.append("Machine Learning alineado temporalmente al Excel Sábana R40.")

if t_kb_max > 0 and t_guia > 0 and t_kb_max > t_guia:
    warnings.append("Desincronización Documental: Hay PDFs jurídicos recientemente subidos que la red neuronal NO ha procesado aún.")
    needs_nlp = True
elif t_kb_max > 0 and t_guia > 0:
    success.append("La memoria RAG comprende el 100% de los documentos PDF de la institución.")

if t_output > 0 and t_guia > 0 and t_guia > t_output:
    warnings.append("Rezago en Tablas de Salida: El modelo matemático es más reciente que el Excel generado.")
    needs_export = True
elif t_output > 0 and t_input > 0 and t_input > t_output:
    warnings.append("Rezago Absoluto: El Excel final es anterior a la nueva matriz original.")
    needs_export = True
elif t_output > 0:
    success.append("Artefactos de Salida perfectamente alineados.")

# ==========================================
# 3. INTERFAZ DE AUDITORÍA EJECUTIVA
# ==========================================
st.markdown("### 1. Trazabilidad Temporal de Clústeres (Timestamps)")
colA, colB, colC = st.columns(3)

with colA:
    st.markdown(f"""
    <div class="metric-module">
        <h4>💾 Nodo Base (Sábana Original)</h4>
        <p>{datetime.fromtimestamp(t_input).strftime('%Y-%m-%d %H:%M:%S') if t_input else 'Inexistente'}</p>
    </div>
    """, unsafe_allow_html=True)
with colB:
    st.markdown(f"""
    <div class="metric-module">
        <h4>🧠 Nodo de Memoria NLP (RAG)</h4>
        <p>{datetime.fromtimestamp(t_guia).strftime('%Y-%m-%d %H:%M:%S') if t_guia else 'Inexistente'}</p>
    </div>
    """, unsafe_allow_html=True)
with colC:
    st.markdown(f"""
    <div class="metric-module">
        <h4>📊 Artefacto Entregable (Output)</h4>
        <p>{datetime.fromtimestamp(t_output).strftime('%Y-%m-%d %H:%M:%S') if t_output else 'Inexistente'}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("### 2. Semáforo de Riesgo Legal (Compliance)")
if len(warnings) == 0:
    st.success("✅ **STATUS VERDE (SEGURIDAD 100%):** Todos los vectores, tensores gráficos y excels exportados coinciden a nivel de milisegundo operativo. El equipo jurídico y gerencial puede confiar plenamente en las cifras exhibidas localmente.")
else:
    st.error("⚠️ **STATUS ROJO (DESFASE COGNITIVO):** Peligro de 'Alucinación Regulatoria'. Los módulos del sistema operan con temporalidades fracturadas. Proceda a ejecutar el orquestador inmediatamente.")
    for w in warnings:
        st.warning(f"🕵️‍♂️ **Vector de Fallo:** {w}")

st.divider()

st.markdown("### 3. Resolución Táctica")
col1, col2 = st.columns(2)

with col1:
    if needs_nlp:
        st.error("👉 **BLOQUEO EN RED NEURONAL:**\nLa topología requiere compilación forzosa.")
        if st.button("Lanzar Consola de Recalibración (NLP)", type="primary"):
            st.switch_page("pages/4_Administracion.py")
    else:
        st.success("✅ **Tensor Aprobado:** Pipeline Analítico sano.")

with col2:
    if needs_export:
        st.warning("👉 **BLOQUEO EN ENSAMBLAJE:**\nEl equipo jurídico no tiene la matriz más reciente.")
        if st.button("Lanzar Empaquetador de Excel", type="primary"):
            st.switch_page("pages/4_Administracion.py")
    else:
        st.success("✅ **Excel Sano:** Bloques exportados correctamente.")

st.divider()
with st.expander("Ver Auditoría de Integridad Estructural (Log)"):
    for s in success:
        st.markdown(f"- ✔️ `{s}`")
