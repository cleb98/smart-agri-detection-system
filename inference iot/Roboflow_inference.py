import base64
import requests
import urllib.request
import os 
from snapshot import counter



# check if the 'output' folder is already created in 'inference iot' folder otherwise you're fucked up
# change the 'output folder'path related to its path in your PC
# Set the path to the output folder
output_folder = 'C:/Users/39379/Desktop/iot_project/inference iot/output'
# Read the image from the file in the output folder
image_filename = 'image{}.jpg'.format(counter)
image_filepath = os.path.join(output_folder, image_filename)
with open(image_filepath, 'rb') as f:
    image_data = f.read()

# # URL dell'immagine da importare
# image_url = "https://best5.it/b5/wp-content/uploads/2019/07/ape-2-800x400.jpg"

# # Scarica l'immagine
# with urllib.request.urlopen(image_url) as url:
#     image_data = url.read()

# # Salva l'immagine in un file
# with open("image.jpg", "wb") as f:
#     f.write(image_data)

#inizio counter=0

# do in inferenza image0 per ottenere predict0
# counter = 0  # counter for generating unique filenames
def prediction():
    global counter
    print(counter)
    filename = os.path.join(output_folder, 'image{}.jpg'.format(counter))
    print(filename)


    # def model():
    #     #!pip install Roboflow
    #     global counter
    from roboflow import Roboflow
    rf = Roboflow(api_key="YswyoRwpN8l4oas9n0qJ")
    project = rf.workspace("iotinsectdetectionproject").project("insects-detection-hndll")
    model = project.version(6).model

    # infer on a local image
    print(model.predict(filename, confidence=40, overlap=30).json())

    # visualize your prediction
    # generate unique filename using the counter
    prediction_filename = os.path.join(output_folder, 'prediction{}.jpg'.format(counter))
    model.predict(filename, confidence=40, overlap=30).save(prediction_filename)
    counter += 1  # increment the counter
    print(counter)

# if __name__ == '__main__':
#     try:
#         prediction()
#     except Exception as e:
#         print('You cannot make a prediction!', e)