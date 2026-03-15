# ECOSISTEMA INTEGRADO MLOps: PLATAFORMA SABIA (CRA - NMTPPA)

Este documento sirve como hoja de ruta técnica y arquitectónica para comprender el ecosistema final de la Plataforma SABIA (Sistema de Análisis Basado en Inteligencia Artificial), la cual consta de **9 módulos de Inteligencia Artificial interconectados** diseñados para gobernar el ciclo completo de participación ciudadana y análisis normativo.

---

## 🏗 Arquitectura de Alto Nivel "Divulgación Progresiva"
El sistema opera bajo un pipeline parametrizado (MLOps) y una interfaz fluida impulsada por Streamlit. Las entradas asíncronas iniciales (Matriz de Participación `.xlsx` y `PDFs` Regulares) desencadenan un cluster de modelos de ML local. 
La interfaz incluye un **Enrutador Lateral Customizado** que estructura el trabajo en tres grandes familias funcionales (1. Topología, 2. Acción Institucional, y 3. Mantenimiento). Para proteger a perfiles gerenciales y abogados de la saturación visual, el software incorpora *switches* o palancas de "Modo Ingeniero", escondiendo los tensores o hiper-parámetros por defecto detrás de diseños sumamente limpios (Cero-Ruido, alta relación `Data-to-Ink`), colores y tipologías corporativas (Azul y Tabular).

---

## 🚀 Desglose de los 9 Módulos del Ecosistema SABIA

### 1. ⚖️ Gestión de Acuerdos (`1_Gestion_Respuestas.py`)
*   **Segmento:** Flujo de Acción Institucional.
*   **Función:** Interfaz CRUD de Asignaciones. Lee la destilación proveniente de la base y muestra las síntesis, requerimientos estratégicos de respuesta y la delegación de responsabilidades de las Dependencias de la entidad a cada Macromasa Ciudadana.

### 2. 🕸️ Cartografía Relacional (`2_Grafos_Topologicos.py`)
*   **Segmento:** Topología y Exploración.
*   **Función:** Dibuja bi-grafos en 2D UMAP del espacio topológico. Renderiza la conexión de fuerzas de los Clusters Ciudadanos atados interactuando con los Documentos Legales de Consulta que el equipo incrustó. Almacena en memoria Resortes y repulsiones `NetworkX`.

### 3. 🔬 Analítica Avanzada (`3_Analitica_Avanzada.py`)
*   **Segmento:** Topología y Exploración.
*   **Función:** Entorno profundo en 3 Dimensiones que dibuja la totalidad del Universo Geométrico (1,701 ciudadanías). Incorpora el Motor TF-IDF Categórico, los heatmaps analíticos sociodemográficos (Zonas, Complejidad) y el buscador Vectorial Coseno profundo (Similaridad).

### 4. 💾 Consola Admin MLOps (`4_Administracion.py`)
*   **Segmento:** Gestión Administrativa.
*   **Función:** Interfaz Master. Permite arrastrar el "Data Lake" primario, inyectar docenas de textos legales en PDFs (Base Documental) y desencadenar a voluntad los scripts en Python de *Machine Learning* Pesado que vuelven a iterar a 384 dimensiones toda la plataforma.

### 5. 🩺 Salud del Orquestador (`5_Monitor_Calidad.py`)
*   **Segmento:** Gestión Administrativa.
*   **Función:** Verificador de Estados o Semáforo Forense. Calcula que los timestaps de Excel entrante, Scripts de salida (TDA.xlsx) y la Base RAG de entrenamiento coincidan. De lo contrario, impide el flujo lanzando Alertas (Rojas/Amarillas) de Desfase o "Alucinación de Memoria".

### 6. 🤖 LLM Cero-Alucinación (`6_Generador_Borradores.py`)
*   **Segmento:** Flujo de Acción Institucional.
*   **Función:** Sala redactora automática. El Agente Gemini API usa la estrategia previamente curada, restringe creativamente al robot para evitar inventos (Temperature=0.0) y aplica un clonado ("Few-Shot Learning") del tono de escritura a partir de las viejas respuestas oficiales humanas incrustadas (`entrenamiento_de_respuestas/`).

### 7. 🌡️ Auditoría Térmica (`7_Analisis_Sentimiento.py`)
*   **Segmento:** Topología y Exploración.
*   **Función:** Lexical de fricción estática o LLM. Calcula qué poblaciones o zonas nacionales portan mayor carga térmica negativa o "Indignación" y neutralidad, previniendo al comunicador que su misiva va con un nivel emocional alto.

### 8. 🔍 Lente Micro-Clústeres (`8_Explorador_Microclusters.py`)
*   **Segmento:** Topología y Exploración.
*   **Función:** Descompone fracturadamente a los macro-tópicos y recarga K-Means. Útil para desmembrar si dos grupos poblacionales discuten el mismo tema legal internamente pero con posturas absolutamente diferentes o distantes.

### 9. 👤 Casos Singulares - Ruido (`9_Consultas_Individuales.py`)
*   **Segmento:** Flujo de Acción Institucional.
*   **Función:** Bandeja de "Anomalías No Asociadas" (-1 HDBSCAN). Todo ciudadano cuyos datos no logren densificarse junto a otro grupo pero el sistema exija legalmente dar un dictamen final (Una tutela, reclamo propio) aterriza aquí para que el perito no deje observaciones de "Ruido Matemático" convertidas en Silencio Administrativo.

---
**Estatus Actual:** Plataforma de producción validada, rediseñada y robustamente documentada a Marzo de 2026. Operable.
