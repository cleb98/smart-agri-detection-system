import requests
import pandas as pd


API_URL_GET_IMAGES = "https://djdkdw.deta.dev/images/"
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
    
    images_table = ritrieve_table(API_URL_GET_IMAGES)

    micro_ids = images_table.loc[images_table["contents"] == "dangerous", "micro_id"].unique().tolist()

    patch_micro_data = {
        "status": True 
    }

    
    for id_item in micro_ids:
        response = requests.patch(url=API_URL_PATCH_MICROCONTROLLER_BY_ID.format(id_item), json=patch_micro_data)
    
    if response.status_code == 200:
        print("status dei microcontrollori cambiati!")
    else:
        print("errore")





if __name__ == "__main__":
    main()

