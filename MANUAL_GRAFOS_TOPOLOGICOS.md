# MANUAL DE USUARIO: GRAFOS TOPOLÓGICOS (CRA)

## 1. Introducción al Módulo
El módulo de **Grafos Topológicos** es una herramienta visual e interactiva pensada para entender, desde una perspectiva "aérea" o satelital, cómo se comportó la participación ciudadana y de qué forma esos reclamos y sugerencias impactan los documentos normativos de la CRA. 

En lugar de leer 1700 filas en Excel, este sistema proyecta geométricamente las ideas, convirtiéndolas en constelaciones (Mapas UMAP) y redes conceptuales (Grafo NetworkX), permitiéndote detectar patrones ocultos de inmediato.

## 2. Acceso al Módulo
1. Abra su explorador web preferido.
2. Ingrese a la dirección brindada por su equipo técnico (por defecto: `http://localhost:8503`).
3. Puede acceder mediante dos vías:
   - Haciendo clic en la tarjeta central de la pantalla principal que dice **"🕸️ Grafos Topológicos"**.
   - O usando en cualquier momento el menú gris de la izquierda (*Sidebar*) y seleccionando `2 Grafos Topologicos`.

## 3. Guía de Uso por Pestaña (Tabs)

El módulo alberga tres subdivisiones o pestañas en la parte superior. Haga clic en ellas para alternar entre diferentes lentes analíticos:

### Pestaña 1: 🗺️ Mapa Semántico UMAP
Este tablero dibuja un diagrama esparcido (Scatterplot) de cientos de pequeños puntos.
*   **¿Qué es cada punto?** Cada punto que usted ve flotando representa **exactamente una (1) pregunta** u observación que un ciudadano de Colombia redactó a la CRA.
*   **¿Por qué están agrupados?** La Inteligencia Artificial leyes los textos e infirió su "*Similitud Semántica*". Si dos puntos están muy pegados el uno al otro, significa que ambos ciudadanos están opinando sobre el mismo dolor o felicitación (Sin importar que hayan escrito palabras distintas). A estos continentes o nubes densas de puntos del mismo color se les llama "Clúster".
*   **Interacción (Tooltip):** Mueva el cursor (ratón) libremente por encima del mar de puntos. Al detenerse sobre cualquier punto individual, una pequeña caja negra negra se abrirá indicándole qué escribió exactamente esa persona y a qué Clúster pertenece.
*   **Filtro:** A la derecha tiene la "Leyenda" de clústeres. El color gris denota el `-1 (Ruido)`, que son comentarios inclasificables o inválidos por irrelevantes. Haga doble clic en los colores de la derecha de la leyenda para ocultar tópicos o aislar y ver exclusivamente la nube que le interesa.

### Pestaña 2: 🕸️ Grafo de Relaciones Normativas
Aquí la plataforma cambia de un mapa estelar a un "Mapa Conceptual o de Araña" (*NetworkX*).
*   **¿Para qué sirve?** El grafo responde a la pregunta vital: *"De todas los clústeres ciudadanos que recibimos... ¿Qué documento oficial del marco regulatorio se ve más interpelado?"*
*   **Nodos Azules (Tópicos):** Representan a la ciudadanía categorizada (Ej: Clúster 1, Clúster 5).
*   **Nodos Naranjas (Documentos Normativos):** Representan el PDF raíz de la política de la CRA (Ej: `Documento Estudio ITBP`, `Bases NMT`, `Resolución Final`).
*   **Líneas Conectoras:** Las líneas ilustran qué documento de la CRA provee la "respuesta jurídica" o la "explicación" a los dolores de cada Clúster. 
*   **Análisis Visual:** Si usted nota que un Nodo Naranja de un Documento (e.g. `Documento Técnico_NMTAAPP_20112025.pdf`) está en el centro rodeado masivamente por muchas líneas y nodos azules (Clústeres), significa que dicho documento es el **epicentro regulatorio del debate** y sobre el cual recaerá la mayor carga argumentativa durante las sesiones de respuesta a la comunidad. Puede hacer clic, acercar/alejar la red (Scroll), e inspeccionar las intersecciones.

### Pestaña 3: 📊 Métricas y Filtros
Esta última pestaña es el resumen duro de los datos consolidados que sirvió de cimiento para los dibujos espaciales.
*   **Indicadores Clave:** En grandes recuadros verá a simple vista la magnitud de la limpieza: Total de ciudadanos procesados limpios, la cantitad finita de tópicos matemáticos estructurados y qué porcentaje exacto de las preguntas resultaron en ruido/anomalías.
*   **Radiografías de Ocurrencia (Gráficos):** Descendiendo, dispondrá de una gráfica en torta (Pie Chart) y un gráfico de barras (Bar Chart) donde podrá dimensionar rápidamente, para todo este estudio regulatorio, de dónde provienen geográficamente los reclamos dominantes (`Distribución por Zona`) y bajo qué rótulo de exigencia jurídica clasificaron (`Nivel de Complejidad`). Igual que todo gráfico en este sistema, al dejar encima el cursor se revela la cantidad bruta detrás del fenómeno visual (ej. *120 comentarios de la Zona Caribe*).
