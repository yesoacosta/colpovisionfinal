
import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

st.set_page_config(page_title="ColpoVision Final", layout="wide")
st.title("🩺 ColpoVision – Diagnóstico IA + Informe Profesional")

# Simulación de IA real (integrar modelo real aquí)
def analizar_imagen(img):
    return {
        "diagnostico": "🔴 Sospechosa de lesión de alto grado (NIC 2-3)",
        "confianza": "91%",
        "prioridad": "🚨 Urgente",
        "recomendacion": "Biopsia dirigida inmediata + derivación según protocolo"
    }

uploaded_img = st.file_uploader("📷 Subí una imagen colposcópica", type=["jpg", "jpeg", "png"])

if uploaded_img:
    st.image(uploaded_img, caption="Imagen cargada", use_column_width=True)
    resultado = analizar_imagen(uploaded_img)

    st.subheader("🔬 Resultado automático por IA")
    st.success(f"**Diagnóstico IA:** {resultado['diagnostico']}")
    st.info(f"**Confianza:** {resultado['confianza']}")
    st.warning(f"**Nivel de prioridad:** {resultado['prioridad']}")

    st.text_area("📝 Recomendación sugerida (editable):", value=resultado['recomendacion'], key="reco_editable")

    st.subheader("📋 Informe clínico")
    nombre = st.text_input("Nombre del paciente:")
    edad = st.text_input("Edad:")
    fecha = st.date_input("Fecha del estudio:", value=datetime.today())
    motivo = st.text_area("Motivo de consulta:")
    tecnica = st.text_area("Técnica y métodos utilizados:")
    hallazgos = st.text_area("Hallazgos colposcópicos:")
    impresion = st.text_area("Impresión diagnóstica:")
    recomendaciones = st.text_area("Recomendaciones finales:", value=st.session_state.reco_editable)

    if st.button("📄 Exportar PDF"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("🧾 Informe Colposcópico - ColpoVision", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Dr. Yesid Acosta Peinado – Ginecólogo y Obstetra", styles['Normal']))
        story.append(Paragraph("M.P. 33210 – M.E. 16665", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Fecha: {fecha.strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"Paciente: {nombre}", styles['Normal']))
        story.append(Paragraph(f"Edad: {edad}", styles['Normal']))
        story.append(Paragraph(f"Motivo: {motivo}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"📸 Diagnóstico IA: {resultado['diagnostico']} – {resultado['confianza']}", styles['Normal']))
        story.append(Paragraph(f"Prioridad: {resultado['prioridad']}", styles['Normal']))
        story.append(Paragraph(f"Recomendación: {recomendaciones}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Técnica utilizada:", styles['Heading3']))
        story.append(Paragraph(tecnica, styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Hallazgos colposcópicos:", styles['Heading3']))
        story.append(Paragraph(hallazgos, styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Impresión diagnóstica:", styles['Heading3']))
        story.append(Paragraph(impresion, styles['Normal']))
        story.append(Spacer(1, 24))
        try:
            image_stream = Image.open(uploaded_img)
            img_path = "/tmp/image_temp.jpg"
            image_stream.save(img_path)
            story.append(RLImage(img_path, width=12*cm, height=9*cm))
        except:
            story.append(Paragraph("Imagen no disponible para impresión", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Firma digital:", styles['Normal']))
        try:
            story.append(RLImage("firma_yesid.png", width=5*cm, height=2*cm))
        except:
            story.append(Paragraph("[Firma]", styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        st.download_button("📥 Descargar informe PDF", buffer, "informe_colposcopico.pdf", mime="application/pdf")
