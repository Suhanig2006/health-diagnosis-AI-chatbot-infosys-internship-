from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO


def generate_pdf_report(age, gender, interpretations, risk, summary):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("AI Health Diagnostic Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Patient Info
    elements.append(Paragraph(f"<b>Age:</b> {age}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Gender:</b> {gender}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Interpretation Table
    elements.append(Paragraph("Parameter Interpretations", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    table_data = [["Parameter", "Value", "Status"]]

    for param, details in interpretations.items():
        value = details.get("value", "N/A")
        status = details.get("status", "N/A")
        table_data.append([param, str(value), status])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Risk Section
    elements.append(Paragraph("Risk Assessment", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(str(risk), styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Summary Section
    elements.append(Paragraph("Summary", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(summary, styles["Normal"]))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    return buffer