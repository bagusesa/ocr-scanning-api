from flask import Flask, request, jsonify
from OCR import convert_pdf_to_text

app = Flask(__name__)

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
    input_publish_1 = request.form.get('publish_1')
    input_publish_2 = request.form.get('publish_2')
    
    if file:
        pdf_bytes = file.read()
        extracted_text = convert_pdf_to_text(pdf_bytes)
        
        # Add spaces before and after each input section
        input_sections = [f" {input_name} ", f" {input_student_id} ", f" {input_universities} "]
             
        matched_sections = count_matched_sections(extracted_text, input_sections)
        
        if matched_sections >= 2:
            feedback = "positive"
        else:
            feedback = "negative"
        
        # Add section on publishing date
        # Check for exact matches including spaces
        input_publish = [f" {input_publish_1} ", f" {input_publish_2} "] 

        matched_publish = count_matched_sections(extracted_text, input_publish)

        if matched_publish >= 1:
            feedback_publish = "active"
        else:
            feedback_publish = "passive"

        return jsonify({"text": extracted_text, "matched_sections": matched_sections, "feedback": feedback,
                        "matched_publish": matched_publish, "feedback_publish": feedback_publish})


def count_matched_sections(text, input_sections):
    # Convert both the input text and sections to lowercase for case-insensitive matching
    text = text.lower()
    input_sections = [section.lower() for section in input_sections]
    
    # Check for exact matches including spaces
    matched_sections = sum(1 for section in input_sections if section in text)
    return matched_sections

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Listen on all available network interfaces