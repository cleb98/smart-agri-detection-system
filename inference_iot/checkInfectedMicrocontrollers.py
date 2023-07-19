# script for checking microcontrollers to trigger led blinking

import requests
import pandas as pd
import schedule
import time

API_URL_GET_MICROCONTROLLERS = "https://insects_api-1-q3217764.deta.app/microcontrollers/"
#imposta micro_ids come variabile globale
micro_ids = []

def ritrieve_table(url):
    response = requests.get(url=url, verify = False)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
            return df
        elif isinstance(data, list):
            df = pd.DataFrame(data)
            return df
    return None


def getInfectedList():
    
    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS)
    print(micro_table)
    
    if micro_table is None:
        return 
    
    micro_ids = micro_table.loc[micro_table["status"] == True, "id"].tolist()

    return micro_ids

    # invia richiesta di accensione led a microcontrollori con status = True tramite seriale 

  




# if __name__ == "__main__":
#     main()