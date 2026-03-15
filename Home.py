import streamlit as st
import os

st.set_page_config(

    page_title="SABIA - Centro Analítico CRA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)
import menu
menu.render_menu()


# Custom CSS estricto SABIA (Heurísticas visuales TDA: Espacio negativo, clean UI)
st.markdown("""
<style>
    /* Fondo limpio y tipografía corporativa CRA */
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* System Cards */
    .card {
        border-radius: 8px;
        padding: 20px;
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 20px;
        transition: all 0.2s ease-in-out;
        height: 100%;
        border-left: 4px solid transparent;
    }
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        border-left: 4px solid #0055A4;
    }
    .card h3 {
        color: #0055A4 !important;
        margin-top: 0;
        font-size: 1.25rem;
    }
    .card p {
        color: #5d6d7e;
        font-size: 0.95rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Logo y Encabezado Principal
col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("⚖️ SABIA: Centro Integrado de Análisis")
    st.markdown("**Sistema de Análisis Basado en Inteligencia Artificial - Control Social NMTPPA**")

st.markdown("""
<p style="font-size: 1.1rem; max-width: 900px; margin-bottom: 2rem;">
Bienvenido al ecosistema unificado de procesamiento normativo. Utilice el menú lateral o el catálogo de módulos a continuación para auditar las participaciones ciudadanas o calibrar los modelos topológicos subyacentes.
</p>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# GRID DE MÓDULOS (DISEÑO LIMPIO)
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🏛️ Gestión de Respuestas</h3>
        <p>Interfaz para que los Coordinadores revisen clústeres temáticos y mapeo RAG. Priorice y asigne bloques de respuesta masiva a los redactores.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Gestión de Respuestas", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Gestion_Respuestas.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3>🕸️ Grafos Topológicos</h3>
        <p>Cartografía de red (Bipartita). Visualice cómo constelaciones de reclamos ciudadanos impactan sobre la Base Normativa histórica de la CRA.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Grafos Topológicos", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Grafos_Topologicos.py")

with col3:
    st.markdown("""
    <div class="card">
        <h3>🔬 Analítica Avanzada</h3>
        <p>Entorno matemático (UMAP/HDBSCAN). Visualice nubes 3D tridimensionales, matrices cruzadas y extraiga vocabularios TF-IDF estocásticos.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Analítica Avanzada", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Analitica_Avanzada.py")

st.markdown("<br>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="card">
        <h3>⚙️ Panel Admin</h3>
        <p>Gestor maestro. Inyecte nueva materia prima (Excel R40), expanda el Acervo Base (PDFs) y reentrene la topología nacional a un solo clic.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Panel de Administración", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Administracion.py")

with col5:
    st.markdown("""
    <div class="card">
        <h3>🩺 Monitor de Calidad</h3>
        <p>Observabilidad TDA. Audite latencias de la memoria caché y confirme que las inferencias jurídicas estén 100% sincronizadas con el input.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Monitor de Calidad", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Monitor_Calidad.py")

with col6:
    st.markdown("""
    <div class="card">
        <h3>🤖 Generador de Borradores</h3>
        <p>Motor LLM estricto (Google Gemini). Emite borradores de respuesta 'Cero Alucinación' basados paramétricamente en los PDF institucionales.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Generador de Borradores", use_container_width=True, type="primary"):
        st.switch_page("pages/6_Generador_Borradores.py")

st.markdown("<br>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("""
    <div class="card">
        <h3>😡 Analizador Térmico</h3>
        <p>Análisis de polaridad semántica. Mida la carga de indignación, fricción técnica o neutralidad de cada subpoblación de la NMTPPA.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Analizador Térmico", use_container_width=True, type="primary"):
        st.switch_page("pages/7_Analisis_Sentimiento.py")

with col8:
    st.markdown("""
    <div class="card">
        <h3>🔬 Explorador Micro-Clúster</h3>
        <p>Zoom Fractal. Aísle un macro-consenso, mutile el resto del país, y recalibre la red neuronal localmente para detectar facciones ocultas.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Explorador de Micro-Clústeres", use_container_width=True, type="primary"):
        st.switch_page("pages/8_Explorador_Microclusters.py")

with col9:
    st.markdown("""
    <div class="card">
        <h3>👤 Consultas Individuales</h3>
        <p>Auditoría de Descarte Topológico. Gestione peticiones solitarias (Outliers) que no se agrupan masivamente pero exigen peritaje jurídico único.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a Consultas Individuales", use_container_width=True, type="primary"):
        st.switch_page("pages/9_Consultas_Individuales.py")

st.divider()

# ==========================================
# FOOTER INSTITUCIONAL
# ==========================================
st.markdown("#### 🏛️ Arquitectura Estructural y Motor Vectorial")
st.markdown("""
Plataforma MLOps operada por algoritmos de vanguardia para la desclasificación ciudadana.
- **Red Neuronal Base:** `paraphrase-multilingual-MiniLM-L12-v2` (Transformer).
- **Reducción Local/Global:** Manifold de Variedad Riemanniana (`UMAP`).
- **Agrupamiento Densimétrico:** Reconocimiento espacial de ruido (`HDBSCAN`).
""")
