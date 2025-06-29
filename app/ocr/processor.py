import os
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata'  # ✅ this time with 'tessdata'

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extract_text_from_pdf(pdf_path, lang="eng"):
    images = convert_from_path(pdf_path)
    full_text = ""

    for img in images:
        text = pytesseract.image_to_string(img, lang=lang)
        full_text += text + "\n"

    return full_text
