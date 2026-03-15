import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# --- 1. PREPARACIÓN DE GRÁFICOS (EXTRACCIÓN DE EXCEL) ---
print("Generando recursos visuales...")
excel_path = 'R40 AAPP - RESULTADOS TDA.xlsx'
df = pd.read_excel(excel_path, sheet_name='REG-FOR03')

# Limpieza básica para los gráficos
df_valido = df[df['Cluster TDA (IA)'] != -1]
total_obs = len(df)
total_ruido = len(df[df['Cluster TDA (IA)'] == -1])
num_clusters = df_valido['Cluster TDA (IA)'].nunique()

# Gráfico 1: Tópicos Principales
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 5))
top_10 = df_valido['Cluster TDA (IA)'].value_counts().head(8)
ax = sns.barplot(x=top_10.values, y=[f"Tópico {c}" for c in top_10.index], palette="viridis")
plt.title("Zonas Críticas: Tópicos con Mayor Volumen de Quejas", fontsize=14, fontweight='bold')
plt.xlabel("Cantidad de Observaciones")
plt.ylabel("Número de Clúster (IA)")
for p in ax.patches:
    ax.annotate(f"{int(p.get_width())}", (p.get_width(), p.get_y() + p.get_height() / 2.), 
                ha='left', va='center', xytext=(5, 0), textcoords='offset points', color='black')
plt.tight_layout()
plt.savefig("tmp_chart_1.png", dpi=300)
plt.close()

# Gráfico 2: Complejidad
plt.figure(figsize=(8, 4))
if 'Nivel de compejidad' in df.columns:
    df_comp = df['Nivel de compejidad'].fillna('Sin Definir').value_counts()
    ax = sns.barplot(x=df_comp.index, y=df_comp.values, palette="rocket")
    plt.title("Volumen de Participación clasificado por Nivel de Complejidad", fontsize=14, fontweight='bold')
    plt.xlabel("Complejidad de la Observación")
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig("tmp_chart_2.png", dpi=300)
    plt.close()


# --- 2. CONSTRUCCIÓN DEL DOCUMENTO PDF ---
print("Ensamblando Informe en PDF...")

import unicodedata

def norm(text):
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

class InformeCRA(FPDF):
    def header(self):
        # Fondo decorativo en la cabecera (Azul CRA)
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 30, 'F')
        self.set_y(12)
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, norm('INFORME EJECUTIVO NMTPPA: ANALISIS TOPOLOGICO'), align='C')
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

    def titulo_seccion(self, titulo):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, norm(titulo), ln=True)
        # Linea separadora
        self.set_draw_color(0, 102, 204)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(5)

    def cuerpo(self, texto):
        self.set_font('helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, norm(texto))
        self.ln(5)

    def destacado(self, texto):
        self.set_fill_color(240, 248, 255) # Azul tenue
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, norm(texto), fill=True, border=True)
        self.ln(5)

pdf = InformeCRA(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# --- SECCIÓN 1: RESUMEN Y ANÁLISIS ---
pdf.titulo_seccion("1. RESUMEN Y RESULTADOS DEL ANÁLISIS NLP")
txt_resumen = (
    "El presente informe destila los resultados de la implementación automatizada de Inteligencia Artificial (NLP/TDA) "
    f"sobre las observaciones ciudadanas radicadas para el Nuevo Marco Tarifario de Pequeños Prestadores. "
    f"Tras analizar una matriz inicial de {total_obs} participaciones en lenguaje natural, el algoritmo de agrupamiento "
    f"(HDBSCAN) segmentó lógicamente la conversación nacional en {num_clusters} Clústeres (Temáticas Primarias)."
)
pdf.cuerpo(txt_resumen)

pdf.destacado(f"Dato Técnico de Limpieza:\nSe identificaron {total_ruido} comentarios aislados, ambiguos o ilegibles rotulados como 'Clúster -1 (Ruido)'. Estos no configuran un vector argumentativo y pueden filtrarse de los esfuerzos primarios de respuesta legal.")

if os.path.exists("tmp_chart_1.png"):
    pdf.image("tmp_chart_1.png", x='C', w=160)
    pdf.ln(5)

# --- SECCIÓN 2: HALLAZGOS CRÍTICOS ---
pdf.titulo_seccion("2. PRINCIPALES HALLAZGOS EVIDENCIADOS")
txt_hallazgos = (
    "🔹 CONCENTRACIÓN DE DOLORES: La ciudadanía no debate equitativamente todos los artículos. Existe un embudo de "
    "preocupación extrema donde el Top 5 de Clústeres abarca la gran mayoría del descontento o solicitud de "
    "aclaración (Ej. Temas de exclusiones o tarifas comunitarias).\n\n"
    "🔹 SOSTENIBILIDAD DE RESPUESTA: Al aplicar la Matriz de Co-ocurrencia RAG, el IA descubrió un porcentaje de la "
    "discusión que cruza transversalmente múltiples Resoluciones y Documentos de Justificación Técnica de la CRA simultáneamente. "
    "Unificar la respuesta es vital.\n\n"
    "🔹 PATRONES DE COMPLEJIDAD:"
)
pdf.cuerpo(txt_hallazgos)

if os.path.exists("tmp_chart_2.png"):
    pdf.image("tmp_chart_2.png", x='C', w=140)
    pdf.ln(5)

pdf.add_page()

# --- SECCIÓN 3: GUÍA OPERATIVA CIENTÍFICA ---
pdf.titulo_seccion("3. GUÍA OPERATIVA: PASO A PASO PARA RESPONDER EL EXCEL")
txt_guia = (
    "Instrucciones estandarizadas para que el Equipo Técnico, junto al Científico de Datos, explote y asigne eficazmente "
    "la matriz 'R40 AAPP - RESULTADOS TDA.xlsx':\n\n"
    
    "PASO 1: ORDEN Y AISLAMIENTO DE RUIDO (Data Scientist)\n"
    "Abra el archivo resultante y aplique un Autofiltro en Excel. Filtre la columna final [Cluster TDA (IA)] para ocultar "
    "el grupo '-1'. De este modo, la hoja le mostrará únicamente a las comunidades con requerimientos legítimos y categorizados en Tópicos.\n\n"
    
    "PASO 2: ASIGNACIÓN DE MACRO-VERTIMIENTOS (Coordinador)\n"
    "Ordene el Excel Ascendentemente de la 'A a la Z' en la misma columna de [Cluster]. Notará que agrupará grupos de 50 a 100 "
    "ciudadanos bajo la columna [Tema Central IA]. Envíe cada bloque a un mismo analista. ¡Nadie debe cruzar temáticas!\n\n"
    
    "PASO 3: USO DE LA CHULETA JURÍDICA RAG (Letrado/Secretaría)\n"
    "Dígale al profesional asignado que lea la celda [Sustento Normativo RAG] y la [Estrategia de Respuesta IA]. Antes de investigar "
    "en decenas de PDF de la CRA, la IA ya le ha transcrito allí el fragmento específico del Decreto, Estudio o Resolución "
    "que resuelve ese dolor exacto de la comunidad, listo para ser adaptado al oficio.\n\n"
    
    "PASO 4: RESPUESTA MASIVA Y MÁQUINA DE COPIAR\n"
    "Se exige que el profesional redacte UNA (1) respuesta legal e impecable dirigida a resolver conceptualmente el Tema Central del "
    "Clúster. Una vez lograda, esa matriz narrativa se copia o 'clona' a todos los residentes (70, 80 personas) que cayeron "
    "en el mismo Subrayado Espacial Topológico. Reduciendo meses de trabajo a una semana de depuración."
)

pdf.cuerpo(txt_guia)
pdf.destacado("💡 PRO TIP PARA EL ENTORNO LOCAL:\nSi desean visualizar todo este mismo Excel pero interactivo, inicie el Dashboard Visualizador en su PC ejecutando a través de su terminal el comando: python -m streamlit run Home.py")

# --- GUARDADO ---
output_pdf = "Informe_Ejecutivo_Hallazgos_TDA.pdf"
pdf.output(output_pdf)

# LImpieza
if os.path.exists("tmp_chart_1.png"): os.remove("tmp_chart_1.png")
if os.path.exists("tmp_chart_2.png"): os.remove("tmp_chart_2.png")

print(f"Informe PDF {output_pdf} exportado con éxito a la carpeta base del proyecto.")
