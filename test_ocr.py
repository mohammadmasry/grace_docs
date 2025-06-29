import os
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/'  # make sure this is BEFORE pytesseract

import pytesseract
from pdf2image import convert_from_path

pdf_path = '/Users/mohammadalmasry/Downloads/german_discharge_summary.pdf'  # 🔁 change this to your actual file name

images = convert_from_path(pdf_path)

print("✅ Converted PDF to image")

text = pytesseract.image_to_string(images[0], lang='deu', config='--tessdata-dir "/usr/local/share/tessdata/"')

print("\n📄 OCR Output:\n")
print(text)
