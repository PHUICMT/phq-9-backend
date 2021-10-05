import json
import requests

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
    save_video_result = save_video(uploaded_file, uuid, True, filename)
    return jsonify({"save_video": save_video_result})


@app.route('/upload-recorded-screen', methods=['POST'])
def upload_screen_file():
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'screen.webm'

    save_video(uploaded_file, uuid, False, filename)
    return jsonify({"response screen": uuid}), 200


@app.route('/select-to-process', methods=['POST'])
def select_to_process():
    requests.post('http://mailsender:5001/node-select-to-process',
                  json=request.get_json())
    return jsonify({"response": "Sended to node-select-to-process"}), 200


@app.route('/process-video', methods=['POST'])
async def process_webcam():
    uuid = request.json['uuid']
    filename = "["+uuid+"]"+'webcam.webm'
    total_emotion, total_emotion_time, start_end_time = await run_predict(
        './app/video_storage/'+filename)
    predictions_result = json.dumps(total_emotion)
    save_backend_result_to_database(uuid, predictions_result)
    return jsonify({"total_emotion": total_emotion, "total_emotion_time": total_emotion_time, "start_end_time": start_end_time}), 200


@app.route('/questionnaire', methods=['POST'])
def upload_questionnaire():
    uuid_json = request.json
    uuid = uuid_json["uuid"]

    save_questionnaire_to_database(uuid)
    questionnaire_row = questionnaire_count()
    return jsonify({"questionnaire": questionnaire_row}), 200


@app.route('/send-mail', methods=['POST'])
def send_mail():
    uuid = request.json['uuid']
    to_mail = request.json['to_email']
    stringEmote = request.json['stringEmote']
    stringClickTime = request.json['stringClickTime']
    stringReactionTime = request.json['stringReactionTime']
    stringBehavior = request.json['stringBehavior']
    setingGroupsTest = request.json['setingGroupsTest']

    result = jsonify({
        "uuid": uuid,
        "stringEmote": stringEmote,
        "stringClickTime": stringClickTime,
        "stringReactionTime": stringReactionTime,
        "stringBehavior": stringBehavior,
        "setingGroupsTest": setingGroupsTest
    })

    send_email(result, to_mail)

    return jsonify({"uuid": uuid, "to_email": to_mail}), 200

# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     uuid = request.form.get("uuid", False)
#     result_image = request.files['result_image']

#     filename = uuid + '.png'
#     save_image(result_image, filename)

#     return jsonify({"image_saved": filename, "uuid": uuid}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
