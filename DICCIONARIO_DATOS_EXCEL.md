# GUÍA DE DATOS Y VARIABLES: MATRIZ DE RESULTADOS EXCEL

Esta guía tiene como fin permitirle a cualquier Coordinador, Técnico Regulatorio o Científico de Datos entender en su totalidad qué representa cada nueva característica o variable inyectada a la planilla base nativa (`R40 AAPP - RESULTADOS TDA.xlsx`), tras su procesamiento cruzado por Inteligencia Artificial de la CRA (NLP y Topología TDA).

Las siguientes **9 variables** se anexaron consecutivamente en las columnas finales de su base maestra tras ser procesadas a través del modelo de aprendizaje profundo (`paraphrase-multilingual-MiniLM-L12-v2`).

## 1. Variable Computacional Central (Agrupador)

### Columna: `Cluster TDA (IA)`
*   **Especificaciones Físicas:** Variable Categórica Cuantitativa (Ordinal Discreto Artificial). Sus valores oscilan de `0 a N`, y el único valor restrictivo negativo es `-1`.
*   **Características del Metadato:** Número único calculado por el algoritmo que engloba qué ideas ciudadanas pertenecen al mismo macrotópico ("Galaxia Argumentativa").
*   **Uso Práctico y Significado:** Todos los ciudadanos etiquetados con un mismo número (e.g. `23`) reclaman en esencia matemáticamente el mismo punto clave (Aun si uno escribió "*costos por agua*" y el otro usó "*cobro para sustentar tuberías*"). Este conector agiliza masivamente la tarea, donde al responder técnica y legamente a él, resolviendo todo ese subconjunto.
*   **El Atípico (Ruido `-1`):** Aquellas deudas conceptuales, agradecimientos en blanco, peticiones extrañas, incoherentes o únicas aisladas en la curvatura de observaciones ciudadana serán separadas con un sub-tipo `-1`. Son apartados que no configuran tendencia estadística sustanciable ante el redactor de Marcos Tarifarios.

## 2. Variables Geométricas/Topológicas Adicionales (Graficación Matemática)

Dado el proceso de compresión dimensional `UMAP`, la hoja provee las coordenadas exactas de la red semántica.

### Columnas: `UMAP_2D_X` y `UMAP_2D_Y`
*   **Especificaciones Físicas:** Número en escala Decimal Flotante (+/- Constantes), típicamente entre -20 y 20 de extremo.
*   **Uso Práctico y Significado:** Al subir y conectarse este Excel como fuente de datos final de Microsoft PowerBI, Tableau Server, Qlik Sense (y otras herramientas de Business Intelligence), esta simple dupla es capaz de graficar un Scatterplot (Diagrama Cúbulo) Plano sobre cualquier visualizador. El analista no necesita programar en Python el gráfico espacial de la CRA; basta con graficar `X o Y` para reproducir todos los 1700 comentarios unidos por temáticas idénticamente coloreadas.

### Columnas: `UMAP_3D_X`, `UMAP_3D_Y` y `UMAP_3D_Z`
*   **Especificaciones Físicas:** Eje adicional Decimal Flotante (Longitud, Latitud, Profundidad Semántica).
*   **Uso Práctico y Significado:** Útil si un Científico de Datos o Analista requiere deccionar visualizaciones estéreo-cópicas, realzando o separando ejes (e.g. *Plotly 3D Charts*), validando qué tan densamente abultado es un Clúster que de lejos parece estar fundido con otro tópico ciudadano.

## 3. Variables Narrativas Legales de Inteligencia Artificial (Cruces RAG Extrapolados)

Las observaciones fueron conectadas textualmente hacia un banco cognitivo de 9 Documentos en PDF Base de la CRA (Sustento). El motor genera, escribe e integra directamente 3 resúmenes finales en su Excel para ser consumidos y gestionados vía Pivot/Tablas Dinámicas de Microsoft.

### Columna: `Tema Central IA`
*   **Especificaciones Físicas:** Cadena de Caracteres Corta/Larga (String).
*   **Uso Práctico y Significado:** Título que designa humanamente el número detectado en `Cluster TDA (IA)`. (e.g. En vez de Clúster 5, es "*dudas relativas sobre las exigencias jurídicas o la exclusión del régimen libertad regulada*"). Este extracto fue determinado tras calcular matemáticamente cuál ciudadano es el "punto central exacto" o "Centroide" de la preocupación global, clonando su inquietud cruda para representar a los demás miembros de sus alrededores.

### Columna: `Sustento Normativo RAG`
*   **Especificaciones Físicas:** Cadenas Extensas. Multirreglón/Párrafo.
*   **Uso Práctico y Significado:** Inyecta evidencia jurídica y sustancial cruda del texto pre-existente directamente al Excel. Por clúster, extrae los top 3 cortes literales relevantes de sus `Resoluciones`, `Estudios de Nivel de Servicio` y `Estructuras de Marco` (*y nombra los documentos fuentes exactos que aborda dicha queja comunitaria*). El Redactor Funcional lo utiliza de "Chuleta" para copiar, justificar el preámbulo legal, y no tener que buscar manualmente a ciegas si el Nuevo Marco resuelve o no dicha petición masiva.

### Columna: `Estrategia de Respuesta IA`
*   **Especificaciones Físicas:** Texto Descriptivo/Directivo Corto (String).
*   **Uso Práctico y Significado:** Recomendación algorítmica y paramétrica sumariada para guiar la mano del equipo (Asesor o Director) asignados. Modela el preámbulo para decirle al redactor cómo debería moldear su discurso final de cara al Grupo de Valor o Tipo de Cliente dominante del clúster (EJ: Dirigido a Asociaciones Comunitarias, y respondiendo sobre complejidades medias, fundamentados en zonas rurales). Mantiene al equipo jurídico en sintonía técnica homogénea.
