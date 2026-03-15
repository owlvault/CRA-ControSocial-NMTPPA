import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING SABIA
# ==========================================
st.set_page_config(page_title="SABIA - Analizador Térmico", layout="wide", page_icon="😡")
import menu
menu.render_menu()



st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* Configuración de Cajas de Redacción / Alertas */
    .metric-module {
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-module h4 { color: #5d6d7e !important; font-size: 1rem; margin-bottom: 5px; }
    .metric-module p { font-family: 'Inter', sans-serif; font-size: 1.8rem; font-weight: 700; color: #0055A4; margin:0;}
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("😡 SABIA: Analizador Lingüístico Térmico")
    st.markdown("**Clasificador de polaridad semántica ciudadana.**")

st.markdown("Mide el nivel de fricción, indignación o neutralidad de los ciudadanos agrupados por Clúster. Ayuda al equipo jurídico a calibrar la empatía diplomática o la firmeza regulatoria requerida en cada borrador de respuesta.")
st.divider()

# ==========================================
# 2. CARGA DEL LAKEHOUSE
# ==========================================
CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    return {'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

@st.cache_data
def load_and_analyze_data():
    config = load_config()
    out_path = config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx')
    
    if not os.path.exists(out_path): return None
    df = pd.read_excel(out_path, sheet_name='REG-FOR03')
    if 'Cluster TDA (IA)' not in df.columns: return None
        
    df_valido = df[df['Cluster TDA (IA)'] != -1].copy()
    
    # Análisis Lexical Estático (Proxy determinístico en lugar de LLM para velocidad)
    terminos_criticos = ['injusto', 'robo', 'demasiado', 'mentira', 'fraude', 'imposible', 'exagerado', 'caro', 'abuso', 'queja', 'denuncia', 'desacuerdo', 'perjuicio', 'daño', 'corrupción', 'ineficiente', 'mal']
    terminos_positivos = ['excelente', 'gracias', 'mejora', 'acuerdo', 'felicito', 'oportunidad', 'apoyo', 'claro', 'buen', 'beneficio', 'correcto', 'útil']
    
    def calcular_friccion(texto):
        texto = str(texto).lower()
        score_critico = sum([1 for word in terminos_criticos if word in texto])
        score_positivo = sum([1 for word in terminos_positivos if word in texto])
        
        if score_critico == 0 and score_positivo == 0: return "Neutral / Informativo 🟢"
        elif score_critico > score_positivo:
            if score_critico > 2: return "Indignación Alta 🔴"
            return "Tensión Moderada 🟡"
        else: return "Recepción Positiva 🔵"
             
    def calcular_score_numerico(texto):
        texto = str(texto).lower()
        return sum([1 for word in terminos_positivos if word in texto]) - sum([1 for word in terminos_criticos if word in texto])

    df_valido['Sentimiento'] = df_valido['Consulta'].apply(calcular_friccion)
    df_valido['Score'] = df_valido['Consulta'].apply(calcular_score_numerico)
    
    return df_valido

df = load_and_analyze_data()

if df is None:
    st.warning("⚠️ No se detectó la matriz de Excel procesada. Acuda a 'Panel Admin' para compilarla.")
    st.stop()

# ==========================================
# 3. INTERFAZ Y DASHBOARD TÉRMICO
# ==========================================
total_casos = len(df)
conteo = df['Sentimiento'].value_counts()
criticos = conteo.get("Indignación Alta 🔴", 0)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-module">
        <h4>Volumen Lingüístico Auditable</h4>
        <p>{total_casos}</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-module">
        <h4>Tasa de Indignación Crítica</h4>
        <p style="color:#d62728 !important;">{(criticos/max(total_casos,1))*100:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-module">
        <h4>Temperamento Dominante Institucional</h4>
        <p style="font-size:1.4rem;">{conteo.idxmax()}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

col_map, col_list = st.columns([2, 1])

# Paleta Térmica Oficial SABIA
color_discrete_map = {
    "Indignación Alta 🔴": "#C0392B",  # Dark Red
    "Tensión Moderada 🟡": "#F39C12",  # Warning Orange
    "Neutral / Informativo 🟢": "#7F8C8D", # Neutral Gray
    "Recepción Positiva 🔵": "#2980B9"   # Trust Blue
}

with col_map:
    st.subheader("🌋 Termografía de Sentimiento por Tópico (Clúster)")
    
    df_plot = df.groupby(['Tema Central IA', 'Sentimiento']).size().reset_index(name='Cantidad')
    
    fig = px.bar(df_plot, x="Tema Central IA", y="Cantidad", color="Sentimiento", 
                 color_discrete_map=color_discrete_map, barmode='stack')
                 
    fig.update_layout(
        xaxis_tickangle=-45, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        height=500, margin=dict(b=150)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_list:
    st.subheader("🚨 Casos Críticos de Fricción")
    st.markdown("Escaneo forense de los textos que requieren atención jurídica y diplomática inmediata para evitar daño reputacional o legal a la CRA.")
    
    alertas = df[df['Sentimiento'] == "Indignación Alta 🔴"]
    if not alertas.empty:
        alertas_top = alertas.sample(min(8, len(alertas)))
        for _, row in alertas_top.iterrows():
            with st.expander(f"📍 Clúster {row['Cluster TDA (IA)']}"):
                st.write(f"_{str(row['Consulta'])[:250]}..._")
                st.caption(f"🛡️ Clasificación Semántica: **{row['Sentimiento']}**")
    else:
        st.success("🎉 Cero incidencias críticas reportadas en el corpus ciudadano actual.")

st.divider()

st.subheader("🔍 Buscador Térmico Subterráneo")
st.markdown("Introduzca un concepto sensible (ej. *'costos'*, *'finca'* o *'estrato'*) para destilar la curva térmica exclusiva de esa palabra.")
busqueda = st.text_input("Ingresar término de búsqueda forense:", placeholder="Ej: subsidio, tarifa, medidor...")

if busqueda:
    mask = df['Consulta'].astype(str).str.contains(busqueda, case=False, na=False)
    resultados = df[mask]
    
    if len(resultados) > 0:
        st.info(f"El analizador interceptó **{len(resultados)}** menciones vinculadas al término buscado.")
        
        pie = px.pie(resultados, names='Sentimiento', color='Sentimiento', color_discrete_map=color_discrete_map)
        pie.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        
        col_pie, col_data = st.columns([1, 2])
        with col_pie:
            st.plotly_chart(pie)
        with col_data:
            st.dataframe(resultados[['Consulta', 'Tema Central IA', 'Sentimiento']].head(15), use_container_width=True, hide_index=True)
    else:
        st.warning(f"La palabra '{busqueda}' no se encuentra registrada en el volumen nacional actual.")
