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

# Configuracion de Pagina
st.set_page_config(page_title='Análisis Topológico NMT', layout='wide')

st.title("🌐 Análisis Topológico y Semántico NMT")
st.markdown("### Plataforma de revisión de clústeres y relaciones normativas de la participación ciudadana.")

# --- MANEJO DE ESTADO MATRIZ ---
@st.cache_resource
def load_models():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_models()

@st.cache_data
def run_analysis_pipeline():
    import json
    with open('config.json', 'r') as f: config = json.load(f)
    excel_path = config['excel_input']
    try:
        df = pd.read_excel(excel_path, sheet_name='REG-FOR03')
    except Exception as e:
        return None, None, None, f"Error cargando Excel: {e}"

    df['Consulta_Clean'] = df['Consulta'].astype(str).str.strip().str.replace('\n', ' ')
    df = df[df['Consulta_Clean'].str.len() > 10].copy().reset_index(drop=True)
    preguntas = df['Consulta_Clean'].tolist()
    
    embeddings = model.encode(preguntas, show_progress_bar=False)
    
    # Reduccion de dimensionalidad con UMAP
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine', random_state=42)
    umap_embeddings = reducer.fit_transform(embeddings)
    df['UMAP_X'] = umap_embeddings[:, 0]
    df['UMAP_Y'] = umap_embeddings[:, 1]
    
    # Clustering HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=25, metric='euclidean', cluster_selection_method='eom')
    df['Cluster'] = clusterer.fit_predict(embeddings)
    
    # Cargar datos de guia estrategica
    file_path = 'guia_estrategica_cra.md'
    if not os.path.exists(file_path):
        return df, embeddings, None, "Falta generar guia estrategica (Base Normativa)"
    
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

with st.spinner('Cargando y procesando matriz topológica... esto puede tomar un poco.'):
    df, embeddings, cluster_docs, err = run_analysis_pipeline()

if err:
    st.error(err)
    st.stop()

# --- INTERFAZ ---

tabs = st.tabs(["🗺️ Mapa Semántico UMAP", "🕸️ Grafo de Relaciones Normativas", "📊 Métricas y Filtros"])

# Tab 1: UMAP
with tabs[0]:
    st.markdown("### Mapa Semántico de Observaciones (Proyección UMAP)")
    st.markdown("Cada punto es una observación ciudadana. La distancia representa similitud semántica. Los colores representan los clústeres (gris es ruido).")
    
    df_plot = df.copy()
    df_plot['Cluster_Str'] = df_plot['Cluster'].astype(str)
    df_plot.loc[df_plot['Cluster'] == -1, 'Cluster_Str'] = '-1 (Ruido)'
    
    df_plot['Hover_Text'] = df_plot['Consulta_Clean'].str[:100] + '...'
    
    fig = px.scatter(df_plot, x='UMAP_X', y='UMAP_Y', color='Cluster_Str', 
                     hover_name='Hover_Text', 
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     opacity=0.7)
    
    fig.update_layout(height=700, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: GRAFO
with tabs[1]:
    st.markdown("### Grafo de Conexiones: Clústeres Temáticos vs Documentos de Resolución")
    st.markdown("Muestra cómo las preocupaciones ciudadanas impactan los diferentes componentes normativos.")
    
    if not cluster_docs:
         st.warning("No se encontraron referencias normativas RAG en la guía.")
    else:
        G = nx.Graph()
        
        # Add nodes and edges
        for c_real, refs in cluster_docs.items():
            # Mapeo id visual
            topico_id = f"Clúster {c_real}"
            
            # Tamano de nodo aprox basado en df (cluster ID interno vs real puede variar un poco por ruido y ordenacion, 
            # asumimos un mapping simple aqui usando count aprox si estuviese mapeado 1:1, pero usamos un size fijo por ahora) 
            # ya que la guia estrategica reordena los clusters.
            c_size = 20
            
            G.add_node(topico_id, type='Topic', size=c_size, color='#1f77b4')
            
            for ref in refs:
                pdf_node = f"Doc: {ref}"
                G.add_node(pdf_node, type='PDF', size=40, color='#ff7f0e')
                G.add_edge(topico_id, pdf_node, weight=1)
                
        # Layout
        pos = nx.spring_layout(G, k=0.8, seed=42)
        
        # Traces
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_color.append(G.nodes[node]['color'])
            node_size.append(G.nodes[node]['size'])

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[t if 'Doc:' in t else '' for t in node_text], # Solo etiquetas grandes en docs
            textposition="bottom center",
            marker=dict(
                color=node_color,
                size=node_size,
                line_width=2))
        
        node_trace.text = node_text

        fig_graph = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=700,
                    plot_bgcolor='white'
                 ))
        
        st.plotly_chart(fig_graph, use_container_width=True)

# Tab 3: METRICAS
with tabs[2]:
    st.markdown("### Explorador de Datos de Participación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Observaciones (Limpias)", len(df))
    with col2:
        num_clusters = len([c for c in df['Cluster'].unique() if c != -1])
        st.metric("Tópicos Semánticos Detectados", num_clusters)
    with col3:
        ruido = len(df[df['Cluster'] == -1])
        st.metric("Observaciones Anómalas (Ruido)", f"{ruido} ({round(ruido/len(df)*100, 1)}%)")
        
    st.markdown("#### Distribución por Nivel de Complejidad")
    if 'Nivel de compejidad' in df.columns:
        comp_df = df['Nivel de compejidad'].value_counts().reset_index()
        comp_df.columns = ['Complejidad', 'Cantidad']
        fig_bar = px.bar(comp_df, x='Complejidad', y='Cantidad', color='Complejidad', text='Cantidad')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Columna de complejidad no encontrada.")
        
    st.markdown("#### Distribución por Zona")
    if 'ZONA' in df.columns:
        zona_df = df['ZONA'].value_counts().reset_index().head(10)
        zona_df.columns = ['Zona', 'Cantidad']
        fig_pie = px.pie(zona_df, names='Zona', values='Cantidad', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
