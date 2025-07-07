# ───── Imports ─────
import os
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata'  # Set before pytesseract

import pytesseract
from pdf2image import convert_from_path
from PIL import Image


# ───── PDF OCR Function ─────
def extract_text_from_pdf(pdf_path, lang="eng"):
    images = convert_from_path(pdf_path)
    full_text = ""

    for img in images:
        text = pytesseract.image_to_string(img, lang=lang)
        full_text += text + "\n"

    return full_text


# ───── Image OCR Function ─────
def extract_text_from_image(image_path, lang="eng"):
    print(f"📸 Running image OCR on {image_path} with lang={lang}")
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text
