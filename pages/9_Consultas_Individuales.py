import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING SABIA
# ==========================================
st.set_page_config(page_title="SABIA - Consultas Individuales", layout="wide", page_icon="👤")
import menu
menu.render_menu()



st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    .metric-module {
        background-color: #ffffff;
        border-left: 5px solid #D68910;
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
    st.title("👤 SABIA: Auditoría de Consultas Individuales")
    st.markdown("**Bandeja de gestión forense para Casos Atípicos (Ruido Topológico).**")

st.markdown("Plataforma de atención especializada: Administre aquellas observaciones que, por su alta especificidad, no fueron agrupadas nacionalmente pero que por Ley exigen una respuesta formal e individual.")
st.divider()

# ==========================================
# 2. CARGA DE BASE DE DATOS
# ==========================================
CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    return {'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

@st.cache_data
def load_noise_data():
    config = load_config()
    out_path = config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx')
    
    if not os.path.exists(out_path): return None, None
    df = pd.read_excel(out_path, sheet_name='REG-FOR03')
    if 'Cluster TDA (IA)' not in df.columns: return None, None
        
    df['Consulta'] = df['Consulta'].astype(str)
    for col in ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'Tipo de remitente']:
        if col in df.columns: df[col] = df[col].fillna('No Definido')

    df_ruido = df[df['Cluster TDA (IA)'] == -1].copy()
    return df, df_ruido

df_full, df_ruido = load_noise_data()

if df_ruido is None:
    st.warning("⚠️ Módulo inactivo. Compile primero el orquestador TDA en el Panel de Administración.")
    st.stop()

if df_ruido.empty:
    st.success("🎉 ¡Topología Perfecta! El modelo agrupó al 100% del país. Cero consultas aisladas detectadas.")
    st.stop()

# ==========================================
# 3. MÉTRICAS FORENSES
# ==========================================
total_poblacion = len(df_full)
total_ruido = len(df_ruido)
porcentaje_ruido = (total_ruido / max(total_poblacion, 1)) * 100

st.subheader("1. Auditoría Volumétrica de Descarte")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-module">
        <p style="margin:0; font-size:1.1rem">Total Tráfico R40</p>
        <h3 style="margin:0; color:#0055A4">{total_poblacion}</h3>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-module" style="border-left-color: #C0392B;">
        <p style="margin:0; font-size:1.1rem">Casos Únicos (Expedientes)</p>
        <h3 style="margin:0; color:#C0392B">{total_ruido}</h3>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-module">
        <p style="margin:0; font-size:1.1rem">Tasa de Excepción</p>
        <h3 style="margin:0; color:#D68910">{porcentaje_ruido:.1f}%</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================
# 4. CARTOGRAFÍA DE EXCEPCIONES
# ==========================================
st.subheader("2. Demografía de la Singularidad")

colA, colB = st.columns(2)

with colA:
    st.markdown("#### ¿Quién demanda atención 1-a-1?")
    fig_grupo = px.pie(df_ruido, names='Grupo de Valor', hole=0.4,
                       color_discrete_sequence=px.colors.qualitative.Safe)
    fig_grupo.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig_grupo, use_container_width=True)

with colB:
    st.markdown("#### Territorialidad del Descarte")
    conteo_zona = df_ruido['ZONA'].value_counts().reset_index()
    conteo_zona.columns = ['ZONA', 'Casos Aislados']
    fig_zona = px.bar(conteo_zona, x='ZONA', y='Casos Aislados', 
                      color_discrete_sequence=['#F39C12'])
    fig_zona.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig_zona, use_container_width=True)

st.divider()

# ==========================================
# 5. BANDEJA DE AUDITORÍA LEGAL
# ==========================================
st.subheader("3. Bandeja Jurídica de Prioridad")
st.markdown("Expedientes de lectura obligatoria. Estos ciudadanos reclaman derechos, correcciones hiper-territoriales o fallas metodológicas que escapan al consenso general del modelo.")

filtro = st.selectbox("Filtrar auditoría por Nivel de Complejidad:", ["Todos los Casos"] + list(df_ruido['Nivel de compejidad'].unique()))

if filtro != "Todos los Casos": df_ver = df_ruido[df_ruido['Nivel de compejidad'] == filtro]
else: df_ver = df_ruido

st.dataframe(df_ver[['Consulta', 'Nivel de compejidad', 'ZONA', 'Grupo de Valor']], use_container_width=True, height=450, hide_index=True)

st.info("⚖️ **Directriz de Calidad MLOps:** Despache este bloque mediante asignación manual en la Coordinación de Atención al Ciudadano. Las Inteligencias Artificiales Generativas masivas incurrirían en error o sesgo si trataran estos casos sin contexto puntual.")
