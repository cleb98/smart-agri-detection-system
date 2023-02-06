import requests
from datetime import datetime


API_URL_POST = "http://127.0.0.1:8000/image/add/"

MICRO_ID = 1

class postImage:
    def __init__(self, datetime, contents, species, binaryimage):
        self.datetime : str = datetime
        self.contents : str = contents
        self.species : str = species
        self.binaryimage : str = binaryimage
        self.micro_id: int = MICRO_ID


def main():
    
    datetime_obj = str(datetime.now())
    contents_obj = "safe"
    species_obj = "bee"
    binaryimage_obj = "perfieeettooo"

    post_item = postImage(datetime=datetime_obj, contents=contents_obj, species=species_obj, binaryimage=binaryimage_obj)



    response = requests.post(url=API_URL_POST, json=vars(post_item))
    print(response)


if __name__ == "__main__":
    main()



