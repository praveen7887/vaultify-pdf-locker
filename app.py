from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfReader, PdfWriter
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf']
    password = request.form['password']

    if file.filename == '':
        return 'No file selected.'

    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    output_filename = f"{uuid.uuid4().hex}.pdf"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    with open(output_path, "wb") as f:
        writer.write(f)

    return f'PDF protected! <a href="/download/{output_filename}">Download here</a>'

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
