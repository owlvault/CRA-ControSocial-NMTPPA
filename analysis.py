import os
import re
import pandas as pd
import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
import hdbscan
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO PIPELINE DE ANÁLISIS ===")

# FASE 1: Ingesta y Preprocesamiento
print("FASE 1: Ingesta y Preprocesamiento")
# Cargar Excel
import json
with open('config.json', 'r') as f: config = json.load(f)
excel_path = config['excel_input']
df = pd.read_excel(excel_path, sheet_name='REG-FOR03')

# Limpiar y normalizar 'Consulta'
df['Consulta'] = df['Consulta'].astype(str)
df['Consulta_Clean'] = df['Consulta'].str.strip().str.replace('\n', ' ', regex=False)
df['Consulta_Clean'] = df['Consulta_Clean'].apply(lambda x: re.sub(r'\s+', ' ', x))
# Filtrar nulos o consultas muy cortas
df = df[df['Consulta_Clean'].str.len() > 10].copy()
df.reset_index(drop=True, inplace=True)

print(f"Preguntas cargadas y validadas: {len(df)}")

# Cargar Modelo de Embeddings
print("Cargando modelo SentenceTransformer ('paraphrase-multilingual-MiniLM-L12-v2')...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Extraer y vectorizar PDFs
pdf_folder = 'Base de Conocimiento'
pdf_texts = []
pdf_metadata = []

print("Extrayendo texto de los PDFs de la Base de Conocimiento...")
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        filepath = os.path.join(pdf_folder, filename)
        try:
            with pdfplumber.open(filepath) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        # Dividir en párrafos
                        paragraphs = text.split('\n\n')
                        for p in paragraphs:
                            p_clean = re.sub(r'\s+', ' ', p).strip()
                            if len(p_clean) > 50:
                                pdf_texts.append(p_clean)
                                pdf_metadata.append(f"{filename} - Pag {page_num+1}")
        except Exception as e:
            print(f"Error procesando {filename}: {e}")

print(f"Total de fragmentos normativos extraídos: {len(pdf_texts)}")
print("Vectorizando textos de PDFs...")
pdf_embeddings = model.encode(pdf_texts, show_progress_bar=False)

# FASE 2: Análisis Topológico y Semántico (Clustering)
print("\nFASE 2: Análisis Semántico y Clustering")
preguntas = df['Consulta_Clean'].tolist()
print("Vectorizando consultas ciudadanas...")
preguntas_embeddings = model.encode(preguntas, show_progress_bar=False)

print("Ejecutando clustering HDBSCAN...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=25, metric='euclidean', cluster_selection_method='eom')
df['Cluster'] = clusterer.fit_predict(preguntas_embeddings)

clusters = [c for c in df['Cluster'].unique() if c != -1]
print(f"Se identificaron {len(clusters)} clústeres temáticos (excluyendo ruido/outliers).")

cluster_info = {}
for c in clusters:
    c_df = df[df['Cluster'] == c]
    c_indices = c_df.index
    c_emb = preguntas_embeddings[c_indices]
    
    # Encontrar el centroide y la pregunta más central
    centroid = np.mean(c_emb, axis=0)
    sims = cosine_similarity([centroid], c_emb)[0]
    best_local_idx = np.argmax(sims)
    best_global_idx = c_indices[best_local_idx]
    
    pregunta_central = df.loc[best_global_idx, 'Consulta_Clean']
    
    # Perfilamiento
    comp_mode = c_df['Nivel de compejidad'].mode()
    complejidad_val = comp_mode.values[0] if len(comp_mode) > 0 else "N/A"
    
    zonas = c_df['ZONA'].value_counts().head(3).index.tolist()
    remitentes = c_df['Grupo de Valor'].value_counts().head(2).index.tolist()
    
    cluster_info[c] = {
        'size': len(c_df),
        'pregunta_central': pregunta_central,
        'complejidad': complejidad_val,
        'zonas': ", ".join([str(z) for z in zonas if pd.notna(z)]),
        'remitentes': ", ".join([str(r) for r in remitentes if pd.notna(r)]),
        'centroid': centroid
    }

# FASE 3: Cruce Normativo (RAG)
print("\nFASE 3: Cruce Normativo (RAG)")
for c, info in cluster_info.items():
    centroid_query = info['centroid'].reshape(1, -1)
    sims = cosine_similarity(centroid_query, pdf_embeddings)[0]
    top_indices = sims.argsort()[-3:][::-1]
    
    sustento = []
    for idx in top_indices:
        text_snippet = pdf_texts[idx][:400].replace('\n', ' ')
        sustento.append(f"> **{pdf_metadata[idx]}**: \"{text_snippet}...\"")
    info['sustento_md'] = "\n\n".join(sustento)
    info['doc_ref'] = pdf_metadata[top_indices[0]].split(' - ')[0]

# FASE 4: Generación Markdown
print("\nFASE 4: Generación de Guía Estratégica")
md_lines = [
    "# Guía Estratégica de Respuestas: Nuevo Marco Tarifario CRA (Pequeños Prestadores)",
    "\n## 1. Resumen Topológico de la Participación Ciudadana\n",
    f"Se analizaron un total de **{len(df)} observaciones ciudadanas**. A través de modelos de embeddings del lenguaje y clustering topológico, las inquietudes fueron consolidadas en **{len(cluster_info)} clústeres temáticos clave**. Los comentarios atípicos fueron aislados para concentrar la estrategia normativa en las tendencias de mayor impacto estructural.\n",
    "## 2. Análisis por Clúster Temático\n"
]

sorted_clusters = sorted(cluster_info.items(), key=lambda x: x[1]['size'], reverse=True)

for idx, (c, info) in enumerate(sorted_clusters, start=1):
    tema_central = " ".join(info['pregunta_central'].split()[:10]) + "..."
    md_lines.append(f"### Clúster {idx}: {tema_central}")
    md_lines.append(f"**Relevancia:** {info['size']} preguntas conformaron este clúster.")
    md_lines.append(f"- **Perfil de la Inquietud:** \n  - **Nivel de complejidad promedio:** {info['complejidad']}\n  - **Principales zonas geográficas:** {info['zonas']}\n  - **Tipo de remitentes:** {info['remitentes']}")
    md_lines.append(f"- **Síntesis de las Preguntas:** \n  *{info['pregunta_central']}*")
    md_lines.append(f"- **Sustento Normativo Identificado:**\n\n{info['sustento_md']}\n")
    md_lines.append(f"- **Estrategia de Respuesta Sugerida:** \n  Se debe orientar la respuesta técnica y jurídica enfocándose en las disposiciones del documento `{info['doc_ref']}`. Para el equipo redactor: contextualice la decisión regulatoria justificando la metodología empleada; adecúe el tono para el grupo de valor ({info['remitentes']}), aportando claridad sobre la manera en que el marco tarifario impacta la operación en zonas como {info['zonas']}.\n")
    md_lines.append("---\n")

output_md_path = 'guia_estrategica_cra.md'
with open(output_md_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

print(f"Proceso completado con éxito. Archivo generado: {output_md_path}")
