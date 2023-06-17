from flask import Flask, request, send_from_directory
import os
import random
import string

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    filename = file.filename
    filename_parts = filename.split('.')
    if len(filename_parts) == 1:
        extension = ''
    else:
        extension = '.' + filename_parts[-1]

    new_filename = generate_random_string(8) + extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    download_url = request.host_url + 'download/' + new_filename
    return 'File uploaded successfully. Download URL: ' + download_url

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
