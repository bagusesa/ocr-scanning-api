# OCR-based Text Matching API

This Flask API allows you to extract text from PDF files and perform text matching operations. It's useful for scenarios where you need to find specific text sections within a PDF document.

## Usage

To use this API, send a POST request to the `/scan_pdf` endpoint with a PDF file and input text parameters. The API will extract text from the PDF and match it against the provided input. You can check if the API finds at least two out of three input sections ("name," "student id," and "universities") for a positive feedback. Additionally, you can provide "month" and "year of publication" for a separate score.

### Endpoint
- `/scan_pdf`

### Input Parameters
- `file`: PDF file to process
- `name`: Name to match
- `student_id`: Student ID to match
- `university`: University name to match
- `publish_1`: Month and Year to match the student active status
- `publish_2`: Month and Year to match if the deadline is at the beginning of the month (optional)

### Example Request
```http
POST /scan_pdf
Content-Type: multipart/form-data

file: [PDF File]
name: John Doe
student_id: 12345
university: Example University
publish_1: Agustus 2023
publish_2: September 2023
```

### Example Response
```json
{
  "text": "Extracted text from the PDF...",
  "matched_sections": 2,
  "feedback": "positive",
  "matched_publish": 1,
  "feedback_publish": "active"
}
```
### Testing with Postman

Provide instructions for users on how to test your API using Postman. You can outline the steps they should follow and include any necessary screenshots or examples. Here's a section you can include:

#### Testing with Postman

1. Download and install [Postman](https://www.postman.com/), if you haven't already.

2. Launch Postman and create a new request.

3. Set the request type to `POST` and enter the API endpoint URL: `http://your-api-host/scan_pdf`.

4. In the request body, use the `form-data` option to add the following parameters:
   - `file`: Select a PDF file to upload.
   - `name`: Provide a name to match.
   - `student_id`: Enter a student ID to match.
   - `university`: Specify a university name to match.
   - `publish_1`: Month and Year to match the student active status
   - `publish_2`: Month and Year to match if the deadline is at the beginning of the month (optional)

5. Click the "Send" button to make the request.

6. Review the response from the API, which will include the extracted text, matched sections, feedback, matched publishing date, and feedback for the publishing date.

## Installation

1. Install Python > 3.8.
2. Clone this repository.
3. Install the required dependencies using `pip install -r requirements.txt`.

## Running the API

Run the API locally using:
```bash
python app.py
```
