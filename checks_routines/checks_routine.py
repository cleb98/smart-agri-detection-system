# script for periodic microcontroller status check based on detected images

import requests
import pandas as pd
import schedule
import time
import urllib3

urllib3.disable_warnings()

API_URL_GET_IMAGES_UNCHECKED = "https://insects_api-1-q3217764.deta.app/images/checked/"
API_URL_PATCH_IMAGE_BY_ID = "https://insects_api-1-q3217764.deta.app/images/update_checked/{}"
API_URL_PATCH_MICROCONTROLLER_BY_ID = "https://insects_api-1-q3217764.deta.app/microcontroller/update_status/{}"

def ritrieve_table(url):
    response = requests.get(url=url, verify = False)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
            return df
        elif isinstance(data, list):
            df = pd.DataFrame(data)
            return df
    return None

def check():
    
    print("I'm working...")

    images_table = ritrieve_table(API_URL_GET_IMAGES_UNCHECKED)

    if images_table is None:
        return

    images_ids = images_table['id'].tolist()

    micro_ids = images_table.loc[images_table["contents"] == "dangerous", "micro_id"].unique().tolist()

    print("micro_ids: ", micro_ids)

    if not micro_ids:
        print("No dangerous images found!")
        return

    patch_micro_data = {
        "status": True 
    }

    patch_image_data = {
        "checked": True
    }

    for micro_item in micro_ids:
        response_0 = requests.patch(url=API_URL_PATCH_MICROCONTROLLER_BY_ID.format(micro_item), json=patch_micro_data, verify = False)
    print(response_0.status_code)
    if response_0.status_code == 200:
        print("status dei microcontrollori cambiati!")
    else:
        print("errore, nessun microcontrollore da cambiare!")

    for image_item in images_ids:
        response_1 = requests.patch(url=API_URL_PATCH_IMAGE_BY_ID.format(image_item), json=patch_image_data, verify = False)
    if response_1.status_code == 200:
        print("campo checked delle immagini cambiato!")
    else:
        print("errore, nessuna immagine da camabiare!")

     # ottengo lista di microcontrollori con status = True


def main():


    schedule.every(1).minutes.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

