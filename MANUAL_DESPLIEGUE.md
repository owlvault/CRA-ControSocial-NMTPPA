# MANUAL DE DESPLIEGUE TÉCNICO: ENTORNO DAta SCIENCE

## Prerrequisitos del Analista

Todo miembro del departamento de Inteligencia de Datos o Analítica que desee auditar o explotar este ecosistema de control social CRA requerirá un OS con **Python 3.8 o superior**.
Es indispensable disponer de su entorno virtualizado preparado o Git Bash habilitado (Anaconda u OS X Nativo es válido).

## Proceso de Instalación

**Paso 1: Clonar el Repositorio Maestro en el Terminal OS**
```bash
git clone https://github.com/owlvault/CRA-ControSocial-NMTPPA.git
cd CRA-ControSocial-NMTPPA
```

**Paso 2: Instalación de Dependencias e IA Pre-entrenada**
- Recomendación: Operar bajo Entorno Virtual local (`python -m venv venv` // luego invocar `.venv/Scripts/activate` o  `source venv/bin/activate`).
- Seguidamente, cargar requerimientos vectoriales listados.
```bash
pip install -r requirements.txt
```
> *(Nota Científica: La librería `sentence-transformers` se descargará por primera vez a este OS una fracción pesada (2-3Gb) de redes neuronales HuggingFace, pero el sistema quedará cacheado off-line indefinidamente).*

## Mantenimiento Predictivo: Generar Exportable o Actualizar Matriz Excel Crudo

Si la entidad reguladora emite un anexo, el archivo nativo (`R40 AAPP - FINAL - Marzo 13.xlsx`) deberá ser reemplazado o sumado a las filas en su pestaña original (`REG-FOR03`).

```bash
# Script de Procesamiento IA, RAG y MarkDown (Ineludible como primer paso si cambian las leyes PDF):
python analysis.py

# Script para Refrescar el cruce final Topológico que se va hacia Excel de Microsoft:
python export_tda_excel.py
```

## Levantamiento Simultáneo de Tableros (Dashboards)

Existen tres interfaces interconectadas que actúan como "Ventanilla de Exploración Interactiva". El equipo técnico deberá servirlos con Streamlit hacia los navegadores de internet designados:

**Módulo 1: Mesa de Ayuda Coordinadores y Asignación Legal**
Panel con el formulario donde el comité asigna los `25 macro-clústeres detectados` pre-resueltos hacia áreas particulares (Técnica o Jurídica). Su estado local se almacena atómicamente en un `.json`.
```bash
python -m streamlit run dashboard.py --server.port 8503
```

**Módulo 2: Panel Visual y Grafo Normativo NetworkX**
Diagramadores analíticos espaciales (2D Scatters + Nodos relacionales PQR vs. Evidencia en Documentos Base de la CRA).
```bash
python -m streamlit run dashboard_topo.py --server.port 8504
```

**Módulo 3: Complejo TDA Avanzado Científico**
Entorno con la matriz 3-Tridimensional para analistas. Matriz cruzada (Categoría *Variable* contra *Variable Termal* o Zonal), generador de top words TF-IDF exclusivas del cúmulo ciudadano y el Motor de Búsqueda Vectorizada Ad-Hoc.
```bash
python -m streamlit run dashboard_analytics.py --server.port 8505
```

## Troubleshooting (Advertencias Comunes en Entornos Corporativos Locales)

*   **RuntimeWarning (OSFork o Threads):** El motor Transformer podría emitir una advertencia a nivel terminal debido al paralelismo asincrónico por defecto que intenta forzar HuggingFace Tokenizers por debajo para velocidad. Si causa inestabilidades bajo Windows nativo, establecer como variable de entorno previa: `export TOKENIZERS_PARALLELISM=false` o fijar `os.environ["TOKENIZERS_PARALLELISM"] = "false"` en el cabezote global de los scripts .py.
