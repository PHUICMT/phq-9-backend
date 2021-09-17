import json
from save import save_image, save_video, save_questionnaire_to_database, save_backend_result_to_database, save_fontend_result_to_database, questionnaire_count
from emotion_recognition import run_predict
from mail_sender import send_email
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
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'webcam.webm'

    save_video(uploaded_file, uuid, True, filename)

    total_emotion, total_emotion_time, start_end_time = run_predict(
        './app/video_storage/'+filename)
    predictions_result = json.dumps(total_emotion)
    save_backend_result_to_database(uuid, predictions_result)
    return jsonify({"total_emotion": total_emotion, "total_emotion_time": total_emotion_time, "start_end_time": start_end_time}), 200


@app.route('/upload-recorded-screen', methods=['POST'])
def upload_screen_file():
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'screen.webm'

    save_video(uploaded_file, uuid, False, filename)
    return jsonify({"response screen": uuid}), 200


@app.route('/questionnaire', methods=['POST'])
def upload_questionnaire():
    uuid_json = request.json
    uuid = uuid_json["uuid"]

    save_questionnaire_to_database(uuid)
    questionnaire_row = questionnaire_count()
    return jsonify({"questionnaire": questionnaire_row}), 200


@app.route('/upload-image', methods=['POST'])
def upload_image():
    uuid = request.form.get("uuid", False)
    result_image = request.files['result_image']

    filename = uuid + '.png'
    save_image(result_image, filename)

    return jsonify({"image_saved": filename, "uuid": uuid}), 200


@app.route('/send-mail', methods=['POST'])
def send_mail():
    uuid = request.json['uuid']
    to_mail = request.json['to_email']

    filename = uuid + '.png'
    send_email(filename, to_mail)

    return jsonify({"image": filename, "uuid": uuid, "to_email": to_mail}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
