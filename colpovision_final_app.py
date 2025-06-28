import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import tempfile
import os

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
        
        # Manejo corregido de la imagen
        try:
            # Crear un archivo temporal para la imagen
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                # Abrir la imagen subida
                image_stream = Image.open(uploaded_img)
                # Convertir a RGB si es necesario (para PNG con transparencia)
                if image_stream.mode in ("RGBA", "P"):
                    image_stream = image_stream.convert("RGB")
                # Guardar en el archivo temporal
                image_stream.save(tmp_file.name, format='JPEG')
                # Agregar la imagen al PDF
                story.append(RLImage(tmp_file.name, width=12*cm, height=9*cm))
                # Limpiar el archivo temporal después de usar
                os.unlink(tmp_file.name)
        except Exception as e:
            st.error(f"Error al procesar la imagen: {str(e)}")
            story.append(Paragraph("Imagen no disponible para impresión", styles['Normal']))
        
        story.append(Spacer(1, 12))
        story.append(Paragraph("Firma digital:", styles['Normal']))
        
        # Manejo corregido de la firma - buscar si existe el archivo
        try:
            if os.path.exists("firma_yesid.png"):
                story.append(RLImage("firma_yesid.png", width=5*cm, height=2*cm))
            else:
                story.append(Paragraph("Dr. Yesid Acosta Peinado", styles['Normal']))
                story.append(Paragraph("Ginecólogo y Obstetra", styles['Normal']))
                story.append(Paragraph("M.P. 33210 – M.E. 16665", styles['Normal']))
        except Exception as e:
            st.error(f"Error al cargar la firma: {str(e)}")
            story.append(Paragraph("Dr. Yesid Acosta Peinado", styles['Normal']))
            story.append(Paragraph("Ginecólogo y Obstetra", styles['Normal']))
            story.append(Paragraph("M.P. 33210 – M.E. 16665", styles['Normal']))

        try:
            doc.build(story)
            buffer.seek(0)
            st.download_button("📥 Descargar informe PDF", buffer, "informe_colposcopico.pdf", mime="application/pdf")
            st.success("✅ PDF generado correctamente!")
        except Exception as e:
            st.error(f"Error al generar el PDF: {str(e)}")
