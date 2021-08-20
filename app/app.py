from save_file import save_file
from emotion_recognition import run_predict
from flask import Flask, request, redirect, url_for, make_response ,jsonify

app = Flask(__name__)

@app.route('/upload-recorded-<type>', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        save_file(uploaded_file)
        run_predict('./app/temp/' + type + '.webm')
    return 'accepted :' + type + '.webm'

@app.route('/check', methods=['GET', 'POST'])
def check_flask():
    return 'Flask is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0')