  
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np

def run_predict(video_path):

    total_emotion = {
        "angry" : 0,
        "disgust" : 0,
        "scared" : 0, 
        "happy" : 0, 
        "sad" : 0, 
        "surprised" : 0, 
        "neutral" : 0
    }

    detection_model_path = './app/haarcascade_files/haarcascade_frontalface_default.xml'
    emotion_model_path = './app/haarcascade_files/_mini_XCEPTION.102-0.66.hdf5'

    face_detection = cv2.CascadeClassifier(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

    camera = cv2.VideoCapture(video_path)
    while(camera.isOpened()):
        ret, frame = camera.read()
        if ret == True:
            frame = imutils.resize(frame,width=400)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
            
            if len(faces) > 0:
                faces = sorted(faces, reverse=True,
                key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
                (fX, fY, fW, fH) = faces
                roi = gray[fY:fY + fH, fX:fX + fW]
                roi = cv2.resize(roi, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                
                preds = emotion_classifier.predict(roi)[0]
                label = EMOTIONS[preds.argmax()]
                total_emotion[label] += 1
        else :
            break

    camera.release()
    cv2.destroyAllWindows()
    return total_emotion
