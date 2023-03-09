import numpy as np
from sklearn.neighbors import NearestNeighbors

# Creare una matrice numpy che contiene le coordinate dei punti
points = np.array([[44.6562831761065, 11.0958893898546], [44.4860137620492, 11.1248225713927], [44.5267776062036, 10.8195526677055], [44.5605345550626, 11.0072550344059]])

# Creare un modello NearestNeighbors con la distanza Euclidea come metrica
# La classe NearestNeighbors è utilizzata per trovare i vicini più vicini a un punto dato nello spazio.
# Il parametro n_neighbors specifica il numero di vicini più vicini da trovare. 
# Nel caso di questo codice, n_neighbors è impostato su 2, il che significa che verranno trovati i 2 vicini più vicini.
# Il parametro metric specifica la metrica da utilizzare per calcolare la distanza tra i punti. Nel caso di questo codice, la metrica "euclidean" viene utilizzata, che rappresenta la distanza euclidea standard.
neigh = NearestNeighbors(n_neighbors=2, metric='euclidean')

# Fit il modello con la matrice di punti
neigh.fit(points)

# Chiedere all'utente di inserire le coordinate del punto
new_point = np.array([float(input("Enter x coordinate: ")), float(input("Enter y coordinate: "))]).reshape(1, -1)

# Trova i nearest neighbor per il nuovo punto
distances, indices = neigh.kneighbors(new_point)

# Prendi la distanza al nearest neighbor
distance = distances[0][1]

# Verifica se la distanza è inferiore a 800 metri
if distance < 800:
    # Stampare la distanza e l'indice del nearest neighbor
    print("The new point has nearest neighbor at index", indices[0][1], "with distance", distance, "meters")
else:
    print("No nearest neighbor was found within 800 meters.")

# # Trova i nearest neighbor per ogni punto
# distances, indices = neigh.kneighbors(points)
# Loop attraverso ogni punto e i suoi nearest neighbor
# for i, index in enumerate(indices):
#     # Prendi la distanza al nearest neighbor
#     distance = distances[i][1]
    
#     # Verifica se la distanza è inferiore a 800 metri
#     if distance < 800:
#         # Stampare la distanza e l'indice del nearest neighbor
#         print("Point", i, "has nearest neighbor at index", index[1], "with distance", distance, "meters")

