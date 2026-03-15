import pandas as pd
import numpy as np
import re
import os
import umap
import hdbscan
from sentence_transformers import SentenceTransformer

# Archivos de Entrada y Salida
excel_in = 'R40 AAPP - FINAL - Marzo 13.xlsx'
excel_out = 'R40 AAPP - RESULTADOS TDA.xlsx'

print("1. Cargando datos del Excel Original...")
xls = pd.ExcelFile(excel_in)
sheets = {sheet: pd.read_excel(excel_in, sheet_name=sheet) for sheet in xls.sheet_names}
df_main = sheets['REG-FOR03'].copy()

print(f"2. Procesando la hoja principal (REG-FOR03) con {len(df_main)} registros...")
# Normalizar texto para la IA pero preservar el df original
df_main['Consulta_Clean'] = df_main['Consulta'].astype(str).str.strip().str.replace('\n', ' ')
df_main['Consulta_Clean'] = df_main['Consulta_Clean'].apply(lambda x: re.sub(r'\s+', ' ', x))

# Para no perder el orden NI el tamaño del excel, procesamos solo filas con texto válido
mask_valid = df_main['Consulta_Clean'].str.len() > 10
preguntas = df_main.loc[mask_valid, 'Consulta_Clean'].tolist()

print("3. Generando Embeddings Sensibles al Contexto...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(preguntas, show_progress_bar=False)

print("4. Ejecutando Análisis Topológico (UMAP + HDBSCAN)...")
# Reducciones dimensionales de TDA
reducer_2d = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine', random_state=42)
umap_2d = reducer_2d.fit_transform(embeddings)

reducer_3d = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=3, metric='cosine', random_state=42)
umap_3d = reducer_3d.fit_transform(embeddings)

# Agrupamiento
clusterer = hdbscan.HDBSCAN(min_cluster_size=25, metric='euclidean', cluster_selection_method='eom')
clusters = clusterer.fit_predict(embeddings)

print("5. Ensamblando Columnas Vectoriales...")
df_main['Cluster TDA (IA)'] = -1
df_main['UMAP_2D_X'] = np.nan
df_main['UMAP_2D_Y'] = np.nan
df_main['UMAP_3D_X'] = np.nan
df_main['UMAP_3D_Y'] = np.nan
df_main['UMAP_3D_Z'] = np.nan

df_main.loc[mask_valid, 'Cluster TDA (IA)'] = clusters
df_main.loc[mask_valid, 'UMAP_2D_X'] = umap_2d[:, 0]
df_main.loc[mask_valid, 'UMAP_2D_Y'] = umap_2d[:, 1]
df_main.loc[mask_valid, 'UMAP_3D_X'] = umap_3d[:, 0]
df_main.loc[mask_valid, 'UMAP_3D_Y'] = umap_3d[:, 1]
df_main.loc[mask_valid, 'UMAP_3D_Z'] = umap_3d[:, 2]

print("6. Cruzando Identificadores con la Base Normativa (RAG)...")
file_path = 'guia_estrategica_cra.md'
cluster_info = {}
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    raw_clusters = content.split('### Clúster ')[1:]
    
    for raw in raw_clusters:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if not lines: continue
        id_split = lines[0].split(':', 1)
        cluster_id = int(id_split[0].strip())
        tema = id_split[1].strip() if len(id_split) > 1 else ""
        
        sustento = []
        estrategia = ""
        capturing_estrategia = False
        
        for line in lines[1:]:
            if line.startswith('- **Estrategia de Respuesta Sugerida:**'):
                capturing_estrategia = True
                estrategia += line.replace('- **Estrategia de Respuesta Sugerida:**', '').strip() + " "
                continue
            elif line.startswith('> **'):
                capturing_estrategia = False
                sustento.append(line.replace('>', '').strip())
                continue
            elif line.startswith('- **') or line.startswith('---'):
                capturing_estrategia = False
                
            if capturing_estrategia:
                estrategia += line + " "

        cluster_info[cluster_id] = {
            'Tema Central': tema,
            'Sustento Normativo': "\n".join(sustento),
            'Estrategia RAG': estrategia.strip()
        }

# Expandir Resultados Normativos
df_main['Tema Central IA'] = "No Asignado (Ruido Topológico / Texto Inválido)"
df_main['Sustento Normativo RAG'] = ""
df_main['Estrategia de Respuesta IA'] = ""

for c_id, info in cluster_info.items():
    mask = df_main['Cluster TDA (IA)'] == c_id
    df_main.loc[mask, 'Tema Central IA'] = info['Tema Central']
    df_main.loc[mask, 'Sustento Normativo RAG'] = info['Sustento Normativo']
    df_main.loc[mask, 'Estrategia de Respuesta IA'] = info['Estrategia RAG']

# Limpieza transitoria
df_main.drop(columns=['Consulta_Clean'], inplace=True)
sheets['REG-FOR03'] = df_main

print("7. Generando libro de salida de Excel (Output Final)...")
with pd.ExcelWriter(excel_out, engine='openpyxl') as writer:
    for sheet_name, df_sheet in sheets.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"=== PROCESO COMPLETADO EXitosamente ===")
print(f"Archivo generado: {excel_out}")
