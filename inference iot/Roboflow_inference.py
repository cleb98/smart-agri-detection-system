import base64
import requests
import urllib.request
import os 
from snapshot import counter
from roboflow import Roboflow
from Data_dictionary import data_dictionary
from datetime import datetime
#per portare image in jpg format
import io
from PIL import Image

API_POST_URL = 'https://djdkdw.deta.dev/image/add/'

image_folder = os.path.join(os.getcwd(), 'image')
prediction_folder = os.path.join(os.getcwd(), 'prediction')

if not os.path.exists(prediction_folder):
    print('funziona')
    os.makedirs(prediction_folder)
# Read the image from the file in the image folder
image_filename = 'image{}.jpg'.format(counter)
image_filepath = os.path.join(image_folder, image_filename)
with open(image_filepath, 'rb') as f:
    image_data = f.read()

#!pip install Roboflow
def prediction():

    global API_POST_URL
    # global micro_id 
    micro_id = 12
    global counter
    # print(counter)
    current_datetime = str(datetime.now())
    print(current_datetime)
    filename = os.path.join(image_folder, 'image{}.jpg'.format(counter))
    # print(filename)
        
    rf = Roboflow(api_key="YswyoRwpN8l4oas9n0qJ")
    project = rf.workspace("iotinsectdetectionproject").project("insects-detection-hndll")
    model = project.version(6).model

    # infer on a local image
    print(model.predict(filename, confidence=40, overlap=30).json())

    # visualize your prediction
    # generate unique filename using the counter
    prediction_filename = os.path.join(prediction_folder, 'prediction{}.jpg'.format(counter))
    model.predict(filename, confidence=40, overlap=30).save(prediction_filename)
    
    response = model.predict(filename, confidence=40, overlap=30).json()
    # #controllo per vedere se apre la predizione giusta
    # pil_image = Image.open(prediction_filename)
    # pil_image.show() # Mostra l'immagine

    predictions = response['predictions']
    
    # try:
    #     class_value = predictions[0]['class']
    # except IndexError:
    #     class_value = ''
    class_values = []
    for prediction in predictions:
        class_values.append(prediction['class'])

    class_value = ' '.join(class_values) if class_values else ''
    # print(class_value)

    if all(word in ['bee', 'ladybird', 'earwing', ''] for word in class_value.split()):
        contents = 'not dangerous'
    else: 
        contents = 'dangerous'
    # if class_value == 'bee' or class_value == 'ladybird' or class_value == 'earwing' or class_value == '':
    #     contents = 'not dangerous'
    # else: 
    #     contents = 'dangerous'

    

    
    with open(prediction_filename, 'rb') as f:
        binary_data = f.read()
        binary_image = base64.b64encode(binary_data).decode() #base64_data
        # print(binary_image)
    print(type(binary_image))
    
    # inserito controllo per vedere se l'immagine binaria salvata come stringa è effettvamente l'immagine inferenziata o no
    # si può togliere da qui
    # Decode the image string to bytes
    binary_image_bytes = base64.b64decode(binary_image)

    # Load the image from bytes
    with io.BytesIO(binary_image_bytes) as img_buffer:
        image = Image.open(img_buffer)

    # Save the image to a file on disk
    with open("image.jpg", "wb") as f:
        f.write(binary_image_bytes)
    #fino a qui
   
    data = data_dictionary(current_datetime = current_datetime , contents = contents, class_value = class_value, binary_image = binary_image , micro_id = micro_id)
    # print(data)
    response = requests.post(url='https://djdkdw.deta.dev/image/add/', json=data)
    print(response.status_code) 
    
    counter += 1  # increment the counter
   
    

# if __name__ == '__main__':
#     prediction()
