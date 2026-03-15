import streamlit as st
import os
import glob
import pdfplumber
import google.generativeai as genai

# ==========================================
# 1. SETUP DE INTERFAZ Y BRANDING
# ==========================================
st.set_page_config(page_title='SABIA - Generador de Borradores Base', layout='wide', page_icon='🤖')
import menu
menu.render_menu()



st.markdown("""
<style>
    .stApp { background-color: #F8FBFF; }
    h1, h2, h3, h4 { color: #003366 !important; font-weight: 700 !important; }
    p, span, div, li { color: #2C3E50; }
    
    /* Configuración de Cajas de Generación */
    .draft-box {
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    textarea { font-family: 'Times New Roman', serif !important; font-size: 1.1rem !important; }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("image/Logo_CRA.png"):
        st.image("image/Logo_CRA.png", use_container_width=True)
with col_title:
    st.title("🤖 SABIA: Generador Asistido 'Cero-Alucinación'")
    st.markdown("**Asistente de Redacción Institucional - Sistema de respaldo basado exclusivamente en Acervo Normativo.**")

# ==========================================
# 2. DIRECTORIOS Y CONFIG BASE
# ==========================================
TRAIN_DIR = "entrenamiento_de_respuestas"
if not os.path.exists(TRAIN_DIR):
    os.makedirs(TRAIN_DIR)

st.sidebar.markdown("### 🔑 Credenciales Generador IA")
api_key = st.sidebar.text_input("Google Gemini API Key:", type="password", help="El token es efímero. No se almacena en el servidor por seguridad.")

if api_key:
    genai.configure(api_key=api_key)

# ==========================================
# 3. MÓDULOS DE CONOCIMIENTO
# ==========================================
@st.cache_data
def load_clusters():
    file_path = 'guia_estrategica_cra.md'
    if not os.path.exists(file_path): return []

    with open(file_path, 'r', encoding='utf-8') as f: content = f.read()

    raw_clusters = content.split('### Clúster ')[1:]
    clusters = []
    
    for raw in raw_clusters:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if not lines: continue
            
        header = lines[0]
        id_tema = header.split(':', 1)
        cluster_id = id_tema[0].strip()
        tema = id_tema[1].strip() if len(id_tema) > 1 else "Tema General"

        sintesis, estrategia, sustento = "", "", []
        cap_sin, cap_est = False, False
        
        for line in lines:
            if line.startswith('- **Síntesis'):
                cap_sin, cap_est = True, False; continue
            elif line.startswith('- **Estrategia'):
                cap_est, cap_sin = True, False; continue
            elif line.startswith('> **'):
                cap_sin, cap_est = False, False
                sustento.append(line.replace('>', '').strip()); continue
            elif line.startswith('- **') or line.startswith('---'):
                cap_sin, cap_est = False, False; continue

            if cap_sin: sintesis += line + " "
            if cap_est: estrategia += line + " "

        clusters.append({
            'identificador': f"Clúster {cluster_id}", 'tema': tema,
            'sintesis': sintesis.strip().replace('*', ''),
            'sustento': "\n".join(sustento), 'estrategia': estrategia.strip()
        })
    return clusters

@st.cache_data
def load_human_responses():
    pdfs = glob.glob(os.path.join(TRAIN_DIR, "*.pdf"))
    text_corpus = ""
    for pdf_p in pdfs:
        with pdfplumber.open(pdf_p) as pdf:
            for page in pdf.pages:
                text_corpus += (page.extract_text() or "") + "\n"
    return text_corpus

# ==========================================
# 4. INTERFAZ GENERATIVA
# ==========================================
clusters = load_clusters()
if not clusters:
    st.error("⚠️ Base Vectorial Vacía: Ejecute el orquestador principal en el módulo de Administración antes de intentar redactar.")
    st.stop()

colA, colB = st.columns([1, 2])

with colA:
    st.info("#### 1. Memoria de Tono (Few-Shot)")
    st.markdown("Suba PDFs con respuestas legales previas *ya firmadas*. La IA imitará su estructura gramatical de despídida y saludo sin inventar la ley.")
    
    with st.form("train_form"):
        uploaded_pdfs = st.file_uploader("Entrenar con Acervo PDF Histórico:", type=["pdf"], accept_multiple_files=True)
        if st.form_submit_button("💾 Absorber Estilo Institucional", type="primary", use_container_width=True):
            if uploaded_pdfs:
                for pdf in uploaded_pdfs:
                    with open(os.path.join(TRAIN_DIR, pdf.name), "wb") as f:
                        f.write(pdf.getbuffer())
                st.success("Tono memorizado.")
                st.cache_data.clear()
                st.rerun()
            
    pdf_count = len(glob.glob(os.path.join(TRAIN_DIR, "*.pdf")))
    st.caption(f"📚 Vectorizando **{pdf_count}** documentos humanos referenciales.")
    
    st.divider()
    st.info("#### 2. Selección de Tópico Ciudadano")
    opciones = [c['identificador'] + " - " + c['tema'][:40] + "..." for c in clusters]
    seleccion = st.selectbox("Apuntar motor generativo al grupo:", opciones)
    
    idx_seleccionado = opciones.index(seleccion)
    c_data = clusters[idx_seleccionado]
    
    with st.expander("Inspeccionar Parámetros de Inyección (Prompt Base)"):
        st.write("**Clamor Popular:**", c_data['sintesis'])
        st.write("**Restricción Estratégica:**", c_data['estrategia'])
        st.write("**Bloqueo Cognitivo (Solo usar estos Artículos):**", c_data['sustento'])

with colB:
    st.info("#### 3. Sala de Redacción Autómata")
    st.markdown("Generación determinística (`Temperature = 0.0`). La máquina construirá un alegato estricto, frío y respaldado únicamente por los nodos documentales.")
    
    if st.button("🚀 Iniciar Redacción Asistida (IA)", type="primary"):
        if not api_key:
            st.error("⚠️ Token de Google Cloud / Gemini ausente en el Panel de Administración.")
        else:
            with st.spinner("Ensamblando sintaxis y validando restricciones de Cero-Alucinación..."):
                try:
                    human_style = load_human_responses()
                    
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
                    
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.0, top_p=0.95, top_k=20
                        )
                    )
                    
                    st.success("✅ Algoritmo Completado. (Validación Cero-Alucinación Exitosa)")
                    
                    st.markdown("""<div class="draft-box">""", unsafe_allow_html=True)
                    st.text_area("Cuerpo Legal del Borrador (Exportar a Microsoft Word):", value=response.text, height=450)
                    st.markdown("""</div>""", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    md_draft = response.text.encode('utf-8')
                    st.download_button(
                        label=f"📥 Descargar Borrador Oficial (.md)",
                        data=md_draft,
                        file_name=f"Borrador_Respuesta_Cluster_{c_data['identificador']}.md",
                        mime="text/markdown",
                        type="primary",
                        use_container_width=True,
                        help="Descargue el archivo Markdown, el cual es directamente compatible con Microsoft Word y preservar formato."
                    )
                    st.markdown("""</div>""", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Falla inter-nodo con la API Generativa: {str(e)}")
