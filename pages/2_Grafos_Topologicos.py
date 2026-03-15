import streamlit as st
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
import hdbscan
import umap
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING
# ==========================================
st.set_page_config(page_title='SABIA - Grafos Topológicos', layout='wide', page_icon='🕸️')

# Inyección UX: Tipografía corporativa, espacio negativo, high data-to-ink ratio
st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div { color: #2C3E50; }
    
    [data-testid="stMetricValue"] { color: #0055A4 !important; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-left: 5px solid #0055A4;
        border-radius: 4px;
        padding: 10px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Logo y Título Principal
col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("🕸️ SABIA: Grafos Topológicos y Redes")
    st.markdown("**Sistema de Análisis Basado en Inteligencia Artificial - Cartografía Relacional**")

# ==========================================
# 2. UX: MODO PROGRESIVO EXPERTO/JURÍDICO
# ==========================================
st.sidebar.markdown("### ⚙️ Panel de Renderizado")
modo_cientifico = st.sidebar.toggle("Modo Ingeniero de Grafos", value=False, help="Revelar tensores UMAP y fuerzas de repulsión del grafo.")

if modo_cientifico:
    st.sidebar.markdown("#### Calibración Topológica")
    n_neighbors_umap = st.sidebar.slider("Vecindario UMAP", 5, 50, 15)
    min_dist_umap = st.sidebar.slider("Dispersión 2D", 0.0, 0.5, 0.1)
    k_forces = st.sidebar.slider("Resorte NetworkX (K)", 0.1, 2.0, 0.8, help="Tensión repulsiva entre los nodos del conocimiento normativo.")
else:
    n_neighbors_umap = 15
    min_dist_umap = 0.1
    k_forces = 0.8
    st.sidebar.info("Vista optimizada para perfiles jurídicos. Las físicas de red y parámetros UMAP han sido abstraídos.")

# ==========================================
# 3. NÚCLEO MATEMÁTICO (Caché optimizado)
# ==========================================
@st.cache_resource
def load_models():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_models()

@st.cache_data(show_spinner=False)
def run_analysis_pipeline(n_neigh, m_dist):
    config_path = 'config.json'
    excel_path = 'R40 AAPP - FINAL - Marzo 13.xlsx' 
    if os.path.exists(config_path):
        with open(config_path, 'r') as f: 
            config = json.load(f)
            excel_path = config.get('excel_input', excel_path)
    
    try:
        df = pd.read_excel(excel_path, sheet_name='REG-FOR03')
    except Exception as e:
        return None, None, None, f"Error cargando Matriz Original: {e}"

    df['Consulta_Clean'] = df['Consulta'].astype(str).str.strip().str.replace('\n', ' ')
    df = df[df['Consulta_Clean'].str.len() > 10].copy().reset_index(drop=True)
    preguntas = df['Consulta_Clean'].tolist()
    
    embeddings = model.encode(preguntas, show_progress_bar=False)
    
    # Reduccion UMAP 2D Optimizada
    reducer = umap.UMAP(n_neighbors=n_neigh, min_dist=m_dist, n_components=2, metric='cosine', random_state=42)
    umap_embeddings = reducer.fit_transform(embeddings)
    df['UMAP_X'] = umap_embeddings[:, 0]
    df['UMAP_Y'] = umap_embeddings[:, 1]
    
    # Clustering rápido EOM
    clusterer = hdbscan.HDBSCAN(min_cluster_size=25, metric='euclidean', cluster_selection_method='eom')
    df['Cluster'] = clusterer.fit_predict(embeddings)
    
    # RAG Extraction
    file_path = 'guia_estrategica_cra.md'
    if not os.path.exists(file_path):
        return df, embeddings, None, "Base Documental RAG no encontrada."
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    raw_clusters = content.split('### Clúster ')[1:]
    cluster_docs = {}
    
    for raw in raw_clusters:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if not lines: continue
            
        cluster_id = int(lines[0].split(':', 1)[0].strip())
        
        doc_refs = []
        for line in lines:
            if line.startswith('> **'):
                doc_name = line.split('**')[1].split('-')[0].strip()
                if doc_name not in doc_refs:
                    doc_refs.append(doc_name)
        
        cluster_docs[cluster_id] = doc_refs
        
    return df, embeddings, cluster_docs, None

with st.spinner('Ensamblando Grafos y Cartografías...'):
    df, embeddings, cluster_docs, err = run_analysis_pipeline(n_neighbors_umap, min_dist_umap)

if err:
    st.error(err)
    st.stop()

# ==========================================
# 4. CAPA DE PRESENTACIÓN PÚBLICA (TABS UX)
# ==========================================
tabs = st.tabs(["🕸️ Red Normativa vs Clústeres", "🗺️ Cartografía Plana UMAP", "📊 Diagnóstico Demográfico"])

# Tab 1: RED BI-PARTITA (NetworkX) UX Limpio
with tabs[0]:
    st.subheader("Grafo Bi-Partito de Tracción Documental")
    st.markdown("Visualice con qué intensidad los diferentes Clústeres Nacionales intersectan (y exigen respuesta) a resoluciones y decretos puntuales del Acervo Normativo Histórico.")
    
    if not cluster_docs:
         st.warning("No se encontraron referencias normativas (RAG) para graficar.")
    else:
        G = nx.Graph()
        
        for c_real, refs in cluster_docs.items():
            topico_id = f"Tópico {c_real}"
            # Nodos de Ciudadanos (Azules)
            G.add_node(topico_id, type='Topic', size=25, color='#0055A4', line='#003366')
            
            for ref in refs:
                pdf_node = f"Norma: {ref}"
                # Nodos de Documentos (Naranjas/Dorados Institucionales)
                G.add_node(pdf_node, type='PDF', size=45, color='#F39C12', line='#D68910')
                G.add_edge(topico_id, pdf_node, weight=1)
                
        # Estructura Física
        pos = nx.spring_layout(G, k=k_forces, seed=42)
        
        # Geometría Visual
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='#D0D3D4'),
            hoverinfo='none', mode='lines')

        node_x, node_y, node_text, node_color, node_size, node_line = [], [], [], [], [], []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x); node_y.append(y); node_text.append(node)
            node_color.append(G.nodes[node]['color'])
            node_size.append(G.nodes[node]['size'])
            node_line.append(G.nodes[node]['line'])

        node_trace = go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            hoverinfo='text',
            text=[t if 'Norma' in t else '' for t in node_text], # Simplificar ruido visual
            textposition="top center",
            textfont=dict(size=12, color='#2C3E50', family="Arial Black"),
            marker=dict(color=node_color, size=node_size, line=dict(width=2, color=node_line)))
        
        node_trace.text = node_text

        fig_graph = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False, hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=750, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                 ))
        
        st.plotly_chart(fig_graph, use_container_width=True)

# Tab 2: UMAP UX (Scatter Plana)
with tabs[1]:
    st.subheader("Cartografía Semántica Plana (Reducción Dimensional)")
    df_plot = df.copy()
    df_plot['Cluster_Str'] = df_plot['Cluster'].astype(str)
    df_plot.loc[df_plot['Cluster'] == -1, 'Cluster_Str'] = '-1 (Consultas Individuales)'
    df_plot['Fragmento'] = df_plot['Consulta_Clean'].str[:90] + '...'
    
    # Paleta condicional (Experto vs Corporativo)
    color_mapped = px.colors.qualitative.Dark24 if modo_cientifico else px.colors.qualitative.Safe
    
    fig = px.scatter(df_plot, x='UMAP_X', y='UMAP_Y', color='Cluster_Str', 
                     hover_name='Fragmento', 
                     hover_data={'UMAP_X':False, 'UMAP_Y':False, 'Cluster_Str':True},
                     color_discrete_sequence=color_mapped, opacity=0.8)
    
    fig.update_layout(height=700, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(showgrid=False, zeroline=False),
                      yaxis=dict(showgrid=False, zeroline=False))
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: MÉTRICAS (Clean UX)
with tabs[2]:
    st.subheader("Cuadro de Mando Ejecutivo")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Observaciones Válidas", len(df))
    with col2: st.metric("Nodos Topológicos Aislados (Tópicos)", len([c for c in df['Cluster'].unique() if c != -1]))
    with col3: st.metric("Tracción Individual (Casos Atípicos)", len(df[df['Cluster'] == -1]))
        
    st.divider()
    colX, colY = st.columns(2)
    
    with colX:
        st.markdown("**Segmentación de Complejidad**")
        if 'Nivel de compejidad' in df.columns:
            comp_df = df['Nivel de compejidad'].value_counts().reset_index()
            comp_df.columns = ['Complejidad', 'Cantidad']
            fig_bar = px.bar(comp_df, x='Complejidad', y='Cantidad', text='Cantidad',
                             color_discrete_sequence=['#0055A4'])
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with colY:
        st.markdown("**Volumen Radiográfico por Zona**")
        if 'ZONA' in df.columns:
            zona_df = df['ZONA'].value_counts().reset_index().head(8)
            zona_df.columns = ['Zona', 'Cantidad']
            fig_pie = px.pie(zona_df, names='Zona', values='Cantidad', hole=0.5,
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
