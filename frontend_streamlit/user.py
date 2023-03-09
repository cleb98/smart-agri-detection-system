import streamlit as st
import requests
import pandas as pd

import folium
import streamlit_folium as st_folium


API_URL_GET_MICROCONTROLLERS_BY_USER = "https://djdkdw.deta.dev/microcontrollers/user/{}"



def ritrieve_table(url):
    response = requests.get(url=url)
    df = pd.DataFrame.from_dict(response.json())
    return df



def main():
    


    st.markdown("<h1 style='text-align: center;'> User Microcontrollers </h1>", unsafe_allow_html=True) 

    

    with st.form(key="login_form", clear_on_submit=True):
        
        st.markdown("<h3 style='text-align: center;'>🔐 User Login 🔐</h3>", unsafe_allow_html=True)

        user_name = st.text_input(label="User Name")
        user_email = st.text_input(label="User Email")

        logged = st.form_submit_button("Login")

    if logged:

        print(user_name)
        print(user_email)

        with st.expander(label="", expanded=True):


            st.markdown("<h3 style='text-align: center;'> Microcontrollers List </h3>", unsafe_allow_html=True)

            micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS_BY_USER.format(1)) # deve cambiare dinamicamente

            micro_table = micro_table.drop(labels=["user_id", "images"], axis=1)

            # rename colums
            micro_table = micro_table.rename(columns={"id":"micro_id"})

            # replace values in status columns
            micro_table["status"] = micro_table["status"].replace({False: "safe", True: "infested"})

            micro_table.sort_values(by=["micro_id"], ascending=False)

            st.table(micro_table)


            st.markdown("<h3 style='text-align: center;'> Microcontrollers Map </h3>", unsafe_allow_html=True)

            m = folium.Map(location=[44.6563, 11.0959], tiles='OpenStreetMap', zoom_start=10)

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

            st_folium.folium_static(m, width=670)


            st.markdown("<h3 style='text-align: center;'> Obtain Images from Microcontroller </h3>", unsafe_allow_html=True)





if __name__ == "__main__":
    main()