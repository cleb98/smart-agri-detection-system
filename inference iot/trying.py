import requests 
import base64  
from Data_dictionary import data_dictionary
import os 
#per portare image in jpg format
import io
from PIL import Image
import json
import streamlit as st

prediction_folder = os.path.join(os.getcwd(), 'prediction')
prediction_filename = os.path.join(prediction_folder, 'prediction0.jpg')

with open(prediction_filename, 'rb') as f:
    binary_data = f.read()
    binary_image = base64.b64encode(binary_data).decode() #base64_data
type(binary_image)
# Decode the image string to bytes
binary_image_bytes = base64.b64decode(binary_image)

# Load the image from bytes
with io.BytesIO(binary_image_bytes) as img_buffer:
    image = Image.open(img_buffer)

# Save the image to a file on disk
with open("image.jpg", "wb") as f:
    f.write(binary_image_bytes)

current_datetime = '2023-03-16 17:28:42.221093'
contents = 'dangerous'
class_value = 'bee'

micro_id = 6
data = data_dictionary(current_datetime=current_datetime, contents=contents, class_value=class_value, binary_image=binary_image, micro_id=micro_id)

response = requests.post(url='https://djdkdw.deta.dev/image/add/', json=data)
print(response.status_code)
