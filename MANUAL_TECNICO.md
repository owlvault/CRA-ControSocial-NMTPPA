# MANUAL TÉCNICO: ARQUITECTURA CORE DEL ECOSISTEMA SABIA

Este manual describe las decisiones de arquitectura de software, stack tecnológico y flujo de datos subyacente para el funcionamiento de SABIA (Sistema de Análisis Basado en Inteligencia Artificial) en la CRA. 

## 1. Stack Tecnológico (Core Libraries)

### Front-End y Orquestación (SABIA UI)
*   **Framework Principal:** `streamlit` (v.1.32+). Streamlit opera como servidor WSGI e interfaz de usuario reactiva bajo un esquema stateful (por pestaña).
*   **Visualización Científica:** `plotly` (express & graph_objects). Seleccionado por su capacidad nativa WebGL, vital para renderizar la constelación 3D de miles de puntos de datos sin congelar el navegador cliente.
*   **Grafos Reticulares:** `networkx` para la física de fuerzas bi-partita (Documentos Reglamentarios vs Clústeres Sociales).

### Back-End y MLOps (NLP Engine)
*   **Red Neuronal (Transformer):** `sentence_transformers`. Modelo empleado: `paraphrase-multilingual-MiniLM-L12-v2`. Seleccionado estadísticamente por ofrecer el mejor equilibrio entre comprensión semántica del idioma español coloquial (Requerido por la participación ciudadana informal) y alta velocidad de inferencia a 384 dimensiones.
*   **Manifold Topológico (TDA):** `umap-learn`. Técnica de reducción dimensional no lineal que preserva distancias estructurales tanto a nivel local (micro-grupos) como global (macro-tendencias). Muy superior a PCA o t-SNE en conservación de estructura comunitaria en lenguaje natural.
*   **Clustering Matemático (Asimétrico):** `hdbscan`. Escogido explícitamente sobre K-Means porque la participación ciudadana no tiene forma circular ni volumen equiparable, y tiene densidades sumamente variadas. Es el **único** modelo que expulsa "Ruido" (`Clúster -1`) permitiendo derivar a los ciudadanos hiper-específicos al Módulo de *Casos Singulares* para trámite legal Uno-a-Uno.
*   **Intersección RAG (Cosine):** `scikit-learn` (`cosine_similarity`). Extraído del pipeline matemático para vectorizar qué extractos del PDF de la base de conocimiento (`PyPDF2` o `pdfplumber` dependencias de abstracción precompiladas) se acercan con mayor intensidad al Clúster.

### Generación "Cero Alucinación" (SABIA LLM)
*   **Interacciones Generativas:** `google.generativeai` (Gemini-1.5-Flash API). Con el hiperparámetro `Temperature=0.0`. Impulsa la capa de Borradores Oficiales y emplea los archivos en `/entrenamiento_de_respuestas/` (Formatos pasados de la CRA) para asimilar o heredar ("Few-Shot") las reglas de formalidad gramatical e institucional, obligándolo, a punta de un prompt asilado, a no salirse de lo extraído por el motor RAG.

---

## 2. Ingesta y Vectorización (Pipeline Python)

El pipeline de recálculo (Activado desde el "Panel de Administración") ejecuta en un subproceso estricto el script `analysis.py`, el cual sigue la siguiente canalización:

1.  **Limpieza Lexical Heurística:** Despierta archivos de Excel que coincidan con `config.json` (`excel_input`). Se aplica una capa Regex (`re.sub`) que demuele dobles espacios, retornos de carro fallidos, y filtra respuestas ridículamente cortas de menos de 10 caracteres (`str.len() > 10`) previniendo puntos ciegos topológicos en la nube 3D.
2.  **Generación Distribuida (Batching Local):** La Red Multilingüe digiere toda la columna saneada usando paralelismo de PyTorch a su mínima expresión en CPU. Devuelve tensores de `[N_Observaciones x 384]`.
3.  **Proyección UMAP (Isometría Coseno):** Configurada con `metric='cosine'` ya que en semántica vectorial, la distancia euclidiana general entre embeddings distorsiona la cercanía conceptual. `n_neighbors` y `min_dist` se ajustaron a 15 y 0.1 como "Baseline", pero en la Interfaz (Módulo Analítica), los científicos de datos gozan de Sliders para recalibrar estas cuerdas dinámicamente frente al magistrado si lo exigen.
4.  **Clasificación Densa HDBSCAN:** Agrupa el colector topológico usando `min_cluster_size=25`. Cifra las sub-poblaciones.
5.  **Intersección Externa RAG y Carga de Output:** Calcula los Cosenos Cruzados contra *chunks* literales procedentes de los Documentos Institucionales (`guia_estrategica_cra.md`) de `Base_de_Conocimiento`, exportando finalmente todo el ciclo matemático al disco `R40 AAPP - RESULTADOS TDA.xlsx`.
