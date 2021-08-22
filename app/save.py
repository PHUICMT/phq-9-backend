import os
import uuid
from datetime import datetime
import mysql.connector

UPLOAD_FOLDER = './app/temp_video'
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

def save_file(file,questionnaire_id,video_type):
    file_name = "["+uuid+"]"+file.filename
    file.save(os.path.join(UPLOAD_FOLDER, file_name))    

    sql_insert_blob_query = " INSERT INTO videos (id, questionnaire_id, video_name, video_type, file) VALUES (%s,%s,%s,%s,%s)"
    insert_blob_tuple = (video_uuid, questionnaire_id, file_name, video_type, file)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    mydb.commit()
    return result

def save_questionnaire_to_database(questionnaire_id):
    sql_insert_query = " INSERT INTO questionnaire (id, created_at) VALUES (%s,%s)"
    insert_tuple = (questionnaire_id, current_time)
    result = cursor.execute(sql_insert_query, insert_tuple)
    mydb.commit()
    return result

def save_result_to_database(questionnaire_id,emotion):
    sql_insert_query = " INSERT INTO result (questionnaire_id, emotion) VALUES (%s,%s)"
    insert_tuple = (questionnaire_id, emotion)
    result = cursor.execute(sql_insert_query, insert_tuple)
    mydb.commit()
    return result