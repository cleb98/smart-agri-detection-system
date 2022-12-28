import base64
import requests
import urllib.request
import os 


# # URL dell'immagine da importare
# image_url = "https://best5.it/b5/wp-content/uploads/2019/07/ape-2-800x400.jpg"

# # Scarica l'immagine
# with urllib.request.urlopen(image_url) as url:
#     image_data = url.read()

# # Salva l'immagine in un file
# with open("image.jpg", "wb") as f:
#     f.write(image_data)

#!pip install Roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="YswyoRwpN8l4oas9n0qJ")
project = rf.workspace("iotinsectdetectionproject").project("insects-detection-hndll")
model = project.version(6).model

# infer on a local image
print(model.predict("image.jpg", confidence=40, overlap=30).json())

# visualize your prediction
model.predict("image.jpg", confidence=40, overlap=30).save("prediction.jpg")



# infer on an image hosted elsewhere
#print(model.predict("http://best5.it/b5/wp-content/uploads/2019/07/ape-2-800x400.jpg", hosted=True, confidence=40, overlap=30).json())
