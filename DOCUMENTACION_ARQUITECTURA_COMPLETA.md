# ECOSISTEMA INTEGRADO MLOps: CENTRO DE ANÁLISIS CRA - NMTPPA

Este documento sirve como hoja de ruta técnica y arquitectónica para comprender el ecosistema final de la plataforma, la cual consta de **9 módulos de Inteligencia Artificial interconectados** diseñados para gobernar el ciclo completo de participación ciudadana regulatorio.

---

## 🏗 Arquitectura de Alto Nivel
El sistema opera bajo un pipeline lineal paramétrico. Las entradas asíncronas iniciales (`.xlsx` original y `PDFs` de Resoluciones) desencadenan un clúster de Inteligencia Artificial basado en HuggingFace que destila conocimiento geométrico. Este conocimiento topológico luego se ramifica hacia herramientas de consumo directo por parte de los 3 Perfiles Clave de la Institución: 
1. **Coordinadores Jurídicos/Técnicos**.
2. **Científicos de Datos y Estadísticos**.
3. **Redactores Finales**.

---

## 🚀 Desglose de los 9 Módulos del Ecosistema

### 1. 🏛️ Gestión de Respuestas (`1_Gestion_Respuestas.py`)
*   **Usuarios:** Coordinadores de Dependencias.
*   **Función:** Interfaz CRUD central. Lee la destilación RAG proveniente del motor primario y muestra un resumen ejecutivo de cada Clúster Ciudadano (Tema Central + Artículos Cruzados + Estrategia Sugerida).
*   **Valor MLOps:** Permite a los directivos asignar dinámicamente un responsable institucional (Jurídico, Técnico) a cada macromasa (Clúster) y priorizar la gravedad de las respuestas.

### 2. 🕸️ Grafos Topológicos (`2_Grafos_Topologicos.py`)
*   **Usuarios:** Analistas y Directivos.
*   **Función:** Transforma la sábana de texto de 1,701 filas en una cartografía viva dimensional (UMAP 2D). Dibuja un Diagrama de Red Bi-partito (NetworkX) conectando nodos de Clústeres contra los Nodos Documentales (PDFs de la CRA) que los sustentan en la nube geométrica.
*   **Valor MLOps:** Cartografía visual de relaciones complejas.

### 3. 🔬 Analítica Avanzada (`3_Analitica_Avanzada.py`)
*   **Usuarios:** Científico de Datos (Data Scientist).
*   **Función:** Controles puros sobre el modelo. Renderizado interactivo WebGL en 3D del Universo de embeddings. Generador Termodinámico TF-IDF para extraer el vocabulario puro de la participación colombiana filtrando el ruido burocrático, además de cruzar heatmaps con variables sociodemográficas.

### 4. ⚙️ Panel Admin (`4_Administracion.py`)
*   **Usuarios:** Ingenieros / Data.
*   **Función:** Tablero de Control y Mantenimiento de la App.
*   **Valor MLOps:** Descentraliza el código crudo. Permite subir `Arrastrando con el Ratón` nuevos Excels `.xlsx` futuros de las R40 y múltiples nuevos PDF. Incluye el Botón Maestro para accionar la red neuronal subyacente (`analysis.py`) y dictaminar cuándo se exportará de regreso la sábana final Excel de Resultados.

### 5. 🩺 Monitor de Calidad (`5_Monitor_Calidad.py`)
*   **Usuarios:** Auditor / Administrador MLOps.
*   **Función:** Observabilidad ("Observability").
*   **Valor MLOps:** Sistema automatizado de semáforos temporales. Audita si los *Timestamps* de los PDFs añadidos o del Excel original se desfasaron contra el Caché en memoria de la Topología y del RAG. Previene que el equipo jurídico despache respuestas que estén usando regulaciones viejas de memoria.

### 6. 🤖 Generador de Borradores (`6_Generador_Borradores.py`)
*   **Usuarios:** Abogados / Redactores.
*   **Función:** Conexión estricta a Google Gemini LLM API con `Temperature=0.0`.
*   **Valor MLOps:** Asimilación "Few-Shot Learning". Permite subir PDFs humanos históricos a una carpeta de entrenamiento para mimetizar el tono institucional de la entidad. Usando el contexto RAG + Estrategia, dicta una carta en milisegundos sin inventar artículos falsos (Restricción Anti-Alucinación).

### 7. 😡 Analizador Térmico de Sentimiento (`7_Analisis_Sentimiento.py`)
*   **Usuarios:** Asesores Conceptuales / Comunicaciones.
*   **Función:** Barrido Lexicográfico por Tópico.
*   **Valor MLOps:** Mide la fricción (Indignación, Neutralidad, Apoyo) segmentándola por regiones o por macro-temas. Permite encontrar a 1 clic los comentarios hirvientes y ubica visualmente si ciertos artículos están generando mayor explosión emocional ciudadana.

### 8. 🔬 Explorador de Micro-Clústeres (`8_Explorador_Microclusters.py`)
*   **Usuarios:** Científico de Datos / Analista Predictivo.
*   **Función:** Deep Dive K-Means recursivo.
*   **Valor MLOps:** Una lupa matemática. Aisla 1 solo Clúster Nacional, borra al resto del país, re-procesa a 384 dimensiones solo a esos usuarios con Distancia de Coseno, y los hiper-fractura dictaminando los matices subterráneos de un dolor en común.

### 9. 👤 Consultas Individuales (`9_Consultas_Individuales.py`)
*   **Usuarios:** Equipo de Apoyo Jurídico / Coordinadores.
*   **Función:** Gestión del descarte topológico (`Clúster -1`).
*   **Valor MLOps:** En los sistemas analíticos ciudadanos, no todo encaja en consensos masivos ("Clústeres"). Esta interfaz rescata las "Anomalías Aisladas" —participaciones con peticiones hiper-específicas o únicas que el algoritmo descartó de la masa grupal. El módulo tabula estos casos, grafica su origen y permite exportarlos para que el Jurídico proceda con respuestas "Uno a Uno", cumpliendo con el derecho de petición individual protegido por ley.

---
**Estatus:** El Sistema se encuentra completamente documentado, consolidado (Git versionado) y funcional para un Despliegue en Producción Institucional a partir de Marzo de 2026.
