import streamlit as st
import streamlit.components.v1 as components
import streamlit_folium as st_folium
import streamlit_js_eval as st_js

import requests
import pandas as pd
import os
import base64
import folium


API_URL_GET_MICROCONTROLLERS_BY_USER = "https://djdkdw.deta.dev/microcontrollers/user/{}"

API_URL_ADD_MICROCONTROLLER = "https://djdkdw.deta.dev/microcontroller/add/"

API_URL_DELETE_MICROCONTROLLER_BY_ID = "https://djdkdw.deta.dev/microcontroller/delete/{}"

API_URL_GET_IMAGES_BY_MICROCONTROLLER = "https://djdkdw.deta.dev/images/microcontroller/{}"

API_URL_GET_USERS = "https://djdkdw.deta.dev/users/"



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



def images_list(user_id):

    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS_BY_USER.format(user_id))

    try:
        micro_id_list = list(micro_table['id'].values)

        images_df_list = []


        for item in micro_id_list:
            images_df_list.append(ritrieve_table(API_URL_GET_IMAGES_BY_MICROCONTROLLER.format(item)))

        images_df_list = list(filter(lambda x: x is not None, images_df_list))


        images_df = pd.concat(images_df_list)


        df_1 = images_df.rename(columns={"id":"image_id"})

        df_2 = df_1.drop(labels=["binaryimage"], axis=1)

        df_2 = df_2.reindex(columns=['micro_id', 'image_id', 'datetime', 'contents', 'species'])

        df_2['datetime'] = pd.to_datetime(images_df['datetime'])

        df_2.reset_index(drop=True, inplace=True)

        return df_1, df_2 # df_1 per il carousel, df_2 per la tabella
    
    except:
            st.error("No images to show!", icon="🚨")
            return None, None



def main(user_id: int):
    
    st.markdown("<h3 style='text-align: center;'> Microcontrollers List </h3>", unsafe_allow_html=True)

    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS_BY_USER.format(user_id))

    if micro_table is not None:
        
        micro_table = micro_table.drop(labels=["user_id", "images"], axis=1)

        # rename colums
        micro_table = micro_table.rename(columns={"id":"micro_id"})

        # replace values in status columns
        micro_table["status"] = micro_table["status"].replace({False: "safe", True: "infested"})

        micro_table.sort_values(by=["micro_id"], ascending=False)

        st.dataframe(micro_table, use_container_width=True)

        st.markdown("<h3 style='text-align: center;'> Microcontrollers Map </h3>", unsafe_allow_html=True)

        # centrare la mappa facendo la media delle coordinate
        map_1 = folium.Map(location=[micro_table["lat"].mean(), micro_table["long"].mean()], tiles='OpenStreetMap', zoom_start=10)

        for index, row in micro_table.iterrows():

            html_template = """
            <html>

                <body>
                <font size="2" face="Courier New">
                <table>
                    <tr>
                        <th>micro_id</th>
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
            """.format(row["micro_id"], row["lat"], row["long"], row["status"])

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

        # st_folium.folium_static(map_1, width=725)
        st_folium.folium_static(map_1)

    else:
        st.error("No microcontroller to show!", icon="🚨")

    # ADD MICROCONTROLLER

    st.markdown("<h3 style='text-align: center;'> Add Microcontroller </h3>", unsafe_allow_html=True)

    if micro_table is not None:

        map_2 = folium.Map(location=[micro_table["lat"].mean(), micro_table["long"].mean()], tiles='OpenStreetMap', zoom_start=10)
    
    else:

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


    if st.button("Add Microcontroller"):

        try:
            post_microcontroller_data = {
                "lat": float(text_input_1),
                "long": float(text_input_2),
                "user_id": user_id
            }
            response = requests.post(url=API_URL_ADD_MICROCONTROLLER, json=post_microcontroller_data)
            st.success('Microcontroller added!', icon="✅")
        except:
            st.error("Please enter valid input!", icon="🚨")


    st.markdown("<h3 style='text-align: center;'> Delete Microcontroller </h3>", unsafe_allow_html=True)

    with st.form(key="delete form", clear_on_submit=True):
   
        micro_table = micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS_BY_USER.format(user_id))


        micro_id = st.text_input(label="Insert Microcontroller Id:")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Delete Microcontroller")

        if submitted:

            try:

                micro_id = int(micro_id)

                if micro_id in micro_table['id'].values:
                    response = requests.delete(url=API_URL_DELETE_MICROCONTROLLER_BY_ID.format(micro_id))
                    if response.status_code == 200:
                        st.success('Microcontroller deleted!', icon="✅")
                    else:
                        raise ValueError("Please enter valid input!")
                else:
                    raise ValueError("Please enter valid input!")
                
            except ValueError as e:

                st.error("Please enter valid input!", icon="🚨")

    
    st.markdown("---")

    # IMAGES

    st.markdown("<h3 style='text-align: center;'> Images List </h3>", unsafe_allow_html=True)


    images_df_1, images_df_2 = images_list(user_id=user_id)

    st.dataframe(images_df_2, use_container_width=True)


    if images_df_1 is not None:

        # Crea la stringa HTML per il carousel
        carousel_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Carousel HTML</title>
            <style>
                .carousel {{
                    width: 640px;
                    height: 480px;
                    overflow: hidden;
                    position: absolute;
                    top: 25%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                }}
                .carousel img {{
                    width: 640px;
                    height: 480px;
                    position: absolute;
                    top: 0;
                    left: 0;
                    opacity: 0;
                    transition: opacity 1s ease-in-out;
                }}
                .carousel img.active {{
                    opacity: 1;
                }}
                .carousel button {{
                    position: absolute;
                    top: 50%;
                    transform: translateY(-50%);
                    z-index: 1;
                    background: transparent;
                    border: none;
                    color: white;
                    font-size: 2em;
                    cursor: pointer;
                }}
                .carousel button.prev {{
                    left: 10px;
                }}
                .carousel button.next {{
                    right: 10px;
                }}
                
            </style>
        </head>
        <body>

            <div class="carousel">
        """

        for i, row in images_df_1.iterrows():
            active_class = "active" if i == 0 else ""
            carousel_html += f'<img class="{active_class}" src="data:image/jpeg;base64,{row["binaryimage"]}">\n'
   


        carousel_html += """
                <button class="prev">&#10094;</button>
                <button class="next">&#10095;</button>
            </div>

            <script>
                var currentSlide = 0;
                var slides = document.querySelectorAll(".carousel img");
                var prevButton = document.querySelector(".carousel button.prev");
                var nextButton = document.querySelector(".carousel button.next");

                // Funzione per passare alla slide successiva
                function nextSlide() {
                    slides[currentSlide].classList.remove("active");
                    currentSlide = (currentSlide + 1) % slides.length;
                    slides[currentSlide].classList.add("active");
                }

                // Funzione per passare alla slide precedente
                function prevSlide() {
                    slides[currentSlide].classList.remove("active");
                    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                    slides[currentSlide].classList.add("active");
                }

                // Aggiungiamo l'evento click sui bottoni
                prevButton.addEventListener("click", prevSlide);
                nextButton.addEventListener("click", nextSlide);
            </script>

        </body>
        </html>
        """
        # Mostra il carousel in Streamlit
        components.html(carousel_html, height=1000)







if __name__ == "__main__":

    st.markdown("<h1 style='text-align: center;'>🔒 User Login 🔒</h1>", unsafe_allow_html=True)

    user_name = st.text_input("Insert user name:    ")
    user_email = st.text_input("Insert user email:    ")
    st.markdown("---")

    users_table = ritrieve_table(API_URL_GET_USERS)
    print(users_table)
    logged = False
 

    for index, row in users_table.iterrows():
        if user_name == row["name"] and user_email == row["email"]:
            logged = True
            user_id = row["id"]
        elif user_name == "" and user_email == "":
            pass
        elif user_name == "" or user_email == "":
            pass
        elif user_email != row["name"] and user_email != row["email"]:
            pass

    if logged:
        main(user_id=user_id)
    