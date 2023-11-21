# Web Application

This web app was developed to monitor agricultural pests using IoT sensor nodes and machine learning algorithms. Different pages allow users to visualize sensor data over a territory, check for pests near a location, and manage their own sensor nodes.

## Tools Used
- **[Streamlit](https://streamlit.io/)** is an open source framework for creating web applications in Python.
- It allows you to create interactive and dynamic user interfaces that can run locally or in the cloud.

## Home Page

- Dashboard showing an interactive map and list of all microcontrollers in the territory. Includes:
    - User ID
    - User name  
    - Micro ID
    - Latitude/Longitude
    - Status

- User can check the status of an area without a microcontroller (selected from map or current GPS coordinates) based on nearby microcontrollers within a 10km radius. 
- Ability to add a new user.
- Uses K-Nearest Neighbors algorithm to determine if microcontrollers nearby a reference location report pest infestations. Returns error message if infestation detected, or success if none found within 10km radius. KNN is trained on training data using Haversine distance metric to calculate distances on Earth's surface.

## User Page 

Dashboard showing an interactive map and list of microcontrollers owned by a specific user. Ability to add a microcontroller via map or current GPS, and delete owned microcontrollers. Shows slideshow of images captured by owned microcontrollers including:
- Micro ID
- Image ID
- Datetime  
- Contents
- Species

## Install Dependencies

```console
insect-detection-iot-system/web_app pip install -r requirements.txt
```

## Run

```console
insect-detection-iot-system/web_app streamlit run app.py
```

## Examples

| `Home` | `Knn` | `User` |
|:-------:|:-----------------:|:----------------------------------:|
| ![Home Example Image](/insect-detection-iot-system/web_app/assets/home.jpg) | ![Knn Example Image](/insect-detection-iot-system/web_app/assets/knn.png) | ![User Example Image](/insect-detection-iot-system/web_app/assets/user.png) |
