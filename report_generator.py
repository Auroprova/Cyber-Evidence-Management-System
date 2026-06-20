import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(case_id, category, severity, iocs, file_hash):

    os.makedirs("reports", exist_ok=True)

    report_path = f"reports/case_{case_id}.pdf"

    pdf = canvas.Canvas(report_path, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 780, "Cyber Evidence Management Report")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 750, f"Case ID: {case_id}")
    pdf.drawString(50, 730, f"Category: {category}")
    pdf.drawString(50, 710, f"Severity: {severity}")

    pdf.drawString(50, 680, "Extracted Indicators of Compromise (IOCs):")

    y = 660

    for key, value in iocs.items():
        pdf.drawString(70, y, f"{key}: {', '.join(value) if value else 'None'}")
        y -= 20

    pdf.drawString(50, y - 10, "SHA-256 Evidence Hash:")
    pdf.drawString(70, y - 30, file_hash)

    pdf.save()

    return report_path

print("PDF Report Generator Ready")