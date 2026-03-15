import streamlit as st
import os
import glob
import pdfplumber
import google.generativeai as genai

st.set_page_config(page_title='Generador de Borradores (LLM)', layout='wide', page_icon='🤖')
st.title("🤖 Generador de Borradores Asistido por Inteligencia Artificial")
st.markdown("Integra el análisis Topológico/RAG con Modelos de Lenguaje Grandes (LLMs) para auto-redactar el borrador de respuesta oficial de la CRA.")

# Directorio de entrenamiento
TRAIN_DIR = "entrenamiento_de_respuestas"
if not os.path.exists(TRAIN_DIR):
    os.makedirs(TRAIN_DIR)

st.sidebar.header("🔑 Configuración del LLM")
api_key = st.sidebar.text_input("Ingresa tu Google Gemini API Key:", type="password", help="Tu llave no se guarda, desaparece al cerrar la aplicación.")

if api_key:
    genai.configure(api_key=api_key)

# 1. Función para cargar clusters del markdown (reutilizamos lógica)
@st.cache_data
def load_clusters():
    file_path = 'guia_estrategica_cra.md'
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_clusters = content.split('### Clúster ')[1:]
    clusters = []
    
    for raw in raw_clusters:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if not lines:
            continue
            
        header = lines[0]
        id_tema = header.split(':', 1)
        cluster_id = id_tema[0].strip()
        tema = id_tema[1].strip() if len(id_tema) > 1 else "Tema General"

        sintesis, estrategia = "", ""
        sustento = []
        cap_sin, cap_est = False, False
        
        for line in lines:
            if line.startswith('- **Síntesis'):
                cap_sin, cap_est = True, False
                continue
            elif line.startswith('- **Estrategia'):
                cap_est, cap_sin = True, False
                continue
            elif line.startswith('> **'):
                cap_sin, cap_est = False, False
                sustento.append(line.replace('>', '').strip())
                continue
            elif line.startswith('- **') or line.startswith('---'):
                cap_sin, cap_est = False, False
                continue

            if cap_sin: sintesis += line + " "
            if cap_est: estrategia += line + " "

        clusters.append({
            'id': cluster_id,
            'identificador': f"Clúster {cluster_id}",
            'tema': tema,
            'sintesis': sintesis.strip().replace('*', ''),
            'sustento': "\n".join(sustento),
            'estrategia': estrategia.strip()
        })
    return clusters

# 2. Funciones para leer PDFs humanos
@st.cache_data
def load_human_responses():
    pdfs = glob.glob(os.path.join(TRAIN_DIR, "*.pdf"))
    text_corpus = ""
    for pdf_p in pdfs:
        with pdfplumber.open(pdf_p) as pdf:
            for page in pdf.pages:
                text_corpus += (page.extract_text() or "") + "\n"
    return text_corpus

# --- Carga de datos ---
clusters = load_clusters()
if not clusters:
    st.warning("No hay Clústeres procesados. Por favor ejecute el Motor NLP en el panel de Administración.")
    st.stop()

colA, colB = st.columns([1, 2])

with colA:
    st.header("1. Material de Entrenamiento 🧠")
    st.markdown("Sube respuestas oficiales (PDFs ya validados y firmados por la CRA) para que el modelo aprenda el tono institucional.")
    
    uploaded_pdfs = st.file_uploader("Subir PDFs de Respuestas Exitosas Anteriores:", type=["pdf"], accept_multiple_files=True)
    if st.button("💾 Entrenar con estos PDFs"):
        if uploaded_pdfs:
            for pdf in uploaded_pdfs:
                with open(os.path.join(TRAIN_DIR, pdf.name), "wb") as f:
                    f.write(pdf.getbuffer())
            st.success("PDFs guardados exitosamente. Memoria de estilo actualizada.")
            st.cache_data.clear()
            st.rerun()
            
    # Mostrar cuantos hay
    pdf_count = len(glob.glob(os.path.join(TRAIN_DIR, "*.pdf")))
    st.info(f"📚 Actualmente el generador usa **{pdf_count} documento(s)** como molde estilístico.")
    
    st.divider()
    st.header("2. Seleccionar Tópico Ciudadano")
    opciones = [c['identificador'] + " - " + c['tema'][:40] + "..." for c in clusters]
    seleccion = st.selectbox("Elija el grupo a responder:", opciones)
    
    idx_seleccionado = opciones.index(seleccion)
    c_data = clusters[idx_seleccionado]
    
    with st.expander("Inspeccionar Contexto TDA Alimentado a la IA"):
        st.write("**Síntesis:**", c_data['sintesis'])
        st.write("**Estrategia:**", c_data['estrategia'])
        st.write("**Artículos RAG:**", c_data['sustento'])

with colB:
    st.header("3. Redacción Asistida")
    st.markdown("Presiona generar para redactar la carta oficial unificando el Análisis de Datos y el Estilo Institucional.")
    
    if st.button("🚀 Generar Borrador Inteligente", type="primary"):
        if not api_key:
            st.error("⚠️ Debes configurar la API Key de Google Gemini en la barra lateral para utilizar la Inteligencia Artificial Generativa.")
        else:
            with st.spinner("La IA está analizando los PDF legales y redactando la respuesta... (Esto toma unos segundos)"):
                try:
                    # Traer el estilo validado
                    human_style = load_human_responses()
                    
                    # Prompt engineering
                    prompt = f"""
                    ====================================
                    SISTEMA DE REDACCIÓN LEGAL ESTRICTA - DIRECTRICES DE CERO-ALUCINACIÓN
                    ====================================
                    Actúa EXCLUSIVAMENTE como un Abogado Senior y Redactor Legal Experto de la Comisión de Regulación de Agua Potable y Saneamiento Básico (CRA) de Colombia.
                    Tu tarea es redactar el cuerpo de una carta formal de respuesta para responder a un grupo ciudadano que participó en la construcción del Nuevo Marco Tarifario (NMTPPA).
                    
                    REGLAS CRÍTICAS (DE OBLIGATORIO CUMPLIMIENTO):
                    1. CERO ALUCINACIÓN LEGAL: NO INVENTES, infieras, ni supongas leyes, decretos, números de resolución, artículos o jurisprudencia. 
                    2. FUENTE ÚNICA DE VERDAD: Si vas a citar o mencionar sustento jurídico, DEBES usar ÚNICAMENTE el texto proporcionado abajo en "ARTÍCULOS O SUSTENTO JURÍDICO A INCLUIR/MENCIONAR".
                    3. LÍMITE DE RESPUESTA: Si los artículos provistos no responden completamente la pregunta ciudadana, limita tu redacción a una respuesta parcial institucional e indica explícitamente que "el resto de la inquietud se encuentra bajo estudio detallado por el equipo técnico", sin inventar la solución.
                    4. ESTRUCTURA: Mantén un tono formal institucional.
                    
                    A CONTINUACIÓN EL CONTEXTO OBTENIDO DEL NLP:
                    - TEMA DE LA CIUDADANÍA: {c_data['tema']}
                    - SÍNTESIS DEL RECLAMO SOCIAL: {c_data['sintesis']}
                    - ESTRATEGIA DE COMUNICACIÓN SUGERIDA: {c_data['estrategia']}
                    
                    - ARTÍCULOS O SUSTENTO JURÍDICO A INCLUIR/MENCIONAR (USAR SOLO ESTO):
                    {c_data['sustento']}
                    """
                    
                    if human_style.strip():
                        prompt += f"""
                        
                        A CONTINUACIÓN ALGUNAS RESPUESTAS LEGALES ANTERIORES PARA QUE REPLIQUES EXACTAMENTE EL TONO INSTITUCIONAL, Y SU SALUDO/DESPEDIDA:
                        (Ignora los temas específicos de estos ejemplos, solo imita su tono, seriedad y estructura gramatical):
                        {human_style[:3000]}
                        """
                        
                    prompt += """
                    
                    INSTRUCCIONES FINALES:
                    Redacta ÚNICAMENTE el cuerpo de la carta de respuesta. Debe ser profesional, clara, asertiva y cordial, justificando la postura de la CRA estrictamente con los artículos brindados, y respondiendo la inquietud central.
                    """
                    
                    # Modelo con Temperature 0 para máximo determinismo y minimizar creatividad/alucinaciones
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.0,
                            top_p=0.95,
                            top_k=20
                        )
                    )
                    
                    st.success("✅ Generación Completada")
                    st.markdown("### Borrador Oficial Obtenido:")
                    st.markdown(f"> {response.text}")
                    
                    # Proveer caja de texto y boton copiar (simulado como st.text_area para facil copia)
                    st.text_area("Copia y Pega este borrador en tu formato de Word oficial:", value=response.text, height=350)
                    
                except Exception as e:
                    st.error(f"Falla de conexión o error en el modelo: {str(e)}")
