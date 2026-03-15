# DICCIONARIO DE DATOS Y COLUMNAS: MATRIZ DE RESULTADOS TDA (SABIA)

El motor de SABIA exportará, al finalizar sus ciclos MLOps, un Excel analítico de retorno (usualmente llamado `R40 AAPP - RESULTADOS TDA.xlsx`). Este archivo no corrompe ni reordena la sábana inicial o matriz de la CRA, sino que inyecta en su flanco derecho cinco (5) nuevas columnas de "Meta-Conocimiento" Algorítmico, producto del paso topológico.

## Arquitectura de la Hoja de Cálculo

### 1. Zona Institucional (Columnas Originales Intactas)
A la izquierda, la plataforma preserva sin alterar los datos iniciales para la legitimidad de las cifras orgánicas, por ejemplo:
*   `Consulta`: El texto redactado en crudo por la Veeduría o Ciudadano.
*   `Grupo de Valor`: Categoría Institucional.
*   `DEPARTAMENTO` y `ZONA`.
*   *(Otras referidas en Formato CR)*.

---

### 2. Zona Meta-Algorítmica (Inyectadas por SABIA)
En el margen derecho del archivo exportado aparecerán las variables operadas por Machine Learning de extremo valor para Business Intelligence (BI):

| Columna de Machine Learning | Descripción y Origen Analítico | Utilidad Práctica y Causa Bi-Dimensional (KPI) |
| :--- | :--- | :--- |
| **`Cluster TDA (IA)`** | Identificador Único Númerico asignado por `HDBSCAN` al nodo dimensional. (Ej: `0`, `1`, `2`...). | Determina a qué Macromasa ciudadana estructural pertenece la respectiva pregunta del usuario. |
| **`Tema Central IA`** | Generación Lexical Determinística de los top 5-7 términos (TF-IDF) de ese grupo. Traducción semántica del Clúster TDA (IA). | Permite al Abogado u Operario de Excel entender con solo ojear la celda sobre qué dialogan esas docenas de filas agrupadas. |
| **`Ruido o Aislado`** | Etiqueta Booleana/Texto (`True` / `False` o `Ruido -1`). | Todo campo que resulte `-1` en HDBSCAN. Son casos con densidad nula (Singularidades o Disidencias) y carecen de Tema Central, útiles para desprendimiento y responder de forma Uno-a-Uno (Individual). |

---

### 3. Zona RAG (Sustento Jurídico y Generativo)
Junto a lo anterior, el Servidor en su cruzado espacial ancla las reglas Coseno desde la `"Base de Conocimiento"` (Textos Legales .pdf de resoluciones):

| Columna Documental y Estratégica | Descripción de Impacto Constitucional | Explicación del Motor |
| :--- | :--- | :--- |
| **`Texto Guía Estratégica RAG`** | El motor analítico genera un Resumen Estratégico general o la Estrategia exigida a aplicarse a todos los reclamos agrupados de la Macromasa. | Sirve como Norte Directivo para el Redactor. Ayuda al callist / escritor humano de la Comisión a no obviar lo que el algoritmo determinó como lo fundamental. (Requerida también en el LLM Generativo de Borradores). |
| **`Norma / Sustento RAG`** | Arrojan listados con "Bulletpoints" o viñetas indexando qué Leyes Nacionales, Resoluciones CRA históricas o fragmentos extraídos atacan o dan marco vinculante a la observación leída en la celda. | Le concede al analista del Excel saber qué documento y reglamentos debe adjuntar a la carta formal. |
