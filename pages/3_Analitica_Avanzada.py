import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sentence_transformers import SentenceTransformer
import hdbscan
import umap
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
import json

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING
# ==========================================
st.set_page_config(page_title='SABIA - Analítica Avanzada', layout='wide', page_icon='🔬')
import menu
menu.render_menu()



# Inyección de CSS (Heurísticas visuales TDA: Espacio negativo, colores corporativos, tablas legibles)
st.markdown("""
<style>
    /* Fondo limpio y tipografía de alto contraste */
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div { color: #2C3E50; }
    
    /* Tablas con números tabulares para lectura de métricas */
    [data-testid="stDataFrame"] { font-variant-numeric: tabular-nums; }
    
    /* Diseño de tarjetas métricas limpias */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# Logo y Título Principal
col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("🔬 SABIA: Analítica Avanzada TDA")
    st.markdown("**Sistema de Análisis Basado en Inteligencia Artificial - Participación NMTPPA**")

# ==========================================
# 2. ARQUITECTURA UX: DIVULGACIÓN PROGRESIVA
# ==========================================
st.sidebar.markdown("### ⚙️ Panel de Control")
modo_cientifico = st.sidebar.toggle("Modo Científico de Datos", value=False, help="Revela hiperparámetros estocásticos y controles estructurales del grafo.")

# Hiperparámetros dinámicos (Ocultos por defecto para el equipo jurídico)
if modo_cientifico:
    st.sidebar.markdown("#### Hiperparámetros TDA")
    n_neighbors_umap = st.sidebar.slider("UMAP n_neighbors", 5, 50, 15, help="Balance entre estructura local vs global.")
    min_dist_umap = st.sidebar.slider("UMAP min_dist", 0.0, 0.5, 0.1, help="Separación física de los puntos en la proyección.")
    min_cluster_hdbscan = st.sidebar.slider("HDBSCAN min_cluster_size", 5, 100, 25, help="Masa crítica mínima para considerar una agrupación como Clúster.")
else:
    n_neighbors_umap = 15
    min_dist_umap = 0.1
    min_cluster_hdbscan = 25
    st.sidebar.info("La vista está optimizada para análisis ejecutivo. Active el Modo Científico para calibrar el modelo.")

# ==========================================
# 3. NÚCLEO MATEMÁTICO Y CACHÉ
# ==========================================
@st.cache_resource
def load_models():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_models()

@st.cache_data(show_spinner=False)
def process_data(n_neigh, m_dist, min_cs):
    config_path = 'config.json'
    excel_path = 'R40 AAPP - FINAL - Marzo 13.xlsx' # Default
    if os.path.exists(config_path):
        with open(config_path, 'r') as f: 
            config = json.load(f)
            excel_path = config.get('excel_input', excel_path)
            
    try:
        df = pd.read_excel(excel_path, sheet_name='REG-FOR03')
    except:
        return None, None

    df['Consulta'] = df['Consulta'].astype(str)
    df['Consulta_Clean'] = df['Consulta'].str.strip().str.replace('\n', ' ')
    df['Consulta_Clean'] = df['Consulta_Clean'].apply(lambda x: re.sub(r'\s+', ' ', x))
    df = df[df['Consulta_Clean'].str.len() > 10].copy().reset_index(drop=True)
    
    for col in ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'Tipo de remitente', 'DEPARTAMENTO']:
        if col in df.columns:
            df[col] = df[col].fillna('No Definido')

    preguntas = df['Consulta_Clean'].tolist()
    embeddings = model.encode(preguntas, show_progress_bar=False)
    
    # Reducción 3D UMAP
    reducer_3d = umap.UMAP(n_neighbors=n_neigh, min_dist=m_dist, n_components=3, metric='cosine', random_state=42)
    umap_3d = reducer_3d.fit_transform(embeddings)
    df['UMAP_3D_X'] = umap_3d[:, 0]
    df['UMAP_3D_Y'] = umap_3d[:, 1]
    df['UMAP_3D_Z'] = umap_3d[:, 2]
    
    # Clustering HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cs, metric='euclidean', cluster_selection_method='eom')
    df['Cluster'] = clusterer.fit_predict(embeddings)
    df['Cluster_Str'] = df['Cluster'].apply(lambda c: "Atípicos (-1)" if c == -1 else f"Clúster {c}")
    
    return df, embeddings

with st.spinner('Ensamblando topología y espacio vectorial...'):
    df, embeddings = process_data(n_neighbors_umap, min_dist_umap, min_cluster_hdbscan)

if df is None:
    st.error("No se pudo cargar la Matriz de Origen (R40). Verifique el Panel Admin.")
    st.stop()

# ==========================================
# 4. CAPA DE PRESENTACIÓN (TABS)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🌌 Espacio Topológico 3D", 
    "📈 Cruces Multivariables",
    "🔤 Modelado de Tópicos (TF-IDF)", 
    "🔍 Interrogación Vectorial"
])

with tab1:
    st.subheader("Topología Cuántica de la Participación Ciudadana")
    if not modo_cientifico:
        st.markdown("Observe las constelaciones de participación regulatoria. Puntos aglomerados significan un consenso ciudadano masivo, indicando áreas donde la regulación genera debates unificados.")
        
    # Paleta Científica Segura (Plasma/Viridis/Blues)
    color_scale = px.colors.qualitative.Prism if modo_cientifico else px.colors.qualitative.Safe
    
    fig_3d = px.scatter_3d(
        df, x='UMAP_3D_X', y='UMAP_3D_Y', z='UMAP_3D_Z',
        color='Cluster_Str', 
        hover_data=['ZONA', 'Nivel de compejidad', 'Grupo de Valor'],
        hover_name=df['Consulta_Clean'].str[:80] + '...',
        opacity=0.7,
        color_discrete_sequence=color_scale
    )
    
    # Limpiando la cuadrícula para maximizar Data-to-Ink ratio
    fig_3d.update_layout(
        height=700, margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(xaxis_showspikes=False, yaxis_showspikes=False, zaxis_showspikes=False,
                   xaxis_backgroundcolor="#F8FBFF", yaxis_backgroundcolor="#F8FBFF", zaxis_backgroundcolor="#F8FBFF")
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
    st.subheader("Cruce Multivariable e Intersección Dimensional")
    
    colA, colB = st.columns(2)
    with colA:
        var_x = st.selectbox("Eje X (Variable Categórica)", ['ZONA', 'DEPARTAMENTO', 'Grupo de Valor', 'Nivel de compejidad'])
    with colB:
        var_color = st.selectbox("Segmentación (Color)", ['Cluster_Str', 'Nivel de compejidad', 'ZONA', 'Tipo de remitente'])

    # Histograma limpio
    fig_mat = px.histogram(df, x=var_x, color=var_color, barmode='stack', title=f"Frecuencia de Observaciones: {var_x} x {var_color}",
                           color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_mat.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Volumen de Casos")
    st.plotly_chart(fig_mat, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Matriz Termal de Concentración")
    var_heat = st.selectbox("Dimensión a cruzar con Clústeres", ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'DEPARTAMENTO'], index=1)
    
    cross_tab = pd.crosstab(df['Cluster_Str'], df[var_heat])
    # Uso obligado de mapa perceptualmente uniforme
    fig_heat = px.imshow(cross_tab, text_auto=True, color_continuous_scale='Viridis', aspect='auto')
    fig_heat.update_layout(height=600, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    st.subheader("Lexicón: Frecuencia Termodinámica (TF-IDF)")
    if modo_cientifico:
         top_n_terms = st.slider("Términos por Clúster", 5, 20, 10)
    else:
         top_n_terms = 8
         st.markdown("Extracción de las palabras exclusivas de cada agrupación, filtrando el vocabulario institucional estándar de la CRA.")
    
    stop_words_es = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'cra', 'resolución', 'prestadores', 'servicio', 'tarifario', 'costos', 'acueducto', 'agua', 'servicios', 'públicos', 'marco']
    
    def extract_top_words(dataframe, n_terms):
        clusters = sorted([c for c in dataframe['Cluster'].unique() if c != -1])
        top_words_list = []
        for c in clusters:
            corpus = dataframe[dataframe['Cluster'] == c]['Consulta_Clean'].tolist()
            if len(corpus) < 3: continue
            vectorizer = TfidfVectorizer(max_features=n_terms*2, stop_words=stop_words_es, token_pattern=r'(?u)\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b')
            try:
                X = vectorizer.fit_transform(corpus)
                words = vectorizer.get_feature_names_out()
                scores = X.sum(axis=0).A1
                sorted_idx = scores.argsort()[::-1]
                top_words = [words[i] for i in sorted_idx[:n_terms]]
                top_words_list.append({'Clúster Analizado': f"Clúster {c}", 'ADN Semántico (Términos)': " • ".join(top_words)})
            except: pass
        return pd.DataFrame(top_words_list)

    df_words = extract_top_words(df, top_n_terms)
    st.dataframe(df_words, use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🔎 Búsqueda Semántica Vectorial")
    st.markdown("Localice participaciones utilizando el motor de inferencia matemática, el cual comprende el contexto (no solo la palabra exacta).")
    
    query = st.text_input("Ingrese la inquietud jurídica o técnica:", value="¿Cómo se impacta la tarifa por inversiones?")
    
    if st.button("Buscar en la Matriz Dimensional", type="primary"):
        if query:
            query_emb = model.encode([query])
            sims = cosine_similarity(query_emb, embeddings)[0]
            top_indices = sims.argsort()[-15:][::-1]
            
            results = []
            for rank, idx in enumerate(top_indices, 1):
                results.append({
                    'Similitud': f"{sims[idx]:.1%}",
                    'Consulta Ciudadana': df.iloc[idx]['Consulta_Clean'],
                    'Clasificación': df.iloc[idx]['Cluster_Str'],
                    'Origen': df.iloc[idx]['ZONA'],
                    'Complejidad': df.iloc[idx]['Nivel de compejidad']
                })
            
            res_df = pd.DataFrame(results)
            st.dataframe(res_df, use_container_width=True, hide_index=True)
