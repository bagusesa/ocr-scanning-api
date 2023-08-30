from flask import Flask, request, jsonify
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['id'])

@app.route('/scan_pdf', methods=['POST'])
def scan_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
   
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
   
    input_name = request.form.get('name')
    input_student_id = request.form.get('student_id')
    input_university = request.form.get('university')
    
    if file:
        extracted_text = extract_text_from_pdf(file)
        
        input_sections = [input_name, input_student_id, input_university]
        input_sections = [section for section in input_sections if section is not None]
        
        matched_sections = count_matched_sections(extracted_text, input_sections)
        
        if matched_sections >= 2:
            feedback = "positive"
        else:
            feedback = "negative"
            
        return jsonify({"text": extracted_text, "matched_sections": matched_sections, "feedback": feedback})

def extract_text_from_pdf(pdf_file):
    image = pdf_file.read()
    results = reader.readtext(image)
    extracted_text = ' '.join([result[1] for result in results])
    return extracted_text

def count_matched_sections(text, input_sections):
    matched_sections = sum(1 for section in input_sections if section.lower() in text.lower())
    return matched_sections

if __name__ == '__main__':
    app.run(debug=True)
