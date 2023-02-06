import streamlit as st
import requests
#import pandas as pd

# API_URL_POST = 'https://so624x.deta.dev/books/addbook/'
#finche il db non è deployato su un server si può solo fare la post in locale
#API_POST_URL = "http://127.0.0.1:8000/image/add/"

def data_dictionary(current_datetime, contents, class_value, binary_image, micro_id):
    data = {
        "datetime": current_datetime,
        "contents": contents,
        "species": class_value,
        "binaryimage": binary_image,
        "micro_id": micro_id
    }

    return data

    # campi del data_object
    # {
    # "datetime": "2023-02-02T21:41:38.739Z",
    # "contents": "string",
    # "species": "string",
    # "binaryimage": "string",
    # "micro_id": 0,
    # }  
    #  
    # myobj = data_object(id=id_input, name=name_input, description=description_input, price=float(price_input))
    # response = requests.post(url=API_URL_POST, json=vars(myobj))
