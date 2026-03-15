# MANUAL DE DESPLIEGUE CONTINUO Y OPERACIÓN - PLATAFORMA SABIA (CRA)

SABIA (Sistema de Análisis Basado en Inteligencia Artificial) es un ecosistema Python/Streamlit que no requiere contenedores Docker complejos para operar, garantizando un despliegue veloz y soberano dentro de los equipos de la Comisión.

## 1. Requisitos del Sistema Base
*   **Sistema Operativo:** Windows 10/11 Profesional, Linux (Ubuntu/Debian) o macOS.
*   **Hardware (Recomendado):** Procesador M1/x64 moderno o superior de 4 núcleos (mínimo). Memoria RAM mínima de 8 GB (Recomendado 16 GB).
*   **Python:** Entorno Limpio Versión `>= 3.9` hasta `3.11`.
*   **Compilador subyacente:** Visual Studio C++ Build Tools (Solo Windows: Necesario para compilar UMAP/HDBSCAN sin error Rueda (`wheel`)).

---

## 2. Instrucciones de Instalación Local y Despliegue en 4 Pasos

1. **Clonación del Repositorio:**
Descargue el ecosistema y entre a la carpeta.
```powershell
git clone <url-del-repositorio>
cd CRA-ControlSocial-NMTPPA
```

2. **Creación del Entorno Aislado Virtual (`venv`):**
Cree un ambiente Python dedicado y hermético por seguridad.
```powershell
python -m venv venv

# En Windows Activar:
.\venv\Scripts\Activate.ps1

# En Linux / Mac Activar:
source venv/bin/activate
```

3. **Inyección de Dependencias Científicas:**
Instalar las sub-librerías matemáticas requeridas para la Topología Numérica y Streamlit puro.
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

*(Si su red corporativa CRA presenta proxys bloqueantes para la descarga del Transformer, desactive SSL o contacte a IT de la Institución)*

4. **Arranque en Caliente del Servidor Web (Localhost):**
El servicio subirá la Interfaz SABIA directamente a su navegador local en segundos.
```powershell
python -m streamlit run Home.py
```
Acceda en `http://localhost:8501`.

---

## 3. Configuración Inicial e Ingesta de Primer Uso
1. Una vez desplegada la Interfaz, diríjase al módulo en la barra de menú: **⚙️ Consola Admin**.
2. Arrastre en la "Capa 1" la matriz base provista por el Ministerio (Ej. `R40 AAPP - FINAL.xlsx`). 
3. Arrastre Documentos Institucionales (`.pdf`) y las Resoluciones del Régimen Tarifario hacia la subsección RAG.
4. Presione en **"🚀 Lanzar Motor de Inteligencia (Pipeline A)"**.
5. *Nota:* La primera ejecución de la red neuronal demorará algo más debido a la descarga del Modelo Multilingüe `MiniLM-L12` (~150 MB) al disco caché local. Las siguientes ejecuciones serán instántaneas.

---

## 4. Estructura de Integridad de Directorios Críticos
El software asume que en el mismo vector o carpeta local operen:
*   `config.json`: Registra qué base de datos está enganchada al sistema y no debe borrarse accidentalmente. (Si no existe, se crea solo).
*   `Base de Conocimiento/`: Carpeta protegida o directorio donde se lanzan los PDFs de las Leyes / Formularios CRA oficiales de los que bebe el Ecosistema para no inducir "alucinación" en sus respuestas.
*   `entrenamiento_de_respuestas/`: Carpeta que guarda los manuales PDF viejos con que la IA mimetiza ("Few-Shot") el léxico, estilo burocrático, encabezado y pie de página de las cartas de los años pasados.
*   `/pages/`: Motor Multi-Página de Streamlit que orquesta y lanza los 8 módulos restantes desde su Enrutador inyectado en `menu.py` hacia `Home.py`.
