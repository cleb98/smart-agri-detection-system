import streamlit as st
import streamlit.components.v1 as components

carousel_html = """
                <!DOCTYPE html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                * {box-sizing: border-box}
                body {font-family: Verdana, sans-serif; margin:0}
                .mySlides {display: none}
                img {vertical-align: middle;}

                /* Slideshow container */
                .slideshow-container {
                max-width: 1000px;
                position: relative;
                margin: auto;
                }

                /* Next & previous buttons */
                .prev, .next {
                cursor: pointer;
                position: absolute;
                top: 50%;
                width: auto;
                padding: 16px;
                margin-top: -22px;
                color: white;
                font-weight: bold;
                font-size: 18px;
                transition: 0.6s ease;
                border-radius: 0 3px 3px 0;
                user-select: none;
                }

                /* Position the "next button" to the right */
                .next {
                right: 0;
                border-radius: 3px 0 0 3px;
                }

                /* On hover, add a black background color with a little bit see-through */
                .prev:hover, .next:hover {
                background-color: rgba(0,0,0,0.8);
                }

                /* Caption text */
                .text {
                color: #f2f2f2;
                font-size: 15px;
                padding: 8px 12px;
                position: absolute;
                bottom: 8px;
                width: 100%;
                text-align: center;
                }


                /* Fading animation */
                .fade {
                animation-name: fade;
                animation-duration: 1.5s;
                }

                @keyframes fade {
                from {opacity: .4} 
                to {opacity: 1}
                }

                /* On smaller screens, decrease text size */
                @media only screen and (max-width: 300px) {
                .prev, .next,.text {font-size: 11px}
                }
                </style>
                </head>
                <body>

                <div class="slideshow-container">

                <div class="mySlides fade">
                <img src="https://source.unsplash.com/random?landscape,mountain" style="width:100%">
                <div class="text">Caption Text</div>
                </div>

                <div class="mySlides fade">
                <img src="https://source.unsplash.com/random?landscape,cars" style="width:100%">
                <div class="text">Caption Two</div>
                </div>

                <div class="mySlides fade">
                <img src="https://source.unsplash.com/random?landscape,night" style="width:100%">
                <div class="text">Caption Three</div>
                </div>

                <a class="prev" onclick="plusSlides(-1)">❮</a>
                <a class="next" onclick="plusSlides(1)">❯</a>

                </div>
                <br>

                <div style="text-align:center">
                <span class="dot" onclick="currentSlide(1)"></span> 
                <span class="dot" onclick="currentSlide(2)"></span> 
                <span class="dot" onclick="currentSlide(3)"></span> 
                </div>

                <script>
                let slideIndex = 1;
                showSlides(slideIndex);

                function plusSlides(n) {
                showSlides(slideIndex += n);
                }

                function currentSlide(n) {
                showSlides(slideIndex = n);
                }

                function showSlides(n) {
                let i;
                let slides = document.getElementsByClassName("mySlides");
                let dots = document.getElementsByClassName("dot");
                if (n > slides.length) {slideIndex = 1}    
                if (n < 1) {slideIndex = slides.length}
                for (i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";  
                }
                for (i = 0; i < dots.length; i++) {
                    dots[i].className = dots[i].className.replace(" active", "");
                }
                slides[slideIndex-1].style.display = "block";  
                dots[slideIndex-1].className += " active";
                }
                </script>

                </body>
                </html>"""

# Mostra il carousel in Streamlit
components.html(carousel_html, height=1000)