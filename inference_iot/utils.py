import os
import cv2
import base64
import requests
from datetime import datetime

from roboflow import Roboflow

rf = Roboflow(api_key="YswyoRwpN8l4oas9n0qJ")
project = rf.workspace("iotinsectdetectionproject").project("insects-detection-hndll")
model = project.version(6).model

MICRO_ID = 14

API_POST_IMAGE_URL = 'https://insects_api-1-q3217764.deta.app/image/add/'


def take_photo():
    """
    takes a photo and places it in the output folder
    """
    cap = cv2.VideoCapture(0) # set the camera index. '0' is for default camera 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # tune
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # tune
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('images/image.jpg', frame) # jpg/png

    cap.release()

def prediction():
    """
    makes a prediction
    """
    image_filename = 'images/image.jpg'

    inference_responce = model.predict(image_filename, confidence=40, overlap=30).json()

    prediction_filename = 'predictions/prediction.jpg'

    model.predict(image_filename, confidence=40, overlap=30).save(prediction_filename)

    predictions = inference_responce['predictions']

    class_values = []

    for prediction in predictions:
        class_values.append(prediction['class'])

    class_value = ' '.join(class_values) if class_values else ''

    if all(word in ['bee', 'ladybird', 'earwing', ''] for word in class_value.split()):
        contents = 'not dangerous'
    else:
        contents = 'dangerous'

    with open(prediction_filename, 'rb') as f:
        binary_data = f.read()
        binary_image = base64.b64encode(binary_data).decode() #base64_data

    prediction_data = {
        "datetime": str(datetime.now()),
        "contents": contents,
        "species": class_value,
        "binaryimage": binary_image,
        "micro_id": MICRO_ID
    }

    return prediction_data

def send_prediction(data):
    """
    sends the prediction to the server
    """
    response = requests.post(API_POST_IMAGE_URL, json=data)

    return response.status_code

def empty_folders():
    """
    empties the images and predictions folders
    """

    for filename in os.listdir("images"):
        file_path = os.path.join("images", filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Errore durante l'eliminazione del file {file_path}: {e}")

    for filename in os.listdir("predictions"):
        file_path = os.path.join("predictions", filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Errore durante l'eliminazione del file {file_path}: {e}")

    
        
if __name__ == "__main__":
    take_photo()
    data = prediction()
    response = send_prediction(data)
    print(response)
    empty_folders()