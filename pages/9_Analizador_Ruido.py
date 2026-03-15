import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(page_title="Analizador de Ruido (Outliers)", layout="wide", page_icon="🗑️")

st.title("🗑️ Analizador de Anormalidades y Ruido Matemático")
st.markdown("Herramienta de depuración: Permite a los científicos de datos auditar los casos clasificados como `Clúster -1` (Ruido) por el algoritmo HDBSCAN, para identificar patrones de descarte, anomalías, o recuperar participaciones válidas mal clasificadas.")

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
    st.success("🎉 ¡El algoritmo clasificó el 100% de la matriz en tópicos! No hay ruido o anomalías detectadas en esta ejecución.")
    st.stop()

# --- KPIs y MÉTRICAS GENERALES ---
st.divider()

total_poblacion = len(df_full)
total_ruido = len(df_ruido)
porcentaje_ruido = (total_ruido / total_poblacion) * 100

st.header("1. Auditoría Volumétrica de Descarte")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Participaciones R40", total_poblacion)
with col2:
    st.metric("Casos Catalogados como Ruido (-1)", total_ruido, delta="-Aislados" if total_ruido > 0 else "0", delta_color="inverse")
with col3:
    st.metric("Tasa de Ruido del Modelo (Outliers)", f"{porcentaje_ruido:.1f}%", help="Idealmente debe ser inferior al 25% en NLP no estructurado.")

# --- CARACTERIZACIÓN DEL RUIDO ---
st.divider()
st.header("2. Radiografía del Ruido: ¿De dónde proviene?")

colA, colB = st.columns(2)

with colA:
    st.markdown("#### ¿Quién genera más ruido metodológico?")
    fig_grupo = px.pie(df_ruido, names='Grupo de Valor', title="Ruido por Entidad Origen",
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_grupo.update_layout(height=400)
    st.plotly_chart(fig_grupo, use_container_width=True)

with colB:
    st.markdown("#### Distribución de Ruido por Zonas")
    conteo_zona = df_ruido['ZONA'].value_counts().reset_index()
    conteo_zona.columns = ['ZONA', 'Casos Aislados']
    fig_zona = px.bar(conteo_zona, x='ZONA', y='Casos Aislados', title="Ruido por Regiones NMT",
                      color='ZONA', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_zona.update_layout(height=400)
    st.plotly_chart(fig_zona, use_container_width=True)


# --- EXTRACCIÓN DE PALABRAS DEL RUIDO ---
st.divider()
st.header("3. Análisis Léxico: ¿De qué habla el ruido?")
st.markdown("Incluso en el descarte hay patrones. Conozca las palabras más frecuentes de los comentarios atípicos:")

stop_words_es = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'cra', 'resolución', 'prestadores', 'nmtppa']

corpus_ruido = df_ruido['Consulta'].tolist()

try:
    vectorizer = TfidfVectorizer(max_features=20, stop_words=stop_words_es)
    X = vectorizer.fit_transform(corpus_ruido)
    words = vectorizer.get_feature_names_out()
    scores = X.sum(axis=0).A1
    
    df_tfidf = pd.DataFrame({'Palabra': words, 'Frecuencia': scores}).sort_values(by='Frecuencia', ascending=False)
    
    fig_tfidf = px.bar(df_tfidf.head(10), x='Frecuencia', y='Palabra', orientation='h',
                       title="Top 10 Términos en Observaciones Descartadas",
                       color='Frecuencia', color_continuous_scale='Reds')
    st.plotly_chart(fig_tfidf, use_container_width=True)
except Exception as e:
    st.info("Los textos del ruido son demasiado cortos o incoherentes para formar palabras estructuradas.")

# --- BANDEJA DE AUDITORÍA MANUAL ---
st.divider()
st.header("4. Bandeja de Depuración: ¿Es realmente Ruido?")
st.markdown("El algoritmo descarta por distancia topológica. Revise manualmente la lista de casos atípicos y decida si hay falsos negativos (casos válidos desechados) o si efectivamente son saludos cortos, insultos o caracteres erróneos.")

filtro = st.selectbox("Filtrar ruido por nivel de complejidad (Opcional):", ["Todos"] + list(df_ruido['Nivel de compejidad'].unique()))

if filtro != "Todos":
    df_ver = df_ruido[df_ruido['Nivel de compejidad'] == filtro]
else:
    df_ver = df_ruido

# Visualización con opción de lectura limpia
st.dataframe(df_ver[['Consulta', 'Nivel de compejidad', 'ZONA', 'Grupo de Valor']], use_container_width=True, height=400)

st.info("💡 **Conclusión TDA:** Si el equipo revisa la tabla y nota que son verdaderamente comentarios de 2 palabras (Ej. 'Gracias', 'Sin quejas', 'ok', o reclamos indescifrables), el motor NLP operó correctamente. Si encuentra preguntas muy elaboradas pero únicas, se trata de 'Anomalías Estadísticas Solitarias' que la ley pide igual responder mediante un canal independiente, pero que no conforman un Clúster Nacional.")
