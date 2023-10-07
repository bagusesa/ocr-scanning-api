from flask import Flask, request, jsonify
from ocr_app.pdf_utils import convert_pdf_to_text, count_matched_sections
from ocr_app.config import get_indonesian_month
import datetime

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
    
    # Get the current month and year in Bahasa Indonesia
    current_date = datetime.datetime.now()
    current_month = get_indonesian_month(current_date.strftime("%B"))
    current_year = current_date.strftime("%Y")
    
    # Get the previous month and year in Bahasa Indonesia
    previous_date = current_date - datetime.timedelta(days=current_date.day)
    previous_month = get_indonesian_month(previous_date.strftime("%B"))
    previous_year = previous_date.strftime("%Y")
    
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
        
        # Add sections for the current month and the previous month
        input_publish_1 = f" {current_month} {current_year}"
        input_publish_2 = f" {previous_month} {previous_year}"
        input_publish = [input_publish_1, input_publish_2]

        matched_publish = count_matched_sections(extracted_text, input_publish)

        if matched_publish >= 1:
            feedback_publish = "active"
        else:
            feedback_publish = "passive"

        return jsonify({"text": extracted_text, "matched_sections": matched_sections, "feedback": feedback,
                        "matched_publish": matched_publish, "feedback_publish": feedback_publish})

if __name__ == '__main__':
    app.debug=False
    app.run(host='0.0.0.0', port=5000)  # Listen on all available network interfaces
