import streamlit as st
import requests
import pandas as pd


API_URL_ADD_USER = "https://djdkdw.deta.dev/user/add/"
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



user_table = ritrieve_table(API_URL_GET_USERS)
print(user_table)


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


