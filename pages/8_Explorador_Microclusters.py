import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Micro-Clustering (Deep Dive)", layout="wide", page_icon="🔬")

st.title("🔬 Explorador de Micro-Clústeres (Deep Dive TDA)")
st.markdown("Herramienta sociológica avanzada: Permite a los científicos de datos tomar un Clúster masivo (Ej. 300 personas) y aplicar recursivamente un **segundo zoom topológico** para descubrir sub-facciones, matices o demandas ocultas específicas de ese único grupo.")

# --- CARGAR DATOS ---
CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

@st.cache_resource
def load_sentence_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_sentence_model()

@st.cache_data
def load_data():
    config = load_config()
    out_path = config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx')
    
    if not os.path.exists(out_path):
        return None
        
    df = pd.read_excel(out_path, sheet_name='REG-FOR03')
    
    if 'Cluster TDA (IA)' not in df.columns:
        return None
        
    # Filtrar solo asignados
    df_valido = df[df['Cluster TDA (IA)'] != -1].copy()
    
    # Rellenar vars
    for col in ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'Tema Central IA']:
        if col in df_valido.columns:
            df_valido[col] = df_valido[col].fillna('No Definido')
    
    return df_valido

df = load_data()

if df is None:
    st.warning("⚠️ Matriz de Resultados no encontrada. Genera el Excel primero.")
    st.stop()

# --- HEADER INTERACTIVO ---
st.divider()

clusters_unicos = sorted(df['Cluster TDA (IA)'].unique())
nombres_temas = {c: df[df['Cluster TDA (IA)'] == c]['Tema Central IA'].iloc[0][:50] + "..." for c in clusters_unicos}

opciones_select = [f"Clúster {c} - {nombres_temas[c]}" for c in clusters_unicos]

colA, colB = st.columns([1, 2])
with colA:
    st.markdown("### 1. Seleccionar Macro-Clúster")
    seleccion = st.selectbox("Elija el continente a explorar:", opciones_select)
    
    cluster_idx = int(seleccion.split(' - ')[0].replace('Clúster ', ''))
    
    df_sub = df[df['Cluster TDA (IA)'] == cluster_idx].copy()
    
    st.info(f"Población Aislada: **{len(df_sub)}** participaciones ciudadanas.")

# --- LÓGICA DE MICRO-CLUSTERING EN VIVO ---
with colB:
    st.markdown("### 2. Parámetros de Resonancia Magnética (K-Means Local)")
    st.markdown("Dividiremos esta población internamente. Ajuste cuántas facciones (Sub-Grupos) sospecha que existen dentro de este tema.")
    
    num_micro = st.slider("Número de Micro-Clústeres deseados:", min_value=2, max_value=8, value=3)
    
    if st.button("🧬 Ejecutar Deep Dive Topológico", type="primary"):
        with st.spinner("Aislando el clúster, re-vectorizando a 384 dimensiones y calculando sub-centroides..."):
            from sklearn.cluster import KMeans
            import umap
            
            # Vectorizar solo este dataframe aisldo
            textos = df_sub['Consulta'].astype(str).tolist()
            emb_sub = model.encode(textos, show_progress_bar=False)
            
            # Sub-Clustering K-Means para segmentacion dura
            kmeans = KMeans(n_clusters=num_micro, random_state=42, n_init=10)
            df_sub['Micro_Cluster'] = kmeans.fit_predict(emb_sub)
            df_sub['Micro_Cluster_Str'] = "Matiz " + df_sub['Micro_Cluster'].astype(str)
            
            # Sub-UMAP 2D exclusivo para este cluster
            reducer = umap.UMAP(n_neighbors=min(15, len(df_sub)-1), min_dist=0.01, n_components=2, metric='cosine', random_state=42)
            umap_sub = reducer.fit_transform(emb_sub)
            df_sub['UMAP_X'] = umap_sub[:, 0]
            df_sub['UMAP_Y'] = umap_sub[:, 1]
            
            st.session_state['df_sub_analyzed'] = df_sub
            st.session_state['centers'] = kmeans.cluster_centers_
            st.session_state['emb_sub'] = emb_sub
            st.session_state['kmeans_labels'] = df_sub['Micro_Cluster'].tolist()

st.divider()

# --- RESULTADOS VISUALES ---
if 'df_sub_analyzed' in st.session_state:
    df_res = st.session_state['df_sub_analyzed']
    
    col_plot, col_data = st.columns([1.5, 1])
    
    with col_plot:
        st.subheader("Micro-Topología (Isla Aislada)")
        st.markdown("Observe las fronteras internas o facciones dentro del Macro-Tópico.")
        
        fig = px.scatter(df_res, x='UMAP_X', y='UMAP_Y', color='Micro_Cluster_Str',
                         hover_data=['ZONA', 'Nivel de compejidad'],
                         hover_name=df_res['Consulta'].str[:60] + '...',
                         title=f"Sub-facciones del Clúster {cluster_idx}",
                         color_discrete_sequence=px.colors.qualitative.Bold,
                         template='plotly_white')
        
        fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_data:
        st.subheader("Lexicón de Facciones")
        st.markdown("¿De qué habla cada sub-grupo exactamente?")
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        stop_words_es = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'cra', 'resolución', 'prestadores']
        
        micro_clusters = sorted(df_res['Micro_Cluster'].unique())
        for mc in micro_clusters:
            corpus = df_res[df_res['Micro_Cluster'] == mc]['Consulta'].astype(str).tolist()
            if len(corpus) > 0:
                vectorizer = TfidfVectorizer(max_features=5, stop_words=stop_words_es)
                try:
                    X = vectorizer.fit_transform(corpus)
                    words = vectorizer.get_feature_names_out()
                    scores = X.sum(axis=0).A1
                    top_words = [words[i] for i in scores.argsort()[::-1]]
                    
                    st.info(f"**Matiz {mc}** ({len(corpus)} personas)\nPalabras Clave: {', '.join(top_words)}")
                except:
                     st.info(f"**Matiz {mc}** ({len(corpus)} personas)\nTextos muy cortos o genéricos.")

    st.subheader("Bandeja de Entrada Detallada de la Facción")
    matiz_seleccionado = st.selectbox("Seleccione un Sub-Grupo para leer los casos puros:", 
                                      [f"Matiz {m}" for m in micro_clusters])
    
    matiz_idx = int(matiz_seleccionado.replace("Matiz ", ""))
    
    casos = df_res[df_res['Micro_Cluster'] == matiz_idx]
    
    st.dataframe(casos[['Consulta', 'ZONA', 'Nivel de compejidad', 'Grupo de Valor']], use_container_width=True)
