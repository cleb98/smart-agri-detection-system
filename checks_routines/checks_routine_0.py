import requests
import pandas as pd


API_URL_GET_IMAGES_UNCHECKED = "https://djdkdw.deta.dev/images/checked/"
API_URL_PATCH_IMAGE_BY_ID = "https://djdkdw.deta.dev/images/update_checked/{}"
API_URL_PATCH_MICROCONTROLLER_BY_ID = "https://djdkdw.deta.dev/microcontroller/update_status/{}"

def ritrieve_table(url):
    response = requests.get(url=url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
            return df
        elif isinstance(data, list):
            df = pd.DataFrame(data)
            return df
    return None

def main():
    
    images_table = ritrieve_table(API_URL_GET_IMAGES_UNCHECKED)

    images_ids = images_table['id'].tolist()

    micro_ids = images_table.loc[images_table["contents"] == "dangerous", "micro_id"].unique().tolist()

    patch_micro_data = {
        "status": True 
    }

    patch_image_data = {
        "checked": True
    }

    for micro_item in micro_ids:
        response_0 = requests.patch(url=API_URL_PATCH_MICROCONTROLLER_BY_ID.format(micro_item), json=patch_micro_data)
    
    if response_0.status_code == 200:
        print("status dei microcontrollori cambiati!")
    else:
        print("errore, nessun microcontrollore da cambiare!")

    for image_item in images_ids:
        response_1 = requests.patch(url=API_URL_PATCH_IMAGE_BY_ID.format(image_item), json=patch_image_data)

    if response_1.status_code == 200:
        print("campo checked delle immagini cambiato!")
    else:
        print("errore, nessuna immagine da cmabiare!")
        

    

if __name__ == "__main__":
    main()

