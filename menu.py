import streamlit as st
import os

def render_menu():
    # Hide default sidebar nav
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Mini Header
        if os.path.exists("image/Logo_CRA.png"):
            st.image("image/Logo_CRA.png", use_container_width=True)
        
        st.markdown("### 🧭 Menú SABIA")
        
        # Central Hub
        st.page_link("Home.py", label="🏠 Inicio Académico", icon="🏛️")
        
        # Flujo 1: Análisis y Exploración TDA
        st.markdown("---")
        st.markdown("**1. Topología y Exploración**")
        st.page_link("pages/3_Analitica_Avanzada.py", label="Analítica Avanzada", icon="🔬")
        st.page_link("pages/2_Grafos_Topologicos.py", label="Cartografía Relacional", icon="🕸️")
        st.page_link("pages/8_Explorador_Microclusters.py", label="Lente Micro-Clústeres", icon="🔍")
        st.page_link("pages/7_Analisis_Sentimiento.py", label="Auditoría Térmica", icon="🌡️")
        
        # Flujo 2: Acción Institucional 
        st.markdown("---")
        st.markdown("**2. Respuestas Institucionales**")
        st.page_link("pages/1_Gestion_Respuestas.py", label="Gestión de Acuerdos", icon="⚖️")
        st.page_link("pages/6_Generador_Borradores.py", label="LLM Cero-Alucinación", icon="🤖")
        st.page_link("pages/9_Consultas_Individuales.py", label="Casos Singulares (Ruido)", icon="👤")
        
        # Flujo 3: Administración (Agrupada en Expander para limpieza UX)
        st.markdown("---")
        with st.expander("⚙️ Gestión Administrativa", expanded=False):
            st.markdown("Configuración y MLOps")
            st.page_link("pages/4_Administracion.py", label="Consola Admin", icon="💾")
            st.page_link("pages/5_Monitor_Calidad.py", label="Salud del Orquestador", icon="🩺")
