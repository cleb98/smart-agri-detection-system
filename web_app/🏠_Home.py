import streamlit as st
import streamlit_js_eval as st_js
import requests
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import folium
import streamlit_folium as st_folium
from math import radians, sin, cos, sqrt, atan2


API_URL_GET_USERS = "https://insects_api-1-q3217764.deta.app/users/"
API_URL_GET_MICROCONTROLLERS = "https://insects_api-1-q3217764.deta.app/microcontrollers/"
API_URL_GET_IMAGES = "https://insects_api-1-q3217764.deta.app/images/"
API_URL_ADD_USER = "https://insects_api-1-q3217764.deta.app/user/add/"

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


def Knn(dataframe, lat, long):
    
    dataframe["status"] = dataframe["status"].replace({"safe": False, "infested": True})

    points = []
    labels = []

    new_point = np.array([lat, long])
    new_point = new_point.reshape(1,-1)

    for index, row in dataframe.iterrows():
        points.append([row["lat"], row["long"]])
        labels.append([row["status"]])

    np_points = np.array(points)
    np_labels = np.array(labels)

    neigh = NearestNeighbors(n_neighbors=len(points), metric=haversine)

    neigh.fit(np_points, np_labels)

    distances, indices = neigh.kneighbors(new_point, return_distance=True)

    # Get the distances, indices, labels
    distances = distances[0]
    indices = indices[0]
    np_labels = np_labels[indices]


    if np.all(distances > 10000):
        st.error("Distance from the first microcontroller greater than 10 km!", icon='🚨')
        return

    for d, i, c in zip(distances, indices, np_labels):

        if d < 10000 and c == True:
            st.error("Microcontrollers in the area detected infestations!", icon='🚨')
            return
        elif d < 10000 and c == False:
            st.success('Microcontrollers in the area do not detect infestations!', icon="✅")
            return
        

def main():

    st.set_page_config(
        page_title="Insect Detection",
        page_icon="🪳",
    )

    st.markdown("<h1 style='text-align: center;'>🪲 Insect Detection 🪲</h1>", unsafe_allow_html=True)

    # ritrieve users table
    user_table = ritrieve_table(API_URL_GET_USERS)

    # ritrieve microcontrollers table
    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS)
    micro_table = micro_table.rename(columns={"id":"micro_id", "user_id":"id"})

    # merge tables
    home_table = pd.merge(user_table, micro_table, on='id')

    # drop columns
    home_table = home_table.drop(labels=["email", "microcontrollers", "images", "chat_id"], axis=1)

    # rename colums
    home_table = home_table.rename(columns={"id":"user_id"})

    # replace values in status columns
    home_table["status"] = home_table["status"].replace({False: "safe", True: "infested"})

    st.dataframe(home_table, use_container_width=True)


    # create map
    st.markdown("<h2 style='text-align: center;'> Map </h1>", unsafe_allow_html=True)

    map_1 = folium.Map(location=[home_table["lat"].mean(), home_table["long"].mean()], tiles='OpenStreetMap', zoom_start=10)

    for index, row in home_table.iterrows():

        html_template = """
        <html>

            <body>
            <font size="2" face="Courier New">
            <table>
                <tr>
                    <th>user_id</th>
                    <td align="right">{}</td>

                </tr>
                <tr>
                    <th>name</th>
                    <td align="right">{}</td>

                </tr>
                <tr>
                    <th>lat</th>  
                    <td align="right">{}</td>

                </tr>
                    <tr>
                    <th>long</th>
                    <td align="right">{}</td>

                </tr>
                    <tr>
                    <th>status</th>
                    <td align="right">{}</td>

                </tr>
            </table>

            </body>
        </html>
        """.format(row["user_id"], row["name"], row["lat"], row["long"], row["status"])

        if row["status"] == "infested":
            folium.CircleMarker(
                location=[row['lat'], row['long']],
                radius=5,
                color='red',
                fill=True,
                fill_opacity=1.0,
                popup=folium.Popup(html=html_template)
            ).add_to(map_1)
        else:
            folium.CircleMarker(
                location=[row['lat'], row['long']],
                radius=5,
                color='green',
                fill=True,
                fill_opacity=1.0,
                popup=folium.Popup(html=html_template)
            ).add_to(map_1)

    st_folium.folium_static(map_1, width=725)

    st.markdown("---")

    st.markdown("<h2 style='text-align: center;'> Check the state of the crops </h2", unsafe_allow_html=True)

    map_2 = folium.Map(location=[42.8333, 12.8333], tiles='OpenStreetMap', zoom_start=6)

    popup = folium.LatLngPopup()

    map_2.add_child(popup)

    # call to render Folium map in Streamlit
    st_data = st_folium.st_folium(map_2, width=725)

    col1, col2, col3 = st.columns(3)

    with col1:
        geo_check = st.checkbox('use your current position')



    if st_data['last_clicked'] is None:

        
        user_position = st_js.get_geolocation()

        with col2:
            text_input_1 = st.text_input(label='lat', value=(user_position['coords']['latitude'] if geo_check else ''))
        with col3:
            text_input_2 = st.text_input(label='long', value=(user_position['coords']['longitude'] if geo_check else ''))

    else:

        user_position = st_js.get_geolocation()

        with col2:
            text_input_1 = st.text_input(label='lat', value=(user_position['coords']['latitude'] if geo_check else st_data['last_clicked']['lat']))
        with col3:
            text_input_2 = st.text_input(label='long', value=(user_position['coords']['longitude'] if geo_check else st_data['last_clicked']['lng']))


    if st.button("Check"):

        try:
            Knn(dataframe=home_table, lat=float(text_input_1), long=float(text_input_2))
        except:
            st.error("No Microcontrollers in the area!", icon="🚨")

    st.markdown("---")

    st.markdown("<h2 style='text-align: center;'> Add User </h1>", unsafe_allow_html=True)

    with st.form(key="add user form", clear_on_submit=True):

        user_name = st.text_input(label="Create user name:")
        user_email = st.text_input(label="Insert user email:")

        submitted = st.form_submit_button("Add user")

        if submitted and user_name not in user_table["name"].values and user_email not in user_table["email"].values:
            try:
                post_user_data = {
                    "name": user_name,
                    "email": user_email,
                }
                response = requests.post(url=API_URL_ADD_USER, json=post_user_data)
                st.success('User added!', icon="✅")
            except:
                st.error("Please enter valid input!", icon="🚨")



if __name__ == "__main__":
    main()


