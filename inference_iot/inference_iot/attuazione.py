import numpy as np
from sklearn.neighbors import NearestNeighbors
from math import radians, sin, cos, sqrt, atan2
import requests 
import pandas as pd
# from inference_iot.Roboflow_inference import micro_id


def haversine(point1, point2):
    # Convertire i punti in radianti
    lat1, lon1 = radians(point1[0]), radians(point1[1])
    lat2, lon2 = radians(point2[0]), radians(point2[1])

    # Calcolare la distanza tra i punti
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Ritornare la distanza in metri
    return c * 6371 * 1000

#trasforma in pandas dataframe la tabella corrispondente all'url
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

API_URL_GET_MICROCONTROLLERS = "https://djdkdw.deta.dev/microcontrollers/"
micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS)
# print(micro_table)

#usato per inserire qualche status su True per testare l'algoritmo
micro_table.loc[micro_table['id'] == 6, 'status'] = True
micro_table.loc[micro_table['id'] == 12, 'status'] = False
micro_table.loc[micro_table['id'] == 7, 'status'] = False
micro_table.loc[micro_table['id'] == 9, 'status'] = False
micro_table.loc[micro_table['id'] == 17, 'status'] = False
print(micro_table)





#controllo per ogni mic (della tab microcontroller) se entro 800 metri c'è mic infestato
#se c'è su quel microcontrollore blinkera il led

# Create a binary array for the infested mic status
infested = np.array([True if s else False for s in micro_table['status']])
print(infested)
# Create a numpy array that contains the coordinates of the mic in the format [latitude, longitude]
mic_coords = np.array(micro_table[['lat', 'long']])
print(mic_coords)
# Create a NearestNeighbors model with the haversine distance metric
neigh = NearestNeighbors(n_neighbors=len(mic_coords), metric=haversine)

# Fit the model with the mic coordinates and their corresponding infested status
neigh.fit(mic_coords, infested)

#initiliaze list for possible infested mic
risk_mic_id = []
# Loop through the ids in the micro_table DataFrame
for mic_id in micro_table['id']:
    # Get the coordinates of the mic with the current id
    mic_coord = mic_coords[micro_table['id'] == mic_id][0]

    # Create a numpy array with the current mic coordinate
    mic_coord_arr = mic_coord.reshape(1, -1)

    # Find the nearest neighbors for the current mic coordinate
    distances, indices = neigh.kneighbors(mic_coord_arr, return_distance=True)

    # Get the indices and infested status of the nearest neighbors
    indices = indices[0]
    infested_status = infested[indices]
    safety_zone = 5000

    if np.any(infested_status) and distances[0][infested_status] <= safety_zone:
        # Find the infested mic(s) within 800 meters of the current mic
        infested_mics = mic_coords[indices][infested_status]
        
        # Calculate the distances from the current mic to the infested mic(s)
        distances_from_infested_mics = [haversine(mic_coord, infested_mic) for infested_mic in infested_mics]
        
        #possible_infested_mic_id = array di interi con i mic_id che passano il controllo
        risk_mic_id.append(mic_id)

        # Print the mic id and the distances from the infested mic(s)
        print(f"Mic with id {mic_id} has an infested mic within {safety_zone} meters! Distances: {distances_from_infested_mics}")
        
    else:
        print(f"Mic with id {mic_id} has not an infested mic within {safety_zone} meters!")

print("all possible new infested mic: ", risk_mic_id)       

# capire come importare micro 
# vedere se fra gli id ce nè uno uguale a micro_id 
# se c'è:
# inviare tramite seriale il segnale per far blinkare il micro collegato con la seriale
