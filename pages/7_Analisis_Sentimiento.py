import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

st.set_page_config(page_title="Analizador Térmico de Sentimiento", layout="wide", page_icon="😡")

st.title("😡 Analizador Térmico de Sentimiento y Tono")
st.markdown("Clasificador Lingüístico: Mide el nivel de fricción, indignación o neutralidad de los ciudadanos agrupados por Clúster. Ayuda al área jurídica a calibrar el nivel de empatía o firmeza requerido en su respuesta.")

# --- CARGAR DATOS ---
CONFIG_FILE = 'config.json'
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'excel_output': 'R40 AAPP - RESULTADOS TDA.xlsx'}

@st.cache_data
def load_and_analyze_data():
    config = load_config()
    out_path = config.get('excel_output', 'R40 AAPP - RESULTADOS TDA.xlsx')
    
    if not os.path.exists(out_path):
        return None
        
    df = pd.read_excel(out_path, sheet_name='REG-FOR03')
    
    # Asegurar que hay clústeres procesados
    if 'Cluster TDA (IA)' not in df.columns:
        return None
        
    df_valido = df[df['Cluster TDA (IA)'] != -1].copy()
    
    # Analisis Lexical de cada frase usando TextBlob (Traduciendo el concepto al español asumiendo q Textblob calcula polarity internamente)
    # Nota: Textblob base es para ingles. Para español usamos un proxy linguistico rapido o la traduccion integrada si es posible.
    # Alternativa segura y rápida local para terminos fuertes:
    
    terminos_criticos = ['injusto', 'robo', 'demasiado', 'mentira', 'fraude', 'imposible', 'exagerado', 'caro', 'abuso', 'queja', 'denuncia', 'desacuerdo', 'perjuicio', 'daño']
    terminos_positivos = ['excelente', 'gracias', 'mejora', 'acuerdo', 'felicito', 'oportunidad', 'apoyo', 'claro', 'buen']
    
    def calcular_friccion(texto):
        texto = str(texto).lower()
        score_critico = sum([1 for word in terminos_criticos if word in texto])
        score_positivo = sum([1 for word in terminos_positivos if word in texto])
        
        # Balance (-1 a 1)
        if score_critico == 0 and score_positivo == 0:
            return "Neutral / Informativo 🟢"
        elif score_critico > score_positivo:
            if score_critico > 2:
                 return "Indignación Alta 🔴"
            return "Tensión Moderada 🟡"
        else:
             return "Recepción Positiva 🔵"
             
    def calcular_score_numerico(texto):
        texto = str(texto).lower()
        score = 0
        score -= sum([1 for word in terminos_criticos if word in texto])
        score += sum([1 for word in terminos_positivos if word in texto])
        return score

    df_valido['Sentimiento'] = df_valido['Consulta'].apply(calcular_friccion)
    df_valido['Score'] = df_valido['Consulta'].apply(calcular_score_numerico)
    
    return df_valido

df = load_and_analyze_data()

if df is None:
    st.warning("⚠️ No se encontró la Matriz de Resultados. Asegúrate de generar el Excel Final en el Administrador.")
    st.stop()

# --- INTERFAZ GRAFICA ---

total_casos = len(df)
conteo = df['Sentimiento'].value_counts()
criticos = conteo.get("Indignación Alta 🔴", 0)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Comentarios Analizados", total_casos)
with col2:
    st.metric("Nivel Crítico de Fricción", f"{(criticos/total_casos)*100:.1f}%")
with col3:
    st.metric("Tensión General Identificada", conteo.idxmax())

st.divider()

col_map, col_list = st.columns([2, 1])

with col_map:
    st.subheader("Termografía de Sentimiento por Tópico (Clúster)")
    
    # Agrupar por Tema Central y Sentimiento
    df_plot = df.groupby(['Tema Central IA', 'Sentimiento']).size().reset_index(name='Cantidad')
    
    # Paleta custom
    color_discrete_map = {
        "Indignación Alta 🔴": "#d62728",
        "Tensión Moderada 🟡": "#ff7f0e",
        "Neutral / Informativo 🟢": "#2ca02c",
        "Recepción Positiva 🔵": "#1f77b4"
    }
    
    fig = px.bar(df_plot, x="Tema Central IA", y="Cantidad", color="Sentimiento", 
                 title="Distribución del Tono Ciudadano en los Principales Temas Nacionales",
                 color_discrete_map=color_discrete_map,
                 barmode='stack')
                 
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

with col_list:
    st.subheader("Casos de Alta Fricción")
    st.markdown("Muestra filtrada de los textos que requieren atención jurídica y diplomática inmediata.")
    
    alertas = df[df['Sentimiento'] == "Indignación Alta 🔴"]
    if not alertas.empty:
        alertas_top = alertas.sample(min(10, len(alertas)))
        for _, row in alertas_top.iterrows():
            with st.expander(f"Caso en Clúster {row['Cluster TDA (IA)']}"):
                st.write(f"_{str(row['Consulta'])[:200]}..._")
                st.caption(f"Clasificación: **{row['Sentimiento']}**")
    else:
        st.success("No se encontraron casos de indignación alta en esta matriz.")

st.divider()

st.subheader("Buscador Térmico Subterráneo")
st.markdown("Escriba un término (ej. 'costos', 'finca', 'estrato') para ver con qué tono lo está mencionando la gente.")
busqueda = st.text_input("Buscar concepto o palabra:")

if busqueda:
    mask = df['Consulta'].astype(str).str.contains(busqueda, case=False, na=False)
    resultados = df[mask]
    
    if len(resultados) > 0:
        st.write(f"Se encontraron **{len(resultados)}** menciones.")
        
        # Mini pie chart de como reaccionaron a esa palabra
        pie = px.pie(resultados, names='Sentimiento', title=f"Tono emocional sobre: '{busqueda}'", 
                     color='Sentimiento', color_discrete_map=color_discrete_map)
        pie.update_layout(height=300)
        
        col_pie, col_data = st.columns([1, 2])
        with col_pie:
            st.plotly_chart(pie)
        with col_data:
            st.dataframe(resultados[['Consulta', 'Tema Central IA', 'Sentimiento']].head(10), use_container_width=True)
    else:
        st.info("No se halló esa palabra en el léxico nacional.")
