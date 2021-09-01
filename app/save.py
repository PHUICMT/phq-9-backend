import os
import uuid
from datetime import datetime
import mysql.connector

UPLOAD_FOLDER = './app/video_storage'
video_uuid = str(uuid.uuid4())
mydb = mysql.connector.connect(
    host="db",
    user="admin",
    password="P@ssw0rd",
    database="phq_9_db"
)
cursor = mydb.cursor()

now = datetime.now()
current_time = now.strftime('%Y-%m-%d %H:%M:%S')


def save_file(file, questionnaire_id, video_type, filename):
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    sql_insert_blob_query = " INSERT INTO Videos (id, video_name, questionnaire_id, video_type_is_webcam) VALUES (%s,%s,%s,%s)"
    insert_blob_tuple = (video_uuid, filename, questionnaire_id, video_type)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    mydb.commit()
    return result


def save_questionnaire_to_database(questionnaire_id):
    sql_insert_query = " INSERT INTO Questionnaire (id, created_at) VALUES (%s,%s)"
    insert_tuple = (questionnaire_id, current_time)
    result = cursor.execute(sql_insert_query, insert_tuple)
    mydb.commit()
    return result


def save_backend_result_to_database(questionnaire_id, emotion):
    sql_insert_query = " UPDATE Result SET emotion=%s WHERE questionnaire_id=%s"
    insert_tuple = (emotion, questionnaire_id)
    result = cursor.execute(sql_insert_query, insert_tuple)
    mydb.commit()
    return result


def save_fontend_result_to_database(answer, events, questionnaire_id):
    sql_insert_query = " INSERT INTO Result (Questionnaire_id, answer, events) VALUES (%s,%s,%s)"
    insert_tuple = (questionnaire_id, answer, events)
    result = cursor.execute(sql_insert_query, insert_tuple)
    mydb.commit()
    return result