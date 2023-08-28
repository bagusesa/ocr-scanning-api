from flask import Flask, jsonify, request, json
import easyocr


app = Flask(__name__)
reader = easyocr.Reader(['en'])  # Initialize the OCR reader with desired languages

@app.route('/scan_pdf', methods=['POST'])
def scan_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        text = extract_text_from_pdf(file)
        return jsonify({"text": text})

def extract_text_from_pdf(pdf_file):
    # Use EasyOCR to extract text from PDF file
    image = pdf_file.read()
    results = reader.readtext(image)
    extracted_text = ' '.join([result[1] for result in results])
    return extracted_text

if __name__ == '__main__':
    app.run(debug=True)