# MANUAL DE USO OPERATIVO: ARCHIVO EXCEL DE RESULTADOS (R40 AAPP)

Este manual te guiará paso a paso sobre cómo exprimir al máximo el archivo `R40 AAPP - RESULTADOS TDA.xlsx` que arroja el sistema SABIA una vez el motor ha analizado las peticiones ciudadanas. Está diseñado para los equipos Jurídicos, Reguladores, Reguladores de Mercado y Analistas Estadísticos que gestionan, tramitan y envían cartas respuesta.

---

## 🏗️ 1. Anatomía Arquitectónica del Archivo
Cuando abras el Excel generado, notarás que está dividido en dos grandes "zonas" o mundos:

*   👉 **Zona Institucional (Lado Izquierdo):** Todo lo que ves aquí es EXACTAMENTE la sábana matriz original que alguien subió al aplicativo. La máquina no altera ni una coma. Allí encuentras el `Grupo de Valor`, la `ZONA`, la `Consulta` cruda del ciudadano, etc.
*   👉 **Zona Computacional o "SABIA" (Últimas 5 Columnas de la Derecha):** Estas columnas están pintadas o inyectadas por la Inteligencia Artificial. Son tu mejor herramienta de trabajo.

---

## ✨ 2. Conociendo las Nuevas Columnas (Zona SABIA)

¿Para qué sirve cada columna que el sistema agregó mágicamente a la derecha del Excel?

| Columna en Excel | ¿Qué significa en lenguaje sencillo? | ¿Cómo la uso en mi día a día? |
| :--- | :--- | :--- |
| **`Cluster TDA (IA)`** | Es el **NÚMERO de Tema**. El sistema lee miles de filas y agrupa a las personas que preguntan lo mismo bajo un número (Ej. Clúster 1, Clúster 2). | Si a ti te asignan el "Tema Tarifario", simplemente te dicen: "Encárgate de redactar el Clúster 2". Vas al Excel, filtras la columna por el número `2` y listo, tienes todo tu trabajo ahí. |
| **`Tema Central IA`** | Es el título de ese número de arriba. (Ej. *Tarifa, Acueducto, Subsidio*). | Sirve para que, con solo ojear la celda desde arriba para abajo, sepas de qué está hablando la gente sin tener que leer sus párrafos larguísimos. |
| **`Ruido o Aislado`** | Etiqueta de "Casos Raros". | Son ciudadanos con peticiones demasiado extrañas, únicas o muy complejas. El motor no pudo agruparlos con nadie. Tienen la etiqueta `-1` o `True`. **(Estos los deben contestar leyendo la petición uno a uno, ya que suelen ser tutelas o PQRS únicos)**. |
| **`Texto Guía Estratégica RAG`** | Un Resumen Asesor Institucional. La IA lee el Manual de la CRA y te dice cuál debe ser la postura oficial de la Comisión. | Si te quedas en blanco antes de redactar un correo masivo para ese Clúster, lee esta celda. Te dará la perspectiva oficial y el párrafo de introducción. |
| **`Norma / Sustento RAG`** | La ley exacta a citar. | Te da el nombre del Documento Regulador (`.pdf`) y a veces la sección para que la pegues en tu oficio como sustento jurídico irrefutable. |

---

## 👩‍💻 3. Recetas de Trabajo en Excel (Paso a Paso)

A continuación, cómo aprovechar el Excel según tu rol en la Entidad:

### 💼 Receta A: El Redactor de Cartas Respuesta (Abogado / Técnico)
1. Abre tu archivo Excel.
2. Ve al encabezado (Fila 1) y actívale los Filtros (`Datos -> Filtro`).
3. Ve a la penúltima columna: **`Cluster TDA (IA)`**.
4. Desmarca todo y selecciona únicamente el clúster que te ordenó tu coordinador (Ej. `1`).
5. Inmediatamente todo el Excel se encogerá dejando solo a los cientos de ciudadanos que exigen esa respuesta.
6. Copia las cédulas o correos electrónicos (de tu sábana izquierda).
7. Lee la columna de la derecha **`Texto Guía Estratégica RAG`** para saber cómo enfocar la carta. Escribe tu modelo de oficio en Word y envíela masivamente a los correos que aliaste. **¡Acabas de responder 300 peticiones redactando una sola carta!**.

### 🔍 Receta B: El Encargado de Peticiones Singulares y Tutelas
1. Abre tu Excel y asegúrate de tener filtros activos.
2. Ve a la columna **`Ruido o Aislado`**.
3. Selecciona la opción que diga `True` o `-1`.
4. El Excel ocultará los miles de casos masivos y dejará, digamos, las 15 personas únicas que preguntaron cosas exóticas o tutelas puntuales.
5. Deberás leer la columna `Consulta` original de la izquierda para cada uno de estos 15 ciudadanos y contestarles usando el Sistema CISA tradicional, uno por uno.

### 📊 Receta C: Creando un Tablero Estadístico para Presentaciones (Reportes)
1. Abre tu Excel y selecciona absolutamente todas las celdas (Sombra `Ctrl + E`).
2. Ve a `Insertar -> Tabla Dinámica`.
3. Arrastra la columna **`Tema Central IA`** o **`Cluster TDA (IA)`** a la caja que dice **Filas**.
4. Arrastra esa *misma columna* a la caja que dice **Valores** (Asegúrate de que diga *Cuenta de...* y no suma).
5. Arrastra tu columna antigua de **`ZONA`** o **`DEPARTAMENTO`** (La de la izquierda institucional) a la caja de **Columnas**.
6. ¡Listo! Tendrás un cuadro bellísimo que te dice, para el "Tema de Facturación", qué región está protestando más. Insértale un Gráfico Dinámico de Barras ahí mismo y ya tienes la pieza lista para PowerPoint.
