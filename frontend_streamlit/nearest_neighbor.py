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
# def knn(points, binary_classes, new_point):
    # Define binary classes for each point
binary_classes = np.array([0, 1, 1, 0])
# binary_classes = binary_classes


# Create a numpy array that contains the coordinates of the points in the format [latitude, longitude]
points = np.array([[44.63233671612906, 10.93369970312806], [43.35566843537755, 12.42751296772821], [43.35566843537755, 13.42751296772821], [44.35566843537755, 11.42751296772821]])
# points = points
# Create a NearestNeighbors model with the haversine distance metric
neigh = NearestNeighbors(n_neighbors = len(points), metric=haversine)

# Fit the model with the points and their corresponding binary classes
neigh.fit(points, binary_classes)

# Ask the user to input the coordinates of the new point
new_point = np.array([float(input("Enter latitude: ")), float(input("Enter longitude: "))])
# print(new_point, new_point.shape)
new_point = new_point.reshape(1, -1)
# print(new_point, new_point.shape)
# Find the nearest neighbors for the new point
distances, indices = neigh.kneighbors(new_point, return_distance=True)


# Get the distances, indices, and binary classes of the nearest neighbors
distances = distances[0]
indices = indices[0]
binary_classes = binary_classes[indices]

# Print the distances, indices, and binary classes of the nearest neighbors
print("Distances to nearest neighbors:")
for d, i, c in zip(distances, indices, binary_classes):
    print(f"Distance: {d}, Class: {c}")
