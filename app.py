from flask import Flask, request, render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os 


ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'static/uploads'

# Defining the app  here
app = Flask(__name__)

# Secret key of the app
app.config['SECRET_KEY'] = '2a87446caff77077bd5d58f144784a87'


# For storing file attributes in a dictionary
def file_attrib(file):
    attrib_dict = {
        'fname': file.filename,
        'ftype': file.content_type,
        'fsize': file.content_length
    }

    return attrib_dict


# For checking allowed file extension
def allowed_extension(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 


# Route for using POST request to upload the file
@app.route('/upload_file', methods=['POST'])
def upload_file():
    # Checks if the post request has the file part
    if 'file' not in request.files:
        flash('No file found')
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']

    # Returns empty file without a filename if a file is not uploaded
    if file.filename == '':
        flash('No selected file')
        return jsonify({'error': 'No file selected'})
    
    if file and allowed_extension(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        attrib = file_attrib(file)
        
        return render_template('result.html', attrib=attrib)
    
    return jsonify({'error': 'Invalid file format'})



@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)