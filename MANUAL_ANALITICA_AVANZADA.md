# MANUAL DE USUARIO: ANALÍTICA AVANZADA (CRA)

## 1. Introducción al Módulo
El módulo de **Analítica Avanzada** fue concebido y parametrizado para Científicos de Datos, Ingenieros o Analistas Estadísticos del equipo de la CRA. 

Este espacio permite manipular e interrogar directamente la topología del Nuevo Marco Tarifario de Pequeños Prestadores de Acueducto. Otorga al usuario control directo sobre el espacio tridimensional y facilita herramientas de cruzamiento en matrices complejas (Heatmaps), y búsquedas en bases de lenguaje natural.

## 2. Acceso al Módulo
1. Abra el navegador y entre al portal integrado de Inteligencia Artificial (por defecto: `http://localhost:8503`).
2. Haga clic en la tarjeta **"🔬 Analítica Avanzada"** o navegue hasta la opción número `3` en la barra lateral (*Sidebar*).

## 3. Navegación por la Interfaz de Explotación de Datos

El sistema contiene 4 pestañas interactivas diseñadas de forma modular.

### Pestaña 1: 🌌 Espacio Topológico 3D
La red semántica de los comentarios se condensa y "flota" matemáticamente en un eje de 3 coordenadas.
*   **¿Para qué sirve?** El analista puede verificar visualmente la homogeneidad, pureza y segmentación esférica de cada macrotópico ciudadano (Clúster) desde un lente tridimensional. Los puntos lejanos al grupo representan quejas con matices distintivos.
*   **Controles:**
    *   **Click + Arrastrar:** Para rotar libremente el globo y encontrar huecos lógicos u observar aglomeraciones desde atrás.
    *   **Rueda del Ratón (Scroll):** Para aplicar zoom (+ y -), sumergiéndose o saliendo de una nube.
    *   **Puntero/Hover:** Al pasar el ratón se despliega la queja escrita, en conjunto con su *Complejidad*, *Grupo de Valor* (Ej: Juntas de Acción o Veedurías) y la *Zona* (Urbana/Rural/Caribe). A diferencia del módulo de Grafos Básicos, este modelo cruza dichas metas variables en vivo.

### Pestaña 2: 🔤 Modelado de Tópicos (TF-IDF)
Esta pestaña responde a: *"¿De qué habla exactamente en esencia este clúster?"*
*   El área técnica puede encontrar en esta tabla el **Lexicón Exclusivo** o la lista de las 12 palabras más dominantes, singulares y frecuentes de un mismo tópico (Ejemplo: *"subsidio, costo, rural, mantenimiento, sobretasa"*).
*   **Dato Clave:** El algoritmo (Term Frequency-Inverse Document Frequency) descartará las palabras ultra-institucionales obvias (ej. "CRA", "Acueducto", "Resolución", "para", "de"), con tal de focalizarse y extraer puros verbos y sustantivos medulares que definen el dolor social que relatan las bases del NMTPPA.

### Pestaña 3: 📈 Variables Cruzadas
Aquí convergen las bases de datos transaccionales con el análisis NLP de Machine Learning.
*   **Panel Cuantitativo Superior (Barras):** Dispone de dos *Dropdowns* o Menús Desplegables. Puede elegir en tiempo real situar el *Eje X* en una característica (Ej: Zona), y colorear o estratificar las subdivisiones con una segunda categoría transversal (Ej: Nivel de Complejidad). Las barras se apilarán y el analista podrá ver gráficamente, por ejemplo, que los casos "Complejos" dominan el "Valle del Cauca".
*   **Matriz Térmica (Heatmap Inferior):** Al escoger una Variable Termal (Ej: Grupo de origen ciudadano u oficios o Zonas), se iluminará un mapa cruzando los 25 Tópicos Identificados de IA contra tu variable. **Casillas amarillas y brillantes** te avisarán visualmente en qué esquina del rectángulo hay una densa cantidad concentrada (Ej: Si la casilla *Clúster 12* cruza *Región Andina* con amarillo incandescente indicando "60 Casos", usted debe priorizar y afilar especialmente el argumento oficial frente a los delegados de esa zona).

### Pestaña 4: 🔍 Motor de Interrogación Vectorial
Este módulo actúa como una enciclopedia interactiva en lenguaje natural ("Google Semántico Propio de la CRA").
*   **¿Qué hace?** En lugar de intentar hallar ciudadanos filtrando rudimentalmente por Clúster o leyendo por encima las filas del Excel, el analista puede teclear conceptos directos suyos en la barra (*e.g., "¿Qué dudas tiene la gente sobre micromedición con esta tarifa?"*).
*   **Algoritmo de Distancia:** Al presionar "Buscar Similitudes", el Transformer convierte su frase a 384 dimensiones, extrae la geometría y persigue en la oscuridad las 15 filas ciudadanas que sean matemáticamente más análogas o compatibles con lo que acaba de escribir.  Indepedientemente si usaron otros sinónimos.
*   **Salida:** Un **Ranking Estadístico en % Relativo**, con el Top 15 de los ciudadanos junto a qué Tópico original pertenecían. Útil para que los Abogados armen jurisprudencia de un reclamo aislado, encontrando testimonios precisos de inmediato.
