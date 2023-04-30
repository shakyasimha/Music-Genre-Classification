from flask import Flask, request, render_template, request, jsonify
import librosa 
from keras.models import load_model

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)

model = load_model('models/model_cat.pkl')

## For classifying the music
@app.route('/classify_music', method=['POST'])
def classify_music():
    audio_file = request.file['audio']
    audio_data, _ = librosa.load(audio_file)
    audio_features = extract_features(audio_data)

    prediction = model.predict([audio_features])[0]
    return render_template('index.html', prediction=prediction)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)