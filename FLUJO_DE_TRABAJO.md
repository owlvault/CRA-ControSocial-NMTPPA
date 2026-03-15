# FLUJO DE TRABAJO: ANÁLISIS DE MATRIZ DE PARTICIPACIÓN CIUDADANA

## Introducción
El siguiente diagrama detalla cómo los datos de participación ciudadana viajan de forma ininterrumpida desde una hoja de cálculo cruda hasta convertirse en respuestas sólidas justificadas legalmente.

## Fases del Flujo Nominal

**1. Fase Institucional: Recepción y Estructuración Básica**
- La CRA consolida en un documento principal de Excel (`R40 AAPP - FINAL - Marzo 13.xlsx`) las observaciones remitidas por la ciudadanía (correos, actas presenciales).
- Simultáneamente, el área técnica aloja los marcos normativos, borradores de resolución y estudios técnicos de justificación (9 documentos PDF) en la carpeta local denominada `Base de Conocimiento`.

**2. Fase Computacional: Ingesta y Vectorización (NLP)**
- **Limpieza (Scrubbing):** El script extrae únicamente la hoja principal de trabajo (`REG-FOR03`). El texto libre de cada ciudadano es despojado de saltos de línea irregulares y espacios dobles. Se suprimen entradas vacías o cortas (e.g. "ok") por falta de sustancia semántica.
- **Generación de Embeddings:** El modelo transformer proyecta el lenguaje natural de cada observación hacia el espacio matemático denso multidimensional (384 dimensiones). Aquí el motor entiende que palabras como "costo", "tarifa" y "valor a cobrar" están entrelazadas en significado.

**3. Fase TDA (Análisis Topológico y Clustering)**
- El conjunto entero de observaciones (los embeddings) pasan a su análisis posicional.
- UMAP aplasta esas 384 dimensiones a 2 y 3 para volverlas visualizables y calculables.
- **HDBSCAN** interviene rastreando la nube de puntos. Define con precisión dónde un grupo de ideas se hace lo suficientemente denso (un macro-tópico) para constituir un **Clúster**, y marca los comentarios aleatorios que no siguen el hilo narrativo del país con un identificador de `-1` (Ruido).

**4. Fase Estructural: Cruce RAG (Retrieval-Augmented Generation)**
- El centro de gravedad de cada clúster se alinea de regreso contra nuestra biblioteca normada (Base de Conocimiento).
- El motor dispara una analogía del "Coseno": recupera los tres fragmentos específicos de PDF (con documento y número de página) que son constitucional, tarifaria o matemáticamente contiguos al reclamo o sugerencia del grupo ciudadano.

**5. Fase Despliegue: Tableros Específicos y Exportables**
- Se construye de manera unificada el `R40 AAPP - RESULTADOS TDA.xlsx` devolviéndole toda la matemática cruzada a las manos de los analistas que prefieren manejar Excel o BI general.
- Se crean dos Dashboards Analíticos para las gerencias de TI.
- Se nutre el Tablero de **Dashboard de Asignaciones** para que la jerarquía de las regulaciones pase al equipo revisor humano y asigne la observación masiva a su redactor final.
