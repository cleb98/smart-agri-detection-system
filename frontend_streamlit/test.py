
import streamlit as st
import requests
import pandas as pd

import folium
import streamlit_folium as st_folium





st.markdown("<h1 style='text-align: center;'> User Microcontrollers </h1>", unsafe_allow_html=True) 



with st.form(key="login_form", clear_on_submit=True):

    dummy = False
    st.markdown("<h3 style='text-align: center;'>🔐 User Login 🔐</h3>", unsafe_allow_html=True)

    user_name = st.text_input(label="User Name")
    user_email = st.text_input(label="User Email")

    logged = st.form_submit_button("Login")

    if logged:
        
        dummy = True



if dummy:

    with st.expander(label="", expanded=True):

        st.markdown("<h3 style='text-align: center;'> Obtain Images from Microcontroller </h3>", unsafe_allow_html=True)



        a = st.selectbox(label="ID Microcontroller", options=[2,4,5,6], label_visibility="hidden")

print(dummy)    