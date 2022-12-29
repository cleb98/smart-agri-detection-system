import base64
import requests
import urllib.request
import os 
from snapshot import counter


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
# devo fare il loop (prendere spunto da codice bridge) 
# senno il counter viene inizializzato ogni volta a 0
# counter = 0  # counter for generating unique filenames
print(counter)
filename = 'image{}.jpg'.format(counter)
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
prediction_filename = 'prediction{}.jpg'.format(counter)
model.predict(filename, confidence=40, overlap=30).save(prediction_filename)
counter += 1  # increment the counter

