import base64
import requests
import urllib.request
import os 
from snapshot import counter
from roboflow import Roboflow
from Data_dictionary import data_dictionary
from datetime import datetime
# from bridge import micro_id

API_POST_URL = "http://djdkdw.deta.dev/image/add/"

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
    micro_id = 1
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
    # datetime = datetime.now()
    # print(datetime)
    predictions = response['predictions']
    class_value = predictions[0]['class']
    
    if class_value == 'bee' or class_value == 'ladybird' or class_value == 'earwing' or class_value == '':
        contents = 'not dangerous'
    else: 
        contents = 'dangerous'

    with open(prediction_filename, 'rb') as f:
        binary_data = base64.b64encode(f.read())
    
    binary_image = binary_data.decode()
   
    data = data_dictionary(current_datetime = current_datetime , contents = contents, class_value = class_value, binary_image = binary_image , micro_id = micro_id)
    response = requests.post(url = API_POST_URL, json = data)
    print(response.status_code)
    
    counter += 1  # increment the counter
   
    

# if __name__ == '__main__':
#     try:
#         prediction()
#     except Exception as e:
#         print('You cannot make a prediction!', e)