from save_file import save_file
from emotion_recognition import run_predict
from flask import Flask, request, redirect, url_for, make_response ,jsonify

app = Flask(__name__)

@app.route('/upload-recorded-webcam', methods=['POST'])
def upload_webcam_file():
    result = {}
    uploaded_file = request.files['blob']
    if uploaded_file.filename != '':
        uploaded_file.filename = 'webcam.webm'
        save_file(uploaded_file)
        result = run_predict('./app/temp_video/webcam.webm')
    return jsonify({"response":result}), 200

@app.route('/upload-recorded-screen', methods=['POST'])
def upload_screen_file():
    uploaded_file = request.files['blob']
    if uploaded_file.filename != '':
        uploaded_file.filename = 'screen.webm'
        save_file(uploaded_file)
    return 'Screen accepted'

@app.route('/check', methods=['GET', 'POST'])
def check_flask():
    return 'Flask is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0')