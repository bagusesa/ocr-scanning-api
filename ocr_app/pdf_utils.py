import os
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR

def convert_pdf_to_text(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)

    result_txt = []

    # Initialize EasyOCR
    reader = PaddleOCR(lang="id", use_gpu=False, show_log=False)

    for i, image in enumerate(images):
        # Save the image temporarily
        image_path = f"image_{i}.jpg"
        image.save(image_path)

        # Perform OCR on the image
        result = reader.ocr(image_path, cls=False, det=True, rec=True)

        result_txt.extend([" ".join([word_info[1][0] for word_info in line]) for line in result])

        # Remove the temporary image file
        os.remove(image_path)

    result_txt = " ".join(result_txt)

    return result_txt

def count_matched_sections(text, input_sections):
    text = text.lower()
    input_sections = [section.lower() for section in input_sections]
    matched_sections = sum(1 for section in input_sections if section in text)
    return matched_sections
