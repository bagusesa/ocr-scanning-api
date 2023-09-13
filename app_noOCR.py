from flask import Flask, request, jsonify
#import easyocr
import fitz  # PyMuPDF

app = Flask(__name__)
#reader = easyocr.Reader(['en'])

@app.route('/scan_pdf', methods=['POST'])
def scan_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
   
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
   
    input_name = request.form.get('name')
    input_student_id = request.form.get('student_id')
    input_universities = request.form.get('university')
    input_publish_in = request.form.get('publish_in')
    input_publish_en = request.form.get('publish_en')
    
    if file:
        pdf_bytes = file.read()

        # Extract text from the PDF using PyMuPDF
        extracted_text = extract_text_from_pdf(pdf_bytes)
        
        # Add spaces before and after each input section
        input_sections = [f" {input_name} ", f" {input_student_id} ", f" {input_universities} "]
             
        matched_sections = count_matched_sections(extracted_text, input_sections)
        
        if matched_sections >= 2:
            feedback = "positive"
        else:
            feedback = "negative"
        
        # Add section on publishing date
        # Check for exact matches including spaces
        input_publish = [f" {input_publish_in} ", f" {input_publish_en} "] 

        matched_publish = count_matched_sections(extracted_text, input_publish)

        if matched_publish >= 1:
            feedback_publish = "active"
        else:
            feedback_publish = "passive"

        return jsonify({"text": extracted_text, "matched_sections": matched_sections, "feedback": feedback,
                        "matched_publish": matched_publish, "feedback_publish": feedback_publish})

def extract_text_from_pdf(pdf_bytes):
    pdf_document = fitz.open("pdf", pdf_bytes)
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def count_matched_sections(text, input_sections):
    # Convert both the input text and sections to lowercase for case-insensitive matching
    text = text.lower()
    input_sections = [section.lower() for section in input_sections]
    
    # Check for exact matches including spaces
    matched_sections = sum(1 for section in input_sections if section in text)
    return matched_sections

if __name__ == '__main__':
    app.run(debug=True)
