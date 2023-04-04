import numpy as np
from sklearn.neighbors import NearestNeighbors
from math import radians, sin, cos, sqrt, atan2

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


# Define binary classes for each point
binary_classes = np.array([0, 1])

# Creare una matrice numpy che contiene le coordinate dei punti in formato [latitudine, longitudine] (casa modena, Gubbio)
points = np.array([[44.63233671612906, 10.93369970312806],[43.35566843537755, 12.42751296772821]])

# Creare un modello NearestNeighbors con la funzione haversine come metrica
neigh = NearestNeighbors(n_neighbors=2, metric=haversine)

# Fit il modello con la matrice di punti e le rispettive classi binarie
neigh.fit(points, binary_classes)

# Chiedere all'utente di inserire le coordinate del punto
new_point = np.array([float(input("Enter latitude: ")), float(input("Enter longitude: "))]).reshape(1, -1)

# Trova i nearest neighbor per il nuovo punto
distances, indices = neigh.kneighbors(new_point)

# Get indices that would sort distances in ascending order
sorted_indices = np.argsort(distances)

# Reorder distances and indices arrays based on sorted indices
distances = distances[0][sorted_indices[0]]
indices = indices[0][sorted_indices[0]]

# Get binary classes for nearest neighbors
binary_classes = neigh.classes_[indices]

# Print distances, indices, and binary classes in order
print("Distances to nearest neighbors:")
for d, i, c in zip(distances, indices, binary_classes):
    print(f"Distance: {d}, Index: {i}, Class: {c}")
