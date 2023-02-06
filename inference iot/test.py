
import requests

import os 



from datetime import datetime


API_POST_URL = "http://127.0.0.1:8000/image/add/"



data = {
  "datetime": "2023-02-06T18:09:09.174Z",
  "contents": "string",
  "species": "string",
  "binaryimage": "string",
  "micro_id": 2
}

response = requests.post(url=API_POST_URL, json=data)

print(response)