import streamlit as st
import re
import os
import json
import pandas as pd
from datetime import datetime

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING
# ==========================================
st.set_page_config(page_title='SABIA - Gestión de Respuestas', layout='wide', page_icon='🏛️')

st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* Clean Cards y Expansores */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border-radius: 4px;
        color: #0055A4 !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stForm"] {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e1e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        padding: 20px;
    }
    
    /* Tipografía Tabular para IDs */
    [data-testid="stDataFrame"] { font-variant-numeric: tabular-nums; }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("🏛️ SABIA: Gestión de Estrategias y Clústeres")
    st.markdown("**Plataforma de revisión ejecutiva y delegación de redacción normativa.**")

# ==========================================
# 2. FUNCIONES DE PARSEO
# ==========================================
@st.cache_data
def load_clusters():
    file_path = 'guia_estrategica_cra.md'
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_clusters = content.split('### Clúster ')[1:]
    clusters = []

    for raw in raw_clusters:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if not lines: continue
            
        header = lines[0]
        id_tema = header.split(':', 1)
        cluster_id = id_tema[0].strip()
        tema = id_tema[1].strip() if len(id_tema) > 1 else "Tema General"

        relevancia = "Desconocida"
        sintesis, estrategia, sustento = "", "", []
        
        capturing_sintesis = False
        capturing_estrategia = False
        
        for i, line in enumerate(lines):
            if line.startswith('**Relevancia:**'):
                relevancia = line.replace('**Relevancia:**', '').strip()
            elif line.startswith('- **Síntesis de las Preguntas:**'):
                capturing_sintesis = True; capturing_estrategia = False; continue
            elif line.startswith('- **Estrategia de Respuesta Sugerida:**'):
                capturing_estrategia = True; capturing_sintesis = False; continue
            elif line.startswith('> **'):
                capturing_sintesis = False; capturing_estrategia = False
                sustento.append(line.replace('>', '').strip()); continue
            elif line.startswith('- **Sustento Normativo Identificado:**') or line.startswith('- **Perfil de la Inquietud:**') or line.startswith('---'):
                capturing_sintesis = False; capturing_estrategia = False; continue

            if capturing_sintesis: sintesis += line + " "
            if capturing_estrategia: estrategia += line + " "

        clusters.append({
            'identificador': f"Clúster {cluster_id}",
            'tema': tema, 'relevancia': relevancia,
            'sintesis': sintesis.strip().replace('*', ''),
            'sustento': sustento, 'estrategia': estrategia.strip()
        })
        
    return clusters

# --- MANEJO DE ESTADO DE ASIGNACIONES ---
ASSIGNMENTS_FILE = "asignaciones_equipo.json"
def load_assignments():
    if os.path.exists(ASSIGNMENTS_FILE):
        with open(ASSIGNMENTS_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_assignment(cluster_id, responsable, prioridad, notas):
    assignments = load_assignments()
    assignments[cluster_id] = {
        'responsable': responsable, 'prioridad': prioridad, 'notas': notas,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(ASSIGNMENTS_FILE, 'w', encoding='utf-8') as f: json.dump(assignments, f, indent=4)
    return True

# ==========================================
# 3. INTERFAZ DE USUARIO
# ==========================================
clusters = load_clusters()
assignments = load_assignments()

if not clusters:
    st.warning("⚠️ No se ha detectado Topología base. Ejecute la Red Neuronal desde el Panel Admin.")
    st.stop()

# Menú Lateral MLOps
with st.sidebar:
    st.markdown("### 📊 Auditoría de Flujo")
    st.metric("Tópicos Totales Procesados", len(clusters))
    st.metric("Asignaciones Delegadas", f"{len(assignments)} de {len(clusters)}")
    st.progress(len(assignments) / max(len(clusters), 1))
    
    st.divider()
    st.markdown("### 🧭 Navegación")
    opciones_clusters = [c['identificador'] + " - " + c['tema'][:30] + "..." for c in clusters]
    seleccion = st.selectbox("Auditar Clúster:", opciones_clusters)

# Layout Principal UX
idx_seleccionado = opciones_clusters.index(seleccion)
c_data = clusters[idx_seleccionado]
c_id = c_data['identificador']

col_info, col_asignacion = st.columns([2, 1])

with col_info:
    st.subheader(f"{c_id}: {c_data['tema']}")
    st.caption(f"**Criticidad Detectada (Módulo de Complejidad):** {c_data['relevancia']}")
    
    with st.expander("📝 Síntesis de la Inquietud Ciudadana", expanded=True):
        st.info(c_data['sintesis'])
        
    with st.expander("⚖️ Mapeo RAG (Sustento Normativo Histórico)", expanded=True):
        if not c_data['sustento']:
            st.warning("Sin intersección normativa detectada en documentos base.")
        for ref in c_data['sustento']:
            st.markdown(f"📄 **{ref}**")
            
    with st.expander("🎯 Directriz Estratégica", expanded=True):
        st.success(c_data['estrategia'])

with col_asignacion:
    st.markdown("#### 👤 Delegación Jurídica")
    st.markdown("Emitir instrucción de redacción al equipo.")
    
    prev_asig = assignments.get(c_id, {})
    
    with st.form(key=f"form_{c_id}"):
        responsable = st.selectbox("Asignar Especialista:", ["Atención al Ciudadano (Call Center)", "Jurídica - Regulación", "Técnico - Economía", "Técnico - Ingeniería", "Comisión Directiva"], 
                                   index=["Atención al Ciudadano (Call Center)", "Jurídica - Regulación", "Técnico - Economía", "Técnico - Ingeniería", "Comisión Directiva"].index(prev_asig.get('responsable', "Jurídica - Regulación")) if prev_asig else 0)
        
        prioridad = st.radio("Prioridad de Despacho:", ["Alta 🔴", "Media 🟡", "Baja 🟢"], 
                             index=["Alta 🔴", "Media 🟡", "Baja 🟢"].index(prev_asig.get('prioridad', "Media 🟡")) if prev_asig else 1)
        
        notas = st.text_area("Directrices manuales / Contexto institucional:", 
                             value=prev_asig.get('notas', ""))
        
        if st.form_submit_button("Fijar Asignación 🚀", type="primary", use_container_width=True):
            save_assignment(c_id, responsable, prioridad, notas)
            st.toast("Clúster delegado al sistema.", icon="✅")
            st.rerun()

# Tabla Ejecutiva Limpia
st.divider()
st.subheader("Directorio General de Clientes / Clústeres")

tabla_datos = []
for c in clusters:
    has_asig = c['identificador'] in assignments
    tabla_datos.append({
        'Clúster TDA': c['identificador'],
        'Asunto Central': c['tema'],
        'Prioridad NLP': c['relevancia'],
        'Status de Flujo': '🟢 Delegado' if has_asig else '⚪ En Espera',
        'Dependencia Asignada': assignments[c['identificador']]['responsable'] if has_asig else '-',
        'Nivel Urgencia': assignments[c['identificador']]['prioridad'] if has_asig else '-'
    })

df_tabla = pd.DataFrame(tabla_datos)
st.dataframe(df_tabla, use_container_width=True, hide_index=True)

if assignments:
    csv = df_tabla.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Matriz de Trazabilidad (CSV)",
        data=csv,
        file_name='SABIA_trazabilidad_asignaciones.csv',
        mime='text/csv',
        type="primary"
    )
