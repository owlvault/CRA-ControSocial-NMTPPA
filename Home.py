import streamlit as st

st.set_page_config(
    page_title="CRA - Centro de Análisis NMTPPA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para estilo de tarjetas
st.markdown("""
<style>
    .card {
        border-radius: 10px;
        padding: 20px;
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .card:hover {
        box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .card h3 {
        color: #1f77b4;
        margin-top: 0;
    }
    .card p {
        color: #555;
    }
    /* Estilo modo oscuro por si el usuario lo tiene activado */
    @media (prefers-color-scheme: dark) {
        .card {
            background-color: #1e1e1e;
            border-color: #333;
        }
        .card h3 {
            color: #4da6ff;
        }
        .card p {
            color: #bbb;
        }
    }
</style>
""", unsafe_allow_html=True)


st.title("⚖️ Centro Integrado de Análisis: Control Social NMTPPA")
st.markdown("""
Bienvenido al portal unificado de Inteligencia Artificial para el **Nuevo Marco Tarifario de Pequeños Prestadores de Acueducto (CRA)**. 
Utilice el menú lateral para navegar por las distintas herramientas analíticas diseñadas para el procesamiento de observaciones ciudadanas.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🏛️ Gestión de Respuestas</h3>
        <p>Plataforma para que el equipo jurídico o técnico (Coordinadores) revise los clústeres temáticos y el cruce RAG de la Base Normativa, delegando y priorizando tareas a sus redactores finales.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Gestión de Respuestas", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Gestion_Respuestas.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3>🕸️ Grafos Topológicos</h3>
        <p>Módulo cartográfico para visualizar la dispersión (UMAP 2D) de las participaciones e investigar dinámicamente el grafo relacional entre las opiniones de la ciudadanía y los documentos regulatorios del esquema.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Grafos Topológicos", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Grafos_Topologicos.py")

with col3:
    st.markdown("""
    <div class="card">
        <h3>🔬 Analítica Avanzada</h3>
        <p>Entorno especializado para Científicos de Datos. Contiene proyecciones volumétricas 3D, generador automático TF-IDF de términos frecuentes, cruce de variables (Zonas/Complejidad) y un motor de similitud vectorial profunda.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Analítica Avanzada", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Analitica_Avanzada.py")

with col4:
    st.markdown("""
    <div class="card">
        <h3>⚙️ Panel Admin</h3>
        <p>Gestor de actualizaciones de bases de datos. Permite la carga de nuevos Excel de participación (R40) relanzando todos los modelos de recalibración topológica (NLP) para volver a iterar.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Panel de Administración", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Administracion.py")

st.divider()

st.markdown("### 📚 Información del Proyecto")
st.markdown("""
Este proyecto es producto del despliegue masivo y automatizado de Modelos Languaje Natural (Transformers) sobre 1,701 consultas del sector social.
- **Modelo Vectorial:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Técnicas Matemáticas:** *UMAP* (Reducción Dimensional), *HDBSCAN* (Clustering Algorítmico), y *Cosine Similarity* para la extracción contextual.
""")
