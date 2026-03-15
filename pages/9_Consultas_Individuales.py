import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(page_title="Consultas Individuales", layout="wide", page_icon="👤")

st.title("👤 Panel de Consultas Individuales (Casos Atípicos)")
st.markdown("Plataforma de atención especializada: Administre aquellos comentarios y observaciones que, por su alta especificidad o naturaleza única, no fueron agrupados nacionalmente pero que por la Ley de Participación Ciudadana exigen una respuesta formal e individual.")

# --- CARGAR DATOS ---
CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

@st.cache_data
def load_noise_data():
    config = load_config()
    out_path = config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx')
    
    if not os.path.exists(out_path):
        return None, None
        
    df = pd.read_excel(out_path, sheet_name='REG-FOR03')
    
    if 'Cluster TDA (IA)' not in df.columns:
        return None, None
        
    # Extraer el DataFrame completo y solo el ruido
    df['Consulta'] = df['Consulta'].astype(str)
    
    # Manejar variables categoricas
    for col in ['ZONA', 'Nivel de compejidad', 'Grupo de Valor', 'Tipo de remitente']:
        if col in df.columns:
            df[col] = df[col].fillna('No Definido')

    df_ruido = df[df['Cluster TDA (IA)'] == -1].copy()
    
    return df, df_ruido

df_full, df_ruido = load_noise_data()

if df_ruido is None:
    st.warning("⚠️ No se encontró la Matriz de Resultados. Asegúrate de generar el Excel Final en el Administrador.")
    st.stop()

if df_ruido.empty:
    st.success("🎉 ¡El modelo logró clusterizar a todo el país! No quedaron consultas aisladas sin respuesta masiva.")
    st.stop()

# --- KPIs y MÉTRICAS GENERALES ---
st.divider()

total_poblacion = len(df_full)
total_ruido = len(df_ruido)
porcentaje_ruido = (total_ruido / total_poblacion) * 100

st.header("1. Auditoría Volumétrica Individual")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Participaciones R40", total_poblacion)
with col2:
    st.metric("Consultas Únicas Aisladas (-1)", total_ruido, delta="-Aislados" if total_ruido > 0 else "0", delta_color="inverse")
with col3:
    st.metric("Tasa de Individualidad", f"{porcentaje_ruido:.1f}%", help="Porcentaje de la participación que requirió separación del consenso masivo.")

# --- CARACTERIZACIÓN DEL RUIDO ---
st.divider()
st.header("2. Radiografía de Participaciones Únicas: ¿De dónde provienen?")

colA, colB = st.columns(2)

with colA:
    st.markdown("#### ¿Quién genera más consultas altamente específicas?")
    fig_grupo = px.pie(df_ruido, names='Grupo de Valor', title="Casos Atípicos por Entidad Origen",
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_grupo.update_layout(height=400)
    st.plotly_chart(fig_grupo, use_container_width=True)

with colB:
    st.markdown("#### Distribución Territorial de Casos Únicos")
    conteo_zona = df_ruido['ZONA'].value_counts().reset_index()
    conteo_zona.columns = ['ZONA', 'Casos Aislados']
    fig_zona = px.bar(conteo_zona, x='ZONA', y='Casos Aislados', title="Casos Individuales por Regiones NMT",
                      color='ZONA', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_zona.update_layout(height=400)
    st.plotly_chart(fig_zona, use_container_width=True)


# --- EXTRACCIÓN DE PALABRAS DEL RUIDO ---
st.divider()
st.header("3. Análisis Léxico: ¿Qué temas abordan?")
st.markdown("Aunque no formen un clúster nacional, estos son los términos más usados por los ciudadanos aislados:")

stop_words_es = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'cra', 'resolución', 'prestadores', 'nmtppa']

corpus_ruido = df_ruido['Consulta'].tolist()

try:
    vectorizer = TfidfVectorizer(max_features=20, stop_words=stop_words_es)
    X = vectorizer.fit_transform(corpus_ruido)
    words = vectorizer.get_feature_names_out()
    scores = X.sum(axis=0).A1
    
    df_tfidf = pd.DataFrame({'Palabra': words, 'Frecuencia': scores}).sort_values(by='Frecuencia', ascending=False)
    
    fig_tfidf = px.bar(df_tfidf.head(10), x='Frecuencia', y='Palabra', orientation='h',
                       title="Top 10 Términos en Consultas Individuales",
                       color='Frecuencia', color_continuous_scale='Blues')
    st.plotly_chart(fig_tfidf, use_container_width=True)
except Exception as e:
    st.info("Los textos asilados son demasiado heterogéneos para estructurar un vocabulario unificado.")

# --- BANDEJA DE AUDITORÍA MANUAL ---
st.divider()
st.header("4. Bandeja Gestora de Respuestas Individuales")
st.markdown("El equipo jurídico debe evaluar este listado tabular. Aquí reposan peticiones con reclamos legales precisos, derechos de petición únicos o casos hiper-territoriales que no admiten la respuesta estándar de los Clústeres Nacionales.")

filtro = st.selectbox("Filtrar casos por nivel de complejidad (Opcional):", ["Todos"] + list(df_ruido['Nivel de compejidad'].unique()))

if filtro != "Todos":
    df_ver = df_ruido[df_ruido['Nivel de compejidad'] == filtro]
else:
    df_ver = df_ruido

# Visualización con opción de lectura limpia
st.dataframe(df_ver[['Consulta', 'Nivel de compejidad', 'ZONA', 'Grupo de Valor']], use_container_width=True, height=400)

st.info("💡 **Instrucción Legal:** Estos casos deben ser delegados al equipo de Apoyo Jurídico para su lectura y redacción uno-a-uno. No utilice plantillas masivas ('Clústeres') para este segmento.")
