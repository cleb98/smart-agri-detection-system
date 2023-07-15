# script for checking microcontrollers to trigger led blinking

import requests
import pandas as pd
import schedule
import time

API_URL_GET_MICROCONTROLLERS = "https://insects_api-1-q3217764.deta.app/microcontrollers/"

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
    
    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS)
    
    if micro_table is None:
        return
    
    micro_ids = micro_table.loc[micro_table["status"] == True, "id"].tolist()

    print(micro_ids)


if __name__ == "__main__":
    main()