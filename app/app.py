import json
from save import save_file, save_questionnaire_to_database, save_result_to_database
from emotion_recognition import run_predict
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload-recorded-webcam', methods=['POST'])
def upload_webcam_file():
    result = {}
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'webcam.webm'
    save_file(uploaded_file, uuid, True, filename)
    result = run_predict('./app/video_storage/'+filename)
    result_json = json.dumps(result)
    save_result_to_database(uuid,result_json)
    return jsonify({"result": result}), 200

@app.route('/upload-recorded-screen', methods=['POST'])
def upload_screen_file():
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'screen.webm'
    save_file(uploaded_file, uuid, False, filename)
    return jsonify({"response": uuid}), 200

@app.route('/questionnaire', methods=['POST'])
def upload_questionnaire():
    uuid_json = request.json
    uuid = uuid_json["uuid"]
    save_questionnaire_to_database(uuid)
    return jsonify({"response":uuid}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')