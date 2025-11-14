import requests
from datetime import datetime, timedelta
import re
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


# === CONFIGURE OUTPUT DIRECTORY ===
OUTPUT_FOLDER = r"C:\Users\Alba Palacio\Desktop\CYBERSECURITY\Phyton 2\Week 13"

# Ensure folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Clean HTML from descriptions
def clean_html(text):
    if not text:
        return ""

    text = re.sub(r'<a[^>]*>', '', text)
    text = text.replace("</a>", "")
    text = text.replace("<br>", "\n").replace("<br/>", "\n")
    text = re.sub(r'<.*?>', '', text)

    return text


# PDF Report Function
def create_pdf_report(breaches):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")

    pdf_filename = f"HIBP_Weekly_Report_{timestamp}.pdf"

    # ABSOLUTE PATH for the PDF
    pdf_path = os.path.join(OUTPUT_FOLDER, pdf_filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("Weekly HIBP Breach Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # Date generated
    content.append(Paragraph(f"Generated on: {timestamp} UTC", styles["Normal"]))
    content.append(Spacer(1, 20))

    if not breaches:
        content.append(Paragraph("No breaches were added in the last 7 days.", styles["Normal"]))
    else:
        for b in breaches:
            safe_description = clean_html(b["Description"])

            entry = f"""
                <b>Name:</b> {b['Name']}<br/>
                <b>Domain:</b> {b['Domain']}<br/>
                <b>Breach Date:</b> {b['BreachDate']}<br/>
                <b>Added to HIBP:</b> {b['AddedDate']}<br/>
                <b>Data Exposed:</b> {', '.join(b['DataClasses'])}<br/>
                <b>Description:</b> {safe_description[:500]}...
            """

            content.append(Paragraph(entry, styles["Normal"]))
            content.append(Spacer(1, 12))

    doc.build(content)

    print("PDF report generated:", pdf_path)


# HIBP data collection
url = "https://haveibeenpwned.com/api/v3/breaches"
response = requests.get(url, headers={"User-Agent": "CTI-Lab-Student"})

if not response.ok:
    print("Error fetching data:", response.status_code)
    exit()

breaches = response.json()

today = datetime.utcnow()
week_ago = today - timedelta(days=7)

recent_breaches = []

for breach in breaches:
    added_date_str = breach.get("AddedDate", "")
    if added_date_str:
        added_date = datetime.strptime(added_date_str, "%Y-%m-%dT%H:%M:%SZ")
        if added_date >= week_ago:
            recent_breaches.append({
                "Name": breach["Name"],
                "Domain": breach["Domain"],
                "BreachDate": breach["BreachDate"],
                "AddedDate": added_date_str,
                "DataClasses": breach["DataClasses"],
                "Description": breach["Description"]
            })

create_pdf_report(recent_breaches)
