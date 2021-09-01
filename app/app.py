import json
from save import save_file, save_questionnaire_to_database, save_backend_result_to_database, save_fontend_result_to_database
from emotion_recognition import run_predict
from flask import Flask, request, jsonify

app = Flask(__name__)

global predictions_result


@app.route('/result', methods=['POST'])
def get_result():
    uuid = request.json['uuid']
    answer = json.dumps(request.json['answer'])
    event = request.json['event']

    save_fontend_result_to_database(answer, event, uuid)
    return jsonify({"answer": answer, "uuid": uuid, "event": event}), 200


@app.route('/upload-recorded-webcam', methods=['POST'])
def upload_webcam_file():
    result = {}
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'webcam.webm'

    save_file(uploaded_file, uuid, True, filename)

    total_emotion, total_emotion_time = run_predict('./app/video_storage/'+filename)
    predictions_result = json.dumps(total_emotion)
    save_backend_result_to_database(uuid, predictions_result)
    return jsonify({"total_emotion": total_emotion, "total_emotion_time": total_emotion_time}), 200


@app.route('/upload-recorded-screen', methods=['POST'])
def upload_screen_file():
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'screen.webm'

    save_file(uploaded_file, uuid, False, filename)
    return jsonify({"response screen": uuid}), 200


@app.route('/questionnaire', methods=['POST'])
def upload_questionnaire():
    uuid_json = request.json
    uuid = uuid_json["uuid"]

    save_questionnaire_to_database(uuid)
    return jsonify({"response questionnaire": uuid}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
