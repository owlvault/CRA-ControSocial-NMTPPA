import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from sentence_transformers import SentenceTransformer

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING SABIA
# ==========================================
st.set_page_config(page_title="SABIA - Explorador de Micro-Clústeres", layout="wide", page_icon="🔬")
import menu
menu.render_menu()



st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* Configuración de inputs y metricas limpias */
    div.stSelectbox > div > div { background-color: #ffffff; border-color: #0055A4; }
    
    .metric-module {
        background-color: #ffffff;
        border-left: 5px solid #0055A4;
        border-radius: 4px;
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
    st.title("🔬 SABIA: Lente Fractal de Micro-Clústeres")
    st.markdown("**Deep Dive TDA. Detección de sub-facciones y disidencias estructurales.**")

st.markdown("Herramienta sociológica avanzada: Permite aislar un Macro-Clúster (Ej. 300 personas) y aplicar recursivamente un **segundo zoom topológico** (K-Means/UMAP local) para descubrir matices o demandas ocultas en dicha agrupación poblacional.")
st.divider()

# ==========================================
# 2. MOTOR MATEMÁTICO (ISOLATION)
# ==========================================
CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    return {'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

@st.cache_resource
def load_sentence_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_sentence_model()

@st.cache_data
def load_data():
    config = load_config()
    out_path = config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx')
    
    if not os.path.exists(out_path): return None
    df = pd.read_excel(out_path, sheet_name='REG-FOR03')
    if 'Cluster TDA (IA)' not in df.columns: return None
        
    df_valido = df[df['Cluster TDA (IA)'] != -1].copy()
    
    for col in ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'Tema Central IA']:
        if col in df_valido.columns: df_valido[col] = df_valido[col].fillna('No Definido')
    
    return df_valido

df = load_data()

if df is None:
    st.warning("⚠️ No se ha detectado Topología base. Construya la matriz desde el Panel de Administración.")
    st.stop()

# ==========================================
# 3. INTERFAZ DE NAVEGACIÓN FRACTAL
# ==========================================
clusters_unicos = sorted(df['Cluster TDA (IA)'].unique())
nombres_temas = {c: df[df['Cluster TDA (IA)'] == c]['Tema Central IA'].iloc[0][:50] + "..." for c in clusters_unicos}
opciones_select = [f"Macro-Tópico {c} - {nombres_temas[c]}" for c in clusters_unicos]

colA, colB = st.columns([1, 2])
with colA:
    st.markdown("### 1. Seleccionar Macro-Tópico")
    seleccion = st.selectbox("Apuntar Microscopio Analítico hacia:", opciones_select)
    
    cluster_idx = int(seleccion.split(' - ')[0].replace('Macro-Tópico ', ''))
    df_sub = df[df['Cluster TDA (IA)'] == cluster_idx].copy()
    
    st.markdown(f"""
    <div class="metric-module">
        <p style="margin:0; font-size:1.1rem">Masa Demográfica Aislada</p>
        <h3 style="margin:0; color:#0055A4">{len(df_sub)} Participaciones</h3>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("### 2. Fracturación de la Sub-Masa (K-Means Local)")
    st.markdown("Parametriza el nivel de fricción interna. ¿Cuántas sub-facciones crees que componen este grupo?")
    
    col_sli, col_btn = st.columns([2, 1])
    with col_sli:
        num_micro = st.slider("Descomposición K (Sub-Centroides):", min_value=2, max_value=8, value=3)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧬 Ejecutar Lente Topológico", type="primary", use_container_width=True):
            with st.spinner("Descomponiendo tensores y recalibrando K-Means local..."):
                from sklearn.cluster import KMeans
                import umap
                
                textos = df_sub['Consulta'].astype(str).tolist()
                emb_sub = model.encode(textos, show_progress_bar=False)
                
                kmeans = KMeans(n_clusters=num_micro, random_state=42, n_init=10)
                df_sub['Micro_Cluster'] = kmeans.fit_predict(emb_sub)
                df_sub['Micro_Cluster_Str'] = "Facción " + df_sub['Micro_Cluster'].astype(str)
                
                reducer = umap.UMAP(n_neighbors=min(15, len(df_sub)-1), min_dist=0.01, n_components=2, metric='cosine', random_state=42)
                umap_sub = reducer.fit_transform(emb_sub)
                df_sub['UMAP_X'] = umap_sub[:, 0]
                df_sub['UMAP_Y'] = umap_sub[:, 1]
                
                st.session_state['df_sub_analyzed'] = df_sub

st.divider()

# ==========================================
# 4. TABLERO DE RESULTADOS MICRO
# ==========================================
if 'df_sub_analyzed' in st.session_state:
    df_res = st.session_state['df_sub_analyzed']
    col_plot, col_data = st.columns([1.5, 1])
    
    with col_plot:
        st.subheader(f"🗺️ Cartografía Sub-Espacial (Macro-Tópico {cluster_idx})")
        
        fig = px.scatter(df_res, x='UMAP_X', y='UMAP_Y', color='Micro_Cluster_Str',
                         hover_data=['ZONA', 'Nivel de compejidad'],
                         hover_name=df_res['Consulta'].str[:60] + '...',
                         color_discrete_sequence=px.colors.qualitative.Prism)
        
        fig.update_layout(
            height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=0,r=0,b=0,t=0)
        )
        
        fig.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=1, color='#ffffff')))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_data:
        st.subheader("🧬 ADN Lexical de Facciones")
        st.markdown("Intersección estocástica para revelar de qué habla cada sub-grupo.")
        
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
                    
                    st.success(f"**Facción {mc}** ({len(corpus)} ciudadanos)\n👉 {', '.join(top_words)}")
                except:
                     st.info(f"**Facción {mc}** ({len(corpus)} ciudadanos) - Vocabulario genérico.")

    st.subheader("📚 Matriz Cruda Filtrada por Facción")
    matiz_seleccionado = st.selectbox("Filtrar Matriz Original por Sub-Grupo:", 
                                      [f"Facción {m}" for m in micro_clusters])
    
    matiz_idx = int(matiz_seleccionado.replace("Facción ", ""))
    casos = df_res[df_res['Micro_Cluster'] == matiz_idx]
    
    st.dataframe(casos[['Consulta', 'ZONA', 'Nivel de compejidad', 'Grupo de Valor']], use_container_width=True, hide_index=True)
