import os

UPLOAD_FOLDER = './app/temp_video'

def save_file(file):
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return True