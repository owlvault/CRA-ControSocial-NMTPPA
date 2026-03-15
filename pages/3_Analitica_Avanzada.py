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

st.set_page_config(page_title='Análisis de Datos Avanzado - TDA y Semántica', layout='wide')
st.title("🔬 Centro de Análisis Avanzado de Datos: TDA y Modelado de Tópicos")

@st.cache_resource
def load_models():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_models()

@st.cache_data
def process_data():
    import json
    with open('config.json', 'r') as f: config = json.load(f)
    excel_path = config['excel_input']
    df = pd.read_excel(excel_path, sheet_name='REG-FOR03')
    
    df['Consulta'] = df['Consulta'].astype(str)
    df['Consulta_Clean'] = df['Consulta'].astype(str).str.strip().str.replace('\n', ' ')
    df['Consulta_Clean'] = df['Consulta_Clean'].apply(lambda x: re.sub(r'\s+', ' ', x))
    df = df[df['Consulta_Clean'].str.len() > 10].copy().reset_index(drop=True)
    
    # Rellenar valores nulos para el cruce de variables
    for col in ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'Tipo de remitente', 'DEPARTAMENTO']:
        if col in df.columns:
            df[col] = df[col].fillna('No Definido')

    preguntas = df['Consulta_Clean'].tolist()
    embeddings = model.encode(preguntas, show_progress_bar=False)
    
    # Reducción 2D UMAP (Para consistencia y visuales planas, si se requiere)
    reducer_2d = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine', random_state=42)
    umap_2d = reducer_2d.fit_transform(embeddings)
    df['UMAP_X'] = umap_2d[:, 0]
    df['UMAP_Y'] = umap_2d[:, 1]
    
    # Reducción 3D UMAP para visualización tridimensional
    reducer_3d = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=3, metric='cosine', random_state=42)
    umap_3d = reducer_3d.fit_transform(embeddings)
    df['UMAP_3D_X'] = umap_3d[:, 0]
    df['UMAP_3D_Y'] = umap_3d[:, 1]
    df['UMAP_3D_Z'] = umap_3d[:, 2]
    
    # Clustering HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=25, metric='euclidean', cluster_selection_method='eom')
    df['Cluster'] = clusterer.fit_predict(embeddings)
    df['Cluster_Str'] = df['Cluster'].apply(lambda c: "Ruido (-1)" if c == -1 else f"Clúster {c}")
    
    return df, embeddings

with st.spinner('Procesando datos y calculando topología y componentes semánticos...'):
    df, embeddings = process_data()

tab1, tab2, tab3, tab4 = st.tabs([
    "🌌 Espacio Topológico 3D", 
    "🔤 Modelado de Tópicos (TF-IDF)", 
    "📈 Variables Cruzadas",
    "🔍 Motor de Interrogación Vectorial"
])

with tab1:
    st.markdown("### Topología Cuántica de la Participación Ciudadana (Proyección 3D)")
    st.markdown("Inspeccione dimensionalmente las relaciones de los clústeres. Las observaciones cercanas en este cubo tridimensional tienen una alta concordancia semántica.")
    
    fig_3d = px.scatter_3d(
        df, x='UMAP_3D_X', y='UMAP_3D_Y', z='UMAP_3D_Z',
        color='Cluster_Str', 
        hover_data=['ZONA', 'Nivel de compejidad', 'Grupo de Valor'],
        hover_name=df['Consulta_Clean'].str[:80] + '...',
        opacity=0.6,
        color_discrete_sequence=px.colors.qualitative.Alphabet
    )
    fig_3d.update_layout(height=800, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
    st.markdown("### Modelado de Tópicos mediante Frecuencia Termodinámica (TF-IDF)")
    st.markdown("Extracción de las **Top Words** exclusivas de cada clúster para entender rápidamente la esencia conceptual de la agrupación, filtrando el vocabulario institucional estándar (stopwords) de la CRA.")
    
    # Lista de stopwords optimizada para el caso de estudio (incluyendo institucionales)
    stop_words_es = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvimos', 'estuvisteis', 'estuvieron', 'hubo', 'hubieron', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'sean', 'era', 'eran', 'fui', 'fue', 'fueron', 'tengo', 'tiene', 'tienen', 'tenía', 'cra', 'resolución', 'prestadores', 'gestores', 'comunitarios', 'servicio', 'tarifario', 'costos', 'acueducto', 'alcantarillado', 'agua', 'servicios', 'públicos', 'marco', 'proyecto']
    
    def extract_top_words_per_cluster_es(dataframe, text_col='Consulta_Clean', cluster_col='Cluster'):
        clusters = sorted([c for c in dataframe[cluster_col].unique() if c != -1])
        top_words_list = []
        for c in clusters:
            corpus = dataframe[dataframe[cluster_col] == c][text_col].tolist()
            vectorizer = TfidfVectorizer(max_features=25, stop_words=stop_words_es, token_pattern=r'(?u)\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b')
            try:
                X = vectorizer.fit_transform(corpus)
                words = vectorizer.get_feature_names_out()
                scores = X.sum(axis=0).A1
                sorted_idx = scores.argsort()[::-1]
                top_words = [words[i] for i in sorted_idx[:12]]
                top_words_list.append({'Clúster': f"Clúster {c}", 'Frecuencia Documental Inter-Clúster (Top Terms)': ", ".join(top_words)})
            except:
                pass
        return pd.DataFrame(top_words_list)

    df_words = extract_top_words_per_cluster_es(df)
    st.dataframe(df_words, use_container_width=True)

with tab3:
    st.markdown("### Cruce Multivariable e Intersección Dimensional")
    
    colA, colB = st.columns(2)
    with colA:
        var_x = st.selectbox("Eje X (Variable Categórica)", ['ZONA', 'DEPARTAMENTO', 'Grupo de Valor', 'Nivel de compejidad'])
    with colB:
        var_color = st.selectbox("Segmentación (Color)", ['Cluster_Str', 'Nivel de compejidad', 'ZONA', 'Tipo de remitente'])

    fig_mat = px.histogram(df, x=var_x, color=var_color, barmode='stack', title=f"Frecuencia de Observaciones: {var_x} x {var_color}",
                           color_discrete_sequence=px.colors.qualitative.Prism)
    fig_mat.update_layout(height=500)
    st.plotly_chart(fig_mat, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Heatmap Topológico (Concentración de Clústeres por Variable)")
    var_heat = st.selectbox("Variable para Matriz Termal", ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'DEPARTAMENTO'], index=1)
    
    cross_tab = pd.crosstab(df['Cluster_Str'], df[var_heat])
    fig_heat = px.imshow(cross_tab, text_auto=True, color_continuous_scale='Magma', aspect='auto', title=f"Matriz de Calor: Clúster vs {var_heat}")
    fig_heat.update_layout(height=600)
    st.plotly_chart(fig_heat, use_container_width=True)

with tab4:
    st.markdown("### 🔎 Motor de Interrogación Vectorial (Búsqueda Semántica por TDA)")
    st.markdown("Permite a los analistas encontrar participaciones ciudadanas específicas simulando la manera en que el modelo de Machine Learning agrupa el significado.")
    
    query = st.text_input("Búsqueda Semántica de Casos o Inquietudes Específicas:", value="¿Cómo financiar las inversiones usando la tarifa?")
    if st.button("Buscar Similitudes Vectoriales"):
        if query:
            query_emb = model.encode([query])
            sims = cosine_similarity(query_emb, embeddings)[0]
            
            top_indices = sims.argsort()[-15:][::-1]
            
            results = []
            for rank, idx in enumerate(top_indices, 1):
                results.append({
                    'Rank': rank,
                    'Similitud (%)': f"{sims[idx]:.2%}",
                    'Consulta Original': df.iloc[idx]['Consulta_Clean'],
                    'Clúster Asignado': df.iloc[idx]['Cluster_Str'],
                    'Zona': df.iloc[idx]['ZONA'],
                    'Remitente': df.iloc[idx]['Grupo de Valor'],
                    'Complejidad': df.iloc[idx]['Nivel de compejidad']
                })
                
            st.dataframe(pd.DataFrame(results))
