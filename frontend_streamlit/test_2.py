import os
import streamlit as st



directory = 'frontend_streamlit/images'

# genera una lista di nomi di file nella directory
images = os.listdir(directory)

# genera il tag HTML per ogni immagine nella directory
html = ''
for index, image in enumerate(images, start=1):
    # html += f'<img src="{directory}/{image}">'
    html += f'''<div class="mySlides fade">
                <div class="numbertext">{index} / {len(images)}</div>
                <img src="{directory}/{image}" style="width:100%">
                <div class="text">London, Ebgland</div>
            </div>\n'''

# stampa il codice HTML generato
print(html)