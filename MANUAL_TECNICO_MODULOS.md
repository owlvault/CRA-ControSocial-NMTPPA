# MANUAL TÉCNICO DE MÓDULOS: ARQUITECTURA DE INTERFACES STREAMLIT

Este documento provee la especificación técnica, lógica de código y dependencias de la capa de presentación (*Frontend*) y gestión de estado de los tres tableros interactivos del **Centro Integrado de Análisis NMTPPA**.

La aplicación está construida sobre una arquitectura **Streamlit Multipage**, sirviendo la página de inicio desde `Home.py` y orquestando el enrutamiento hacia la carpeta estandarizada `/pages/`.

---

## 1. Módulo: Gestor de Respuestas (`1_Gestion_Respuestas.py`)

### Arquitectura Técnica y Lógica Fundamental
*   **Propósito:** Interfaz CRUD (Create, Read, Update, Delete) simplificada para lectura de extracciones NLP y asignación de responsables.
*   **Ingesta de Datos (Parsing):**
    *   No lee directamente de la red neuronal en vivo para optimizar la velocidad (0 ms *load-time*).
    *   Llama y parsea (`@st.cache_data`) el archivo `guia_estrategica_cra.md`, dividiendo el MarkDown con Regex/Splits por encabezados de nivel 3 (`### Clúster X`).
    *   Extrae asincrónicamente los 4 atributos vitales: *Tema, Sustento Normativo (RAG > Markdown Blockquotes), Síntesis y Estrategia recomendada*.
*   **Gestión de Estado y Persistencia:**
    *   Escritura I/O Física. Emplea las rutinas `load_assignments()` y `save_assignment()` para crear o sobrescribir de forma atómica el archivo de control `asignaciones_equipo.json`.
    *   Los formularios (`st.form`) bloquean la mutación asíncrona parcial. Solo al hacer clic en el botón *Submit*, se compila la estructura `{'responsable', 'prioridad', 'notas', 'timestamp'}` y se vuelca al JSON, alimentando directamente la Tabla General en el mismo Request-Response.
*   **Exportación:** Concatena localmente la tabla en memoria usando `pandas` (`df.to_csv()`) inyectándolo en un botón de descarga en binario (`text/csv`).

---

## 2. Módulo: Grafos Topológicos (`2_Grafos_Topologicos.py`)

### Arquitectura Técnica y Lógica Fundamental
*   **Propósito:** Geometría Analítica 2D y Renderización de Grafos No-Dirigidos.
*   **Flujo Topológico (Pipeline):**
    *   Importa la librería matemática matemática `UMAP-Learn`.
    *   Vectoriza al vuelo (`SentenceTransformer` cacheado en VRAM/RAM mediante `@st.cache_resource` para evitar dobles instanciaciones entre páginas).
    *   Condensa los Embeddings de forma determinística (`random_state=42` hiper-parameterizado) para que el gráfico sea reproducible cada vez que el abogado inicie sesión, minimizando el vector hacia coordenadas X, Y mediante métricas de Distancia de Coseno (`metric='cosine'`).
*   **Grafo NetworkX Computacional:**
    *   Construye las triadas *Nodo (Clúster) -> Borde Ponderado -> Nodo (Documento PDF)* a partir del Parseo del archivo `guia_estrategica_cra.md`.
    *   Calcula el Algoritmo de Fuerza Dirigida `spring_layout(G, k=0.8)` de *NetworkX*.
    *   *Plotly Graph Objects (`go.Scatter`)* asume los vértices invisibles en el lienzo WebGL dibujando aristas grises conectaras y superponiendo los Nodos Dinámicos con etiquetas interactivas.

---

## 3. Módulo: Analítica Avanzada (`3_Analitica_Avanzada.py`)

### Arquitectura Técnica y Lógica Fundamental
*   **Propósito:** BI Estadístico y Data-Mining Profundo para analistas. Funciones pesadas renderizadas en el navegador (Plotly).
*   **Vectorización Multidimensional (3D):**
    *   Al igual que el módulo 2, pero inicializa un `reducer_3d` sobre el motor `UMAP` fijando `n_components=3`.
    *   Genera un DataFrame espacial en memoria (`UMAP_3D_X, Y, Z`) y llama a `px.scatter_3d`. A nivel frontend, el framework descarga la responsabilidad a la GPU del navegador del científico renderizando una figura WebCanvas interactiva.
*   **Lógica de Extracción TF-IDF (Term Frequency-Inverse Document Frequency):**
    *   Scikit-Learn (`TfidfVectorizer`). Separa el DataFrame filtrando por Tópicos (ignora `-1`).
    *   Inyecta un diccionario custom (*Stopwords en Español + Jerga CRA*) en memoria.
    *   Tokeniza (`token_pattern=r'(?u)\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b'`) eliminando basuras de menos de 4 caracteres.
    *   Suma la matriz esparsa de SparseArrays para extraer el Top 12 numérico descendente (Aporte ponderado penalizado de cada término por documento) devolviéndolo en una tabla.
*   **Búsqueda Interpolada (Cosine Similarity Search):**
    *   El motor no lee tablas relacionales (SQL). Cuándo el usuario teclea, el campo de input dispara `model.encode([query])`.
    *   Ese puntero flota matemáticamente hacia el espacio de `embeddings` de las 1700 participaciones vectorizadas y extrae en Array NumPy el coseno (`sklearn.metrics.pairwise.cosine_similarity`).
    *   Se retorna un argumento indexado (`argsort()[-15:]`) y un loop trunca el dataframe y exhibe porcentajes formateados al vuelo.
