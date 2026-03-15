# MANUAL DE USUARIO: GESTOR DE RESPUESTAS (CRA)

## 1. Introducción al Gestor
El **Gestor de Respuestas** es el primer módulo del "Centro Integrado de Análisis: Control Social NMTPPA". Está diseñado específicamente para Coordinadores (Líderes Técnicos o Jurídicos de la CRA) que tienen la tarea de revisar, analizar y delegar la redacción final de respuestas a los grandes bloques de inquietudes ciudadanas (Clústeres).

Este módulo agiliza el trabajo al entregar las preguntas ciudadanas ya leídas, agrupadas, filtradas y cruzadas algorítmicamente contra la base de datos de PDF institucionales de la CRA.

## 2. Acceso al Módulo
1. Abra su explorador web (Chrome, Edge, Safari, Firefox).
2. Ingrese a la dirección brindada por su equipo técnico (por defecto, si se ejecuta de forma local en su computador: `http://localhost:8503`).
3. En la pantalla de bienvenida (Home), haga clic en la tarjeta **"🏛️ Gestión de Respuestas"** o selecciónela desde la barra lateral de navegación izquierda (`1 Gestión Respuestas`).

## 3. Navegación por la Interfaz

La interfaz está dividida en tres áreas principales de trabajo:

### A. Panel de Selección (Barra Lateral Izquierda)
En este panel usted visualizará las **estadísticas vitales del día** (Cuántos clústeres hay en total y cuántos ha logrado delegar). 
Debajo encontrará una lista desplegable (**"Seleccione un Clúster para revisar:"**). Al abrirla, verá la enumeración de los macrotópicos detectados. Haciendo clic sobre cualquiera, la matriz cambiará todos los textos de la plataforma automáticamente para mostrar el análisis particular de ese grupo social.

### B. Tablero Informativo Central
Una vez seleccionado un Clúster, la pantalla enfocará tres viñetas o "acordeones" expandibles:
*   **📝 Síntesis de la Inquietud Ciudadana:** Un resumen unificado generado a partir de decenas de quejas u observaciones. Representa el "corazón" matemático de la participación social, ideal para entender rápidamente qué reclama este grupo en particular de las 1700 participaciones.
*   **⚖️ Sustento Normativo Identificado (RAG):** El motor buscará e imprimirá párrafos exactos (con número de página y nombre de documento PDF oficial) provenientes de la biblioteca doctrinal (Resoluciones, Estudios de ITBP o Nivel de Servicio). Actúa como un atajo o *"chuleta jurídica"* para argumentar por qué el NMTPPA sí resuelve esta solicitud ciudadana grupal.
*   **🎯 Estrategia Sugerida para el Redactor:** Un lineamiento autogenerado que le recomienda al equipo cómo focalizar la redacción y modular el tono de respuesta dependiendo de si el grupo objetivo dominó en zona rural comunitaria o zona urbana.

### C. Módulo de Asignación y Delegación
En la columna lateral derecha visualizará el panel administrativo ("**👤 Asignación de Tareas**"). Una vez estudiada la información central, el coordinador debe:
1.  **Desplegar "Asignar a:"**: Y seleccionar el departamento responsable que deberá redactar la contestación oficial (e.g. `Jurídica - Regulación`, `Técnico - Economía`, etc).
2.  **Seleccionar Nivel de Prioridad**: Marcar si el impacto al marco tarifario representa una criticidad `Alta 🔴`, `Media 🟡` o `Baja 🟢`.
3.  **Campo de "Instrucciones Específicas"**: Una bitácora en blanco donde usted, como revisor en jefe, digita las instrucciones directas para su abogado/ingeniero a cargo. (Ej: *"Revisar el Art. 40 que cruza la IA y hacer una mesa con Ministerio"*, o *"Acelerar redacción, tema altamente sensible de subsidios"*).
4.  Presionar el botón **`Asignar Clúster 🚀`**. El sistema notificará con un mensaje en verde que se ha guardado en caliente.

## 4. Tabla de Seguimiento y Exportación del Trabajo (Backlog)

Si se desplaza a la zona inferior de la pantalla, encontrará la **"Tabla General de Gestión de Clústeres"**.
*   **¿Qué es?** Un reporte tabular en vivo. Cada vez que usted delega un tema arriba, aquí cambiará automáticamente de estatus `⏳ Pendiente` a `✅ Asignado`, evidenciando el avance del Comité a tiempo real.
*   **Botón `📥 Descargar Reporte de Asignaciones (CSV)`**: Este es el paso final de la jornada. Al finalizar las evaluaciones, haga clic aquí. El sistema descargará un archivo Excel (CSV) a su bandeja de descargas, en el cual compila toda su gestión. Con este archivo, usted podrá enviar masivamente las tareas por correo o integrarlo a un sistema institucional de tickets para que cada área empiece a redactar.
