import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components
import os
import base64



API_URL_GET_MICROCONTROLLERS_BY_USER = "https://djdkdw.deta.dev/microcontrollers/user/{}"

API_URL_GET_IMAGES_BY_MICROCONTROLLER = "https://djdkdw.deta.dev/images/microcontroller/{}"

USER_ID = 10 # cambiare questo


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

def images_list():

    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS_BY_USER.format(USER_ID))

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








def main():


    images_df_1, images_df_2 = images_list()
    

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
    main()



