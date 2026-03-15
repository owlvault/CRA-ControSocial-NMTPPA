import streamlit as st
import re
import os
import json
import pandas as pd
from datetime import datetime

# Configuracion de Pagina
st.set_page_config(page_title='Gestor de Respuestas NMT', layout='wide')

st.title("⚖️ Gestión y Asignación de Respuestas - CRA")
st.markdown("### Plataforma de revisión de clústeres por el equipo Técnico/Jurídico")

# --- FUNCIONES DE PARSEO ---
@st.cache_data
def load_clusters():
    file_path = 'guia_estrategica_cra.md'
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar por '### Clúster ' y eliminar el primer elemento (resumen inicial)
    raw_clusters = content.split('### Clúster ')[1:]
    clusters = []

    for raw in raw_clusters:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if not lines:
            continue
            
        header = lines[0]
        id_tema = header.split(':', 1)
        cluster_id = id_tema[0].strip()
        tema = id_tema[1].strip() if len(id_tema) > 1 else "Tema General"

        # Buscar relevancia
        relevancia = "Desconocida"
        sintesis = ""
        estrategia = ""
        sustento = []
        
        capturing_sintesis = False
        capturing_estrategia = False
        
        for i, line in enumerate(lines):
            if line.startswith('**Relevancia:**'):
                relevancia = line.replace('**Relevancia:**', '').strip()
            # Síntesis
            elif line.startswith('- **Síntesis de las Preguntas:**'):
                capturing_sintesis = True
                capturing_estrategia = False
                continue
            # Estrategia
            elif line.startswith('- **Estrategia de Respuesta Sugerida:**'):
                capturing_estrategia = True
                capturing_sintesis = False
                continue
            # Sustento
            elif line.startswith('> **'):
                capturing_sintesis = False
                capturing_estrategia = False
                sustento.append(line.replace('>', '').strip())
                continue
            elif line.startswith('- **Sustento Normativo Identificado:**') or line.startswith('- **Perfil de la Inquietud:**') or line.startswith('---'):
                capturing_sintesis = False
                capturing_estrategia = False
                continue

            if capturing_sintesis:
                sintesis += line + " "
            if capturing_estrategia:
                estrategia += line + " "

        clusters.append({
            'identificador': f"Clúster {cluster_id}",
            'tema': tema,
            'relevancia': relevancia,
            'sintesis': sintesis.strip().replace('*', ''),
            'sustento': sustento,
            'estrategia': estrategia.strip()
        })
        
    return clusters

# --- MANEJO DE ESTADO DE ASIGNACIONES ---
ASSIGNMENTS_FILE = "asignaciones_equipo.json"
def load_assignments():
    if os.path.exists(ASSIGNMENTS_FILE):
        with open(ASSIGNMENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_assignment(cluster_id, responsable, prioridad, notas):
    assignments = load_assignments()
    assignments[cluster_id] = {
        'responsable': responsable,
        'prioridad': prioridad,
        'notas': notas,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(ASSIGNMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(assignments, f, indent=4)
    return True

# --- INTERFAZ DE USUARIO ---
clusters = load_clusters()
assignments = load_assignments()

if not clusters:
    st.warning("No se ha encontrado el archivo `guia_estrategica_cra.md`. Ejecuta primero el pipeline de análisis.")
    st.stop()

# Sidebar para Filtros y Navegación
with st.sidebar:
    st.header("📊 Resumen del Análisis")
    st.metric("Total de Clústeres", len(clusters))
    st.metric("Preguntas procesadas", "1701")
    st.metric("Clústeres Asignados", len(assignments))
    
    st.divider()
    st.subheader("Filtro de Navegación")
    opciones_clusters = [c['identificador'] + " - " + c['tema'][:30] + "..." for c in clusters]
    seleccion = st.selectbox("Seleccione un Clúster para revisar:", opciones_clusters)

# Layout Principal dividido en Columnas
idx_seleccionado = opciones_clusters.index(seleccion)
c_data = clusters[idx_seleccionado]
c_id = c_data['identificador']

col_info, col_asignacion = st.columns([2, 1])

with col_info:
    st.subheader(f"{c_id}: {c_data['tema']}")
    st.caption(f"**Relevancia:** {c_data['relevancia']}")
    
    with st.expander("📝 Síntesis de la Inquietud Ciudadana", expanded=True):
        st.write(c_data['sintesis'])
        
    with st.expander("⚖️ Sustento Normativo Identificado (RAG)", expanded=True):
        if not c_data['sustento']:
            st.info("Sin referencias.")
        for ref in c_data['sustento']:
            st.markdown(f"📖 {ref}")
            
    with st.expander("🎯 Estrategia Sugerida para el Redactor", expanded=True):
        st.success(c_data['estrategia'])

with col_asignacion:
    st.subheader("👤 Asignación de Tareas")
    st.markdown("Delegar a coordinador/abogado responsable")
    
    prev_asig = assignments.get(c_id, {})
    
    with st.form(key=f"form_{c_id}"):
        responsable = st.selectbox("Asignar a:", ["Jurídica - Regulación", "Técnico - Economía", "Técnico - Ingeniería", "Atención al Ciudadano"], 
                                   index=["Jurídica - Regulación", "Técnico - Economía", "Técnico - Ingeniería", "Atención al Ciudadano"].index(prev_asig.get('responsable', "Jurídica - Regulación")) if prev_asig else 0)
        
        prioridad = st.radio("Nivel de Prioridad:", ["Alta 🔴", "Media 🟡", "Baja 🟢"], 
                             index=["Alta 🔴", "Media 🟡", "Baja 🟢"].index(prev_asig.get('prioridad', "Media 🟡")) if prev_asig else 1)
        
        notas = st.text_area("Instrucciones Específicas / Observaciones internas:", 
                             value=prev_asig.get('notas', ""))
        
        submit_button = st.form_submit_button(label="Asignar Clúster 🚀")
        
        if submit_button:
            save_assignment(c_id, responsable, prioridad, notas)
            st.success("¡Asignación guardada con éxito!")

# Tabla Resumen Inferior
st.divider()
st.subheader("Tabla General de Gestión de Clústeres")

tabla_datos = []
for c in clusters:
    has_asig = c['identificador'] in assignments
    tabla_datos.append({
        'ID Clúster': c['identificador'],
        'Tema Central': c['tema'],
        'Relevancia': c['relevancia'],
        'Estado': '✅ Asignado' if has_asig else '⏳ Pendiente',
        'Responsable': assignments[c['identificador']]['responsable'] if has_asig else '-',
        'Prioridad': assignments[c['identificador']]['prioridad'] if has_asig else '-'
    })

df_tabla = pd.DataFrame(tabla_datos)
st.dataframe(df_tabla, use_container_width=True)

# Botón para descargar reporte de asignaciones
if assignments:
    csv = df_tabla.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte de Asignaciones (CSV)",
        data=csv,
        file_name='reporte_asignaciones_cra.csv',
        mime='text/csv',
    )
