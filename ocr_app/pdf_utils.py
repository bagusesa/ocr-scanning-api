import os
from pdf2image import convert_from_bytes
import easyocr

def convert_pdf_to_text(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)

    combined_text = ""  # Initialize an empty string to store combined text

    # Initialize EasyOCR
    reader = easyocr.Reader(['en'])

    for i, image in enumerate(images):
        # Save the image temporarily
        image_path = f"image_{i}.jpg"
        image.save(image_path)

        # Perform OCR on the image
        result = reader.readtext(image_path)

        # Extract the text from OCR results and add it to the combined text
        text = " ".join([item[1] for item in result])
        combined_text += text + " "

        # Remove the temporary image file
        os.remove(image_path)

    return combined_text

def count_matched_sections(text, input_sections):
    text = text.lower()
    input_sections = [section.lower() for section in input_sections]
    matched_sections = sum(1 for section in input_sections if section in text)
    return matched_sections
