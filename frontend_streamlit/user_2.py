import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import os
import folium
import streamlit_folium as st_folium


API_URL_GET_MICROCONTROLLERS_BY_USER = "https://djdkdw.deta.dev/microcontrollers/user/{}"



def ritrieve_table(url):
    response = requests.get(url=url)
    df = pd.DataFrame.from_dict(response.json())
    return df



def main():
    
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

    st_folium.folium_static(m, width=725)

    st.markdown("<h3 style='text-align: center;'> Obtain Images from Microcontroller </h3>", unsafe_allow_html=True)

    


    # components.html(
    #     """
    #         <!DOCTYPE html>
    #         <html>
    #         <head>
    #         <meta name="viewport" content="width=device-width, initial-scale=1">
    #         <style>
    #         * {box-sizing: border-box;}
    #         body {font-family: Verdana, sans-serif;}
    #         .mySlides {display: none;}
    #         img {vertical-align: middle;}

    #         /* Slideshow container */
    #         .slideshow-container {
    #         max-width: 1000px;
    #         position: relative;
    #         margin: auto;
    #         }

    #         /* Caption text */
    #         .text {
    #         color: #f2f2f2;
    #         font-size: 15px;
    #         padding: 8px 12px;
    #         position: absolute;
    #         bottom: 8px;
    #         width: 100%;
    #         text-align: center;
    #         }

    #         /* Number text (1/3 etc) */
    #         .numbertext {
    #         color: #f2f2f2;
    #         font-size: 12px;
    #         padding: 8px 12px;
    #         position: absolute;
    #         top: 0;
    #         }

    #         /* The dots/bullets/indicators */
    #         .dot {
    #         height: 15px;
    #         width: 15px;
    #         margin: 0 2px;
    #         background-color: #bbb;
    #         border-radius: 50%;
    #         display: inline-block;
    #         transition: background-color 0.6s ease;
    #         }

    #         .active {
    #         background-color: #717171;
    #         }

    #         /* Fading animation */
    #         .fade {
    #         animation-name: fade;
    #         animation-duration: 1.5s;
    #         }

    #         @keyframes fade {
    #         from {opacity: .4} 
    #         to {opacity: 1}
    #         }

    #         /* On smaller screens, decrease text size */
    #         @media only screen and (max-width: 300px) {
    #         .text {font-size: 11px}
    #         }
    #         </style>
    #         </head>
    #         <body>

    #         <h2>Automatic Slideshow</h2>
    #         <p>Change image every 10 seconds:</p>

    #         <div class="slideshow-container">

    #         <div class="mySlides fade">
    #         <div class="numbertext">1 / 3</div>
    #         <img src="https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920" style="width:100%">
    #         <div class="text">Caption Text</div>
    #         </div>

    #         <div class="mySlides fade">
    #         <div class="numbertext">2 / 3</div>
    #         <img src="https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920" style="width:100%">
    #         <div class="text">Caption Two</div>
    #         </div>

    #         <div class="mySlides fade">
    #         <div class="numbertext">3 / 3</div>
    #         <img src="https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920" style="width:100%">
    #         <div class="text">Caption Three</div>
    #         </div>

    #         </div>
    #         <br>

    #         <div style="text-align:center">
    #         <span class="dot"></span> 
    #         <span class="dot"></span> 
    #         <span class="dot"></span> 
    #         </div>

    #         <script>
    #         let slideIndex = 0;
    #         showSlides();

    #         function showSlides() {
    #         let i;
    #         let slides = document.getElementsByClassName("mySlides");
    #         let dots = document.getElementsByClassName("dot");
    #         for (i = 0; i < slides.length; i++) {
    #             slides[i].style.display = "none";  
    #         }
    #         slideIndex++;
    #         if (slideIndex > slides.length) {slideIndex = 1}    
    #         for (i = 0; i < dots.length; i++) {
    #             dots[i].className = dots[i].className.replace(" active", "");
    #         }
    #         slides[slideIndex-1].style.display = "block";  
    #         dots[slideIndex-1].className += " active";
    #         setTimeout(showSlides, 10000); // Change image every 10 seconds
    #         }
    #         </script>

    #         </body>
    #         </html> 
    #     """,
    #     height=600,
    # )

    # components.html(
    #     """
    #         <!DOCTYPE html>
    #         <html>
    #         <head>
    #         <meta name="viewport" content="width=device-width, initial-scale=1">
    #         <style>
    #         * {box-sizing: border-box}
    #         body {font-family: Verdana, sans-serif; margin:0}
    #         .mySlides {display: none}
    #         img {vertical-align: middle;}

    #         /* Slideshow container */
    #         .slideshow-container {
    #         max-width: 1000px;
    #         position: relative;
    #         margin: auto;
    #         }

    #         /* Next & previous buttons */
    #         .prev, .next {
    #         cursor: pointer;
    #         position: absolute;
    #         top: 50%;
    #         width: auto;
    #         padding: 16px;
    #         margin-top: -22px;
    #         color: white;
    #         font-weight: bold;
    #         font-size: 18px;
    #         transition: 0.6s ease;
    #         border-radius: 0 3px 3px 0;
    #         user-select: none;
    #         }

    #         /* Position the "next button" to the right */
    #         .next {
    #         right: 0;
    #         border-radius: 3px 0 0 3px;
    #         }

    #         /* On hover, add a black background color with a little bit see-through */
    #         .prev:hover, .next:hover {
    #         background-color: rgba(0,0,0,0.8);
    #         }

    #         /* Caption text */
    #         .text {
    #         color: #f2f2f2;
    #         font-size: 15px;
    #         padding: 8px 12px;
    #         position: absolute;
    #         bottom: 8px;
    #         width: 100%;
    #         text-align: center;
    #         }

    #         /* Number text (1/3 etc) */
    #         .numbertext {
    #         color: #f2f2f2;
    #         font-size: 12px;
    #         padding: 8px 12px;
    #         position: absolute;
    #         top: 0;
    #         }

    #         /* The dots/bullets/indicators */
    #         .dot {
    #         cursor: pointer;
    #         height: 15px;
    #         width: 15px;
    #         margin: 0 2px;
    #         background-color: #bbb;
    #         border-radius: 50%;
    #         display: inline-block;
    #         transition: background-color 0.6s ease;
    #         }

    #         .active, .dot:hover {
    #         background-color: #717171;
    #         }

    #         /* Fading animation */
    #         .fade {
    #         animation-name: fade;
    #         animation-duration: 1.5s;
    #         }

    #         @keyframes fade {
    #         from {opacity: .4} 
    #         to {opacity: 1}
    #         }

    #         /* On smaller screens, decrease text size */
    #         @media only screen and (max-width: 300px) {
    #         .prev, .next,.text {font-size: 11px}
    #         }
    #         </style>
    #         </head>
    #         <body>

    #         <div class="slideshow-container">

    #         <div class="mySlides fade">
    #         <div class="numbertext">1 / 3</div>
    #         <img src="https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920" style="width:100%">
    #         <div class="text">Caption Text</div>
    #         </div>

    #         <div class="mySlides fade">
    #         <div class="numbertext">2 / 3</div>
    #         <img src="https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920" style="width:100%">
    #         <div class="text">Caption Two</div>
    #         </div>

    #         <div class="mySlides fade">
    #         <div class="numbertext">3 / 3</div>
    #         <img src="https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920" style="width:100%">
    #         <div class="text">Caption Three</div>
    #         </div>

    #         <a class="prev" onclick="plusSlides(-1)">❮</a>
    #         <a class="next" onclick="plusSlides(1)">❯</a>

    #         </div>
    #         <br>

    #         <div style="text-align:center">
    #         <span class="dot" onclick="currentSlide(1)"></span> 
    #         <span class="dot" onclick="currentSlide(2)"></span> 
    #         <span class="dot" onclick="currentSlide(3)"></span> 
    #         </div>

    #         <script>
    #         let slideIndex = 1;
    #         showSlides(slideIndex);

    #         function plusSlides(n) {
    #         showSlides(slideIndex += n);
    #         }

    #         function currentSlide(n) {
    #         showSlides(slideIndex = n);
    #         }

    #         function showSlides(n) {
    #         let i;
    #         let slides = document.getElementsByClassName("mySlides");
    #         let dots = document.getElementsByClassName("dot");
    #         if (n > slides.length) {slideIndex = 1}    
    #         if (n < 1) {slideIndex = slides.length}
    #         for (i = 0; i < slides.length; i++) {
    #             slides[i].style.display = "none";  
    #         }
    #         for (i = 0; i < dots.length; i++) {
    #             dots[i].className = dots[i].className.replace(" active", "");
    #         }
    #         slides[slideIndex-1].style.display = "block";  
    #         dots[slideIndex-1].className += " active";
    #         }
    #         </script>

    #         </body>
    #         </html> 

    #     """,
    #     height=600,
    # )

    # components.html(
    #     """
    #     <!DOCTYPE html>
    #     <html>
    #     <head>
    #         <title>Slideshow Images</title>
    #         <style>
    #         * {
    #             box-sizing: border-box
    #         }
    #         body {
    #             font-family: Verdana, sans-serif;
    #             margin: 0
    #         }
    #         .mySlides {
    #             display: none
    #         }
    #         img {
    #             vertical-align: middle;
    #         }
    #         .slideshow-container {
    #             max-width: 1000px;
    #             position: relative;
    #             margin: auto;
    #         }
    #         /* Next & previous buttons */
    #         .prev,
    #         .next {
    #             cursor: pointer;
    #             position: absolute;
    #             top: 50%;
    #             width: auto;
    #             padding: 16px;
    #             margin-top: -22px;
    #             color: white;
    #             font-weight: bold;
    #             font-size: 18px;
    #             transition: 0.6s ease;
    #             border-radius: 0 3px 3px 0;
    #             user-select: none;
    #         }
    #         /* Position the "next button" to the right */
    #         .next {
    #             right: 0;
    #             border-radius: 3px 0 0 3px;
    #         }
    #         /* On hover, add a black background color with a little bit see-through */
    #         .prev:hover,
    #         .next:hover {
    #             background-color: rgba(0, 0, 0, 0.8);
    #         }
    #         /* Caption text */
    #         .text {
    #             color: #ffffff;
    #             font-size: 15px;
    #             padding: 8px 12px;
    #             position: absolute;
    #             bottom: 8px;
    #             width: 100%;
    #             text-align: center;
    #         }
    #         /* Number text (1/3 etc) */
    #         .numbertext {
    #             color: #ffffff;
    #             font-size: 12px;
    #             padding: 8px 12px;
    #             position: absolute;
    #             top: 0;
    #         }
    #         /* The dots/bullets/indicators */
    #         .dot {
    #             cursor: pointer;
    #             height: 15px;
    #             width: 15px;
    #             margin: 0 2px;
    #             background-color: #999999;
    #             border-radius: 50%;
    #             display: inline-block;
    #             transition: background-color 0.6s ease;
    #         }
    #         .active,
    #         .dot:hover {
    #             background-color: #111111;
    #         }
    #         /* Fading animation */
    #         .fade {
    #             -webkit-animation-name: fade;
    #             -webkit-animation-duration: 1.5s;
    #             animation-name: fade;
    #             animation-duration: 1.5s;
    #         }
    #         @-webkit-keyframes fade {
    #             from {
    #             opacity: .4
    #             }
    #             to {
    #             opacity: 1
    #             }
    #         }
    #         @keyframes fade {
    #             from {
    #             opacity: .4
    #             }
    #             to {
    #             opacity: 1
    #             }
    #         }
    #         /* On smaller screens, decrease text size */
    #         @media only screen and (max-width: 300px) {
    #             .prev,
    #             .next,
    #             .text {
    #             font-size: 11px
    #             }
    #         }
    #         </style>
    #     </head>
    #     <body>
    #         <div class="slideshow-container">
    #         <div class="mySlides fade">
    #             <div class="numbertext">1 / 3</div>
    #             <img src="https://www.w3docs.com/uploads/media/default/0001/03/66cf5094908491e69d8187bcf934050a4800b37f.jpeg" style="width:100%">
    #             <div class="text">London, Ebgland</div>
    #         </div>
    #         <div class="mySlides fade">
    #             <div class="numbertext">2 / 3</div>
    #             <img src="https://www.w3docs.com/uploads/media/default/0001/03/b7d624354d5fa22e38b0ab1f9b905fb08ccc6a05.jpeg" style="width:100%">
    #             <div class="text">Sunset in Romania</div>
    #         </div>
    #         <div class="mySlides fade">
    #             <div class="numbertext">3 / 3</div>
    #             <img src="https://www.w3docs.com/uploads/media/default/0001/03/5bfad15a7fd24d448a48605baf52655a5bbe5a71.jpeg" style="width:100%">
    #             <div class="text">New York, USA</div>
    #         </div>
    #         <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
    #         <a class="next" onclick="plusSlides(1)">&#10095;</a>
    #         </div>
    #         <br>
    #         <div style="text-align:center">
    #         <span class="dot" onclick="currentSlide(0)"></span>
    #         <span class="dot" onclick="currentSlide(1)"></span>
    #         <span class="dot" onclick="currentSlide(2)"></span>
    #         </div>
    #         <script>
    #         let slideIndex = 0;
    #         let timeoutId = null;
    #         const slides = document.getElementsByClassName("mySlides");
    #         const dots = document.getElementsByClassName("dot");
            
    #         showSlides();
    #         function currentSlide(index) {
    #             slideIndex = index;
    #             showSlides();
    #         }
    #         function plusSlides(step) {
                
    #             if(step < 0) {
    #                 slideIndex -= 2;
                    
    #                 if(slideIndex < 0) {
    #                 slideIndex = slides.length - 1;
    #                 }
    #             }
                
    #             showSlides();
    #         }
    #         function showSlides() {
    #             for(let i = 0; i < slides.length; i++) {
    #             slides[i].style.display = "none";
    #             dots[i].classList.remove('active');
    #             }
    #             slideIndex++;
    #             if(slideIndex > slides.length) {
    #             slideIndex = 1
    #             }
    #             slides[slideIndex - 1].style.display = "block";
    #             dots[slideIndex - 1].classList.add('active');
    #             if(timeoutId) {
    #                 clearTimeout(timeoutId);
    #             }
    #             timeoutId = setTimeout(showSlides, 10000); // Change image every 10 seconds
    #         }
    #         </script>
    #     </body>
    #     </html>
    #     """,
    #     height=600,
    # )


    directory = 'images'

    # genera una lista di nomi di file nella directory
    images = os.listdir(directory)

    # genera il tag HTML per ogni immagine nella directory
    html = ''
    for index, image in enumerate(images, start=1):
        # html += f'<img src="{directory}/{image}">'
        print(index, image)
        html += f'''<div class="mySlides fade">
                    <div class="numbertext">{index} / {len(images)}</div>
                    <img src="{directory}/{image}" style="width:100%">
                    <div class="text">London, Ebgland</div>
                </div>\n'''

    # stampa il codice HTML generato
    print(html)




    # html_complete = """
    #             <!DOCTYPE html>
    #             <html>
    #             <head>
    #                 <title>Slideshow Images</title>
    #                 <style>
    #                 * {
    #                     box-sizing: border-box
    #                 }
    #                 body {
    #                     font-family: Verdana, sans-serif;
    #                     margin: 0
    #                 }
    #                 .mySlides {
    #                     display: none
    #                 }
    #                 img {
    #                     vertical-align: middle;
    #                 }
    #                 .slideshow-container {
    #                     max-width: 1000px;
    #                     position: relative;
    #                     margin: auto;
    #                 }
    #                 /* Next & previous buttons */
    #                 .prev,
    #                 .next {
    #                     cursor: pointer;
    #                     position: absolute;
    #                     top: 50%;
    #                     width: auto;
    #                     padding: 16px;
    #                     margin-top: -22px;
    #                     color: white;
    #                     font-weight: bold;
    #                     font-size: 18px;
    #                     transition: 0.6s ease;
    #                     border-radius: 0 3px 3px 0;
    #                     user-select: none;
    #                 }
    #                 /* Position the "next button" to the right */
    #                 .next {
    #                     right: 0;
    #                     border-radius: 3px 0 0 3px;
    #                 }
    #                 /* On hover, add a black background color with a little bit see-through */
    #                 .prev:hover,
    #                 .next:hover {
    #                     background-color: rgba(0, 0, 0, 0.8);
    #                 }
    #                 /* Caption text */
    #                 .text {
    #                     color: #ffffff;
    #                     font-size: 15px;
    #                     padding: 8px 12px;
    #                     position: absolute;
    #                     bottom: 8px;
    #                     width: 100%;
    #                     text-align: center;
    #                 }
    #                 /* Number text (1/3 etc) */
    #                 .numbertext {
    #                     color: #ffffff;
    #                     font-size: 12px;
    #                     padding: 8px 12px;
    #                     position: absolute;
    #                     top: 0;
    #                 }
    #                 /* The dots/bullets/indicators */
    #                 .dot {
    #                     cursor: pointer;
    #                     height: 15px;
    #                     width: 15px;
    #                     margin: 0 2px;
    #                     background-color: #999999;
    #                     border-radius: 50%;
    #                     display: inline-block;
    #                     transition: background-color 0.6s ease;
    #                 }
    #                 .active,
    #                 .dot:hover {
    #                     background-color: #111111;
    #                 }
    #                 /* Fading animation */
    #                 .fade {
    #                     -webkit-animation-name: fade;
    #                     -webkit-animation-duration: 1.5s;
    #                     animation-name: fade;
    #                     animation-duration: 1.5s;
    #                 }
    #                 @-webkit-keyframes fade {
    #                     from {
    #                     opacity: .4
    #                     }
    #                     to {
    #                     opacity: 1
    #                     }
    #                 }
    #                 @keyframes fade {
    #                     from {
    #                     opacity: .4
    #                     }
    #                     to {
    #                     opacity: 1
    #                     }
    #                 }
    #                 /* On smaller screens, decrease text size */
    #                 @media only screen and (max-width: 300px) {
    #                     .prev,
    #                     .next,
    #                     .text {
    #                     font-size: 11px
    #                     }
    #                 }
    #                 </style>
    #             </head>
    #             <body>
    #                 <div class="slideshow-container">
    #                 {}
    #                 <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
    #                 <a class="next" onclick="plusSlides(1)">&#10095;</a>
    #                 </div>
    #                 <br>
    #                 <div style="text-align:center">
    #                 <span class="dot" onclick="currentSlide(0)"></span>
    #                 <span class="dot" onclick="currentSlide(1)"></span>
    #                 <span class="dot" onclick="currentSlide(2)"></span>
    #                 </div>
    #                 <script>
    #                 let slideIndex = 0;
    #                 let timeoutId = null;
    #                 const slides = document.getElementsByClassName("mySlides");
    #                 const dots = document.getElementsByClassName("dot");
                    
    #                 showSlides();
    #                 function currentSlide(index) {
    #                     slideIndex = index;
    #                     showSlides();
    #                 }
    #                 function plusSlides(step) {
                        
    #                     if(step < 0) {
    #                         slideIndex -= 2;
                            
    #                         if(slideIndex < 0) {
    #                         slideIndex = slides.length - 1;
    #                         }
    #                     }
                        
    #                     showSlides();
    #                 }
    #                 function showSlides() {
    #                     for(let i = 0; i < slides.length; i++) {
    #                     slides[i].style.display = "none";
    #                     dots[i].classList.remove('active');
    #                     }
    #                     slideIndex++;
    #                     if(slideIndex > slides.length) {
    #                     slideIndex = 1
    #                     }
    #                     slides[slideIndex - 1].style.display = "block";
    #                     dots[slideIndex - 1].classList.add('active');
    #                     if(timeoutId) {
    #                         clearTimeout(timeoutId);
    #                     }
    #                     timeoutId = setTimeout(showSlides, 10000); // Change image every 10 seconds
    #                 }
    #                 </script>
    #             </body>
    #             </html>
    #     """.format(html)
    
    # print(html_complete)

    # components.html(
    #     """
    #     <!DOCTYPE html>
    #     <html>
    #     <head>
    #         <title>Slideshow Images</title>
    #         <style>
    #         * {
    #             box-sizing: border-box
    #         }
    #         body {
    #             font-family: Verdana, sans-serif;
    #             margin: 0
    #         }
    #         .mySlides {
    #             display: none
    #         }
    #         img {
    #             vertical-align: middle;
    #         }
    #         .slideshow-container {
    #             max-width: 1000px;
    #             position: relative;
    #             margin: auto;
    #         }
    #         /* Next & previous buttons */
    #         .prev,
    #         .next {
    #             cursor: pointer;
    #             position: absolute;
    #             top: 50%;
    #             width: auto;
    #             padding: 16px;
    #             margin-top: -22px;
    #             color: white;
    #             font-weight: bold;
    #             font-size: 18px;
    #             transition: 0.6s ease;
    #             border-radius: 0 3px 3px 0;
    #             user-select: none;
    #         }
    #         /* Position the "next button" to the right */
    #         .next {
    #             right: 0;
    #             border-radius: 3px 0 0 3px;
    #         }
    #         /* On hover, add a black background color with a little bit see-through */
    #         .prev:hover,
    #         .next:hover {
    #             background-color: rgba(0, 0, 0, 0.8);
    #         }
    #         /* Caption text */
    #         .text {
    #             color: #ffffff;
    #             font-size: 15px;
    #             padding: 8px 12px;
    #             position: absolute;
    #             bottom: 8px;
    #             width: 100%;
    #             text-align: center;
    #         }
    #         /* Number text (1/3 etc) */
    #         .numbertext {
    #             color: #ffffff;
    #             font-size: 12px;
    #             padding: 8px 12px;
    #             position: absolute;
    #             top: 0;
    #         }
    #         /* The dots/bullets/indicators */
    #         .dot {
    #             cursor: pointer;
    #             height: 15px;
    #             width: 15px;
    #             margin: 0 2px;
    #             background-color: #999999;
    #             border-radius: 50%;
    #             display: inline-block;
    #             transition: background-color 0.6s ease;
    #         }
    #         .active,
    #         .dot:hover {
    #             background-color: #111111;
    #         }
    #         /* Fading animation */
    #         .fade {
    #             -webkit-animation-name: fade;
    #             -webkit-animation-duration: 1.5s;
    #             animation-name: fade;
    #             animation-duration: 1.5s;
    #         }
    #         @-webkit-keyframes fade {
    #             from {
    #             opacity: .4
    #             }
    #             to {
    #             opacity: 1
    #             }
    #         }
    #         @keyframes fade {
    #             from {
    #             opacity: .4
    #             }
    #             to {
    #             opacity: 1
    #             }
    #         }
    #         /* On smaller screens, decrease text size */
    #         @media only screen and (max-width: 300px) {
    #             .prev,
    #             .next,
    #             .text {
    #             font-size: 11px
    #             }
    #         }
    #         </style>
    #     </head>
    #     <body>
    #         <div class="slideshow-container">
    #         {}
    #         <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
    #         <a class="next" onclick="plusSlides(1)">&#10095;</a>
    #         </div>
    #         <br>
    #         <div style="text-align:center">
    #         <span class="dot" onclick="currentSlide(0)"></span>
    #         <span class="dot" onclick="currentSlide(1)"></span>
    #         <span class="dot" onclick="currentSlide(2)"></span>
    #         </div>
    #         <script>
    #         let slideIndex = 0;
    #         let timeoutId = null;
    #         const slides = document.getElementsByClassName("mySlides");
    #         const dots = document.getElementsByClassName("dot");
            
    #         showSlides();
    #         function currentSlide(index) {
    #             slideIndex = index;
    #             showSlides();
    #         }
    #         function plusSlides(step) {
                
    #             if(step < 0) {
    #                 slideIndex -= 2;
                    
    #                 if(slideIndex < 0) {
    #                 slideIndex = slides.length - 1;
    #                 }
    #             }
                
    #             showSlides();
    #         }
    #         function showSlides() {
    #             for(let i = 0; i < slides.length; i++) {
    #             slides[i].style.display = "none";
    #             dots[i].classList.remove('active');
    #             }
    #             slideIndex++;
    #             if(slideIndex > slides.length) {
    #             slideIndex = 1
    #             }
    #             slides[slideIndex - 1].style.display = "block";
    #             dots[slideIndex - 1].classList.add('active');
    #             if(timeoutId) {
    #                 clearTimeout(timeoutId);
    #             }
    #             timeoutId = setTimeout(showSlides, 10000); // Change image every 10 seconds
    #         }
    #         </script>
    #     </body>
    #     </html>
    #     """.format(html),
    #     height=600,
    # )






if __name__ == "__main__":
    main()