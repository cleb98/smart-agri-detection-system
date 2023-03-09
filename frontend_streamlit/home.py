import streamlit as st
import requests
import pandas as pd

import folium
import streamlit_folium as st_folium


API_URL_GET_USERS = "https://djdkdw.deta.dev/users/"
API_URL_GET_MICROCONTROLLERS = "https://djdkdw.deta.dev/microcontrollers/"
API_URL_GET_IMAGES = "https://djdkdw.deta.dev/images/"

def ritrieve_table(url):
    response = requests.get(url=url)
    df = pd.DataFrame.from_dict(response.json())
    return df


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
    home_table = home_table.drop(labels=["email", "microcontrollers", "images"], axis=1)

    # rename colums
    home_table = home_table.rename(columns={"id":"user_id"})

    # replace values in status columns
    home_table["status"] = home_table["status"].replace({False: "safe", True: "infested"})

    st.dataframe(home_table, use_container_width=True)


    # create map
    st.markdown("<h2 style='text-align: center;'> Map </h1>", unsafe_allow_html=True)

    m = folium.Map(location=[home_table["lat"].mean(), home_table["long"].mean()], tiles='OpenStreetMap', zoom_start=10)

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
            ).add_to(m)
        else:
            folium.CircleMarker(
                location=[row['lat'], row['long']],
                radius=5,
                color='green',
                fill=True,
                fill_opacity=1.0,
                popup=folium.Popup(html=html_template)
            ).add_to(m)

    st_folium.folium_static(m, width=725)


if __name__ == "__main__":
    main()


