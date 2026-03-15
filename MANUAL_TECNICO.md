# MANUAL TÉCNICO: PROCESAMIENTO ANALÍTICO, NLP Y TDA

## 1. Arquitectura Científica General
La base analítica del Proyecto `CRA-ControlSocial-NMTPPA` se fundamenta en un flujo ininterrumpido que va de la Extracción Óptica (Pdf-parsing) y lectura tubular, hacia la Vectorización Profunda y una reducción multi-etapas de densidad poblacional (TDA).

## 2. Modelos Lingüísticos y Procesadores NLP

**Extracción del Dominio Legal (PDF Parser):**
*   Librería: `pdfplumber` (Basada en PyMuPDF/PDFMiner estructurado).
*   Especificación de Parseado: Transcribe renglones preservando los saltos ortográficos duros (`\n\n`) para seccionar estructuralmente el "párrafo". A diferencia de otros scrapers que parten a medias las sentencias, esta librería retiene la intención del argumento normativo de las resoluciones o decretos importados.

**Transformer Vectorial Empatico del Contexto (Sentence-Transformers):**
*   Modelo Específico: `paraphrase-multilingual-MiniLM-L12-v2`.
*   Propiedades: Arquitectura de *Knowledge Distillation* (Destilación de Conocimiento) sobre un modelo multilingüe enorme acortado a sus 12 capas neuronales fundamentales. Este algoritmo fue entrenado bajo pares de parafraseos (sabe que decir "agua gratis" es muy similar semánticamente a "no cobrar por servicio hídrico"), siendo radicalmente superior a técnicas crudas donde coinciden palabras. Genera de cada consulta bruta un Embedding de 384 dimensiones flotantes de alta densidad matemática. Ideal para el Español legislativo.

## 3. Topología Predictiva y Agrupación Analítica (TDA)

**Reducción de Dimensionalidad Continua: UMAP:**
*   Acrónimo Técnico: *Uniform Manifold Approximation and Projection*.
*   Configuración: `n_components=2` y `3`, `n_neighbors=15`, y un `min_dist=0.1`.
*   Operación Numérica: Asume matemáticamente que los 1700 casos flotan en una curvatura "Uniforme de Riemann". Genera aproximaciones locales y las obliga a co-existir juntas con baja pérdida de información hacia un plano 2D (Dashboard visual) y 3D (Escatterplot Topológico) donde la semántica ciudadana colindante se vuelve una vecindad espacial.

**Detección de Sub-Espacios de Densidad: HDBSCAN:**
*   Acrónimo Técnico: *Hierarchical Density-Based Spatial Clustering of Applications with Noise*.
*   Propósito Físico y Razón de Ser: La participación pública no está dividida en círculos limpios ($k$) como demanda un *K-Means*. Está trazada como manchas orgánicas variables que incluyen preguntas misceláneas inservibles. `HDBSCAN` ignora la suposición de formas hiper-esféricas (Euclideana) y en su lugar detecta montañas estables de "densidad local" de comentarios, marcando todo aquello debajo del umbral como ruido o `-1`.
*   Configuración: `min_cluster_size=25` (Filtra todas las quejas o comentarios minoritarios/aislados y se centra en verdaderas políticas repetitivas de masas), método de selección óptimo: `eom` (Extracción de las ramas primarias más densas del Dendrograma generado).

## 4. Técnica NLP Adicional: Frecuencia de Tópicos TF-IDF
En el Módulo Análisis (Tablero 8505), para la humanización y nombramiento del agrupamiento topológico, se calcula:
- *Term Frequency - Inverse Document Frequency (TF-IDF)*.
- Procesa el Clúster detectado calculando de 0 a 1 la palabra que repiten obsesivamente sus integrantes contra todas las 1600 observaciones del exterior, filtrando un lexicón depurado (e.g. `la, de, acueducto, cra, comunitario`) para arrojar Top Terms distintivos del fenómeno social al analista.
