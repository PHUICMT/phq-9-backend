import json
from save import save_file, save_questionnaire_to_database, save_result_to_database
from emotion_recognition import run_predict
from flask import Flask, request, redirect, url_for, make_response ,jsonify

app = Flask(__name__)

@app.route('/upload-recorded-webcam', methods=['POST'])
def upload_webcam_file():
    result = {}
    uploaded_file = request.files['blob']
    uuid = request.files['uuid']
    if uploaded_file.filename != '':
        uploaded_file.filename = 'webcam.webm'
        save_file(uploaded_file, uuid, True)
        result = run_predict('./app/temp_video/webcam.webm')
        result_json = json.dumps(result)
        save_result_to_database(uuid,result_json)
    return jsonify({"response":result}), 200

@app.route('/upload-recorded-screen', methods=['POST'])
def upload_screen_file():
    uploaded_file = request.files['blob']
    uuid = request.files['uuid']
    if uploaded_file.filename != '':
        uploaded_file.filename = 'screen.webm'
        save_file(uploaded_file, uuid, False)
    return jsonify({"response":"Screen record saved!"}), 200

@app.route('/questionnaire', methods=['POST'])
def upload_questionnaire():
    uuid = request.files['uuid']
    result_save_file = save_questionnaire_to_database(uuid)
    return jsonify({"response":result_save_file}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')