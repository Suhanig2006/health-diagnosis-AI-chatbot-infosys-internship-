import pytesseract
from pdf2image import convert_from_path
import re

def read_pdf_ocr(pdf_path):
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

def extract_parameters_from_text(text):
    patterns = {
        "Hemoglobin": r"Hemoglobin\s*[:\-]?\s*(\d+\.?\d*)",
        "WBC": r"WBC\s*[:\-]?\s*(\d+)",
        "Platelets": r"Platelets\s*[:\-]?\s*(\d+)"
    }

    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = float(match.group(1))

    return data
